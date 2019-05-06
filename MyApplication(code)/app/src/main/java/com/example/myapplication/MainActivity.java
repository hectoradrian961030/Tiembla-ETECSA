package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.app.AppOpsManager;
import android.app.usage.NetworkStats;
import android.app.usage.NetworkStatsManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.net.ConnectivityManager;
import android.net.TrafficStats;
import android.os.Bundle;
import android.os.RemoteException;
import android.provider.CallLog;
import android.provider.Settings;
import android.provider.Telephony;
import android.renderscript.ScriptIntrinsicYuvToRGB;
import android.telecom.Call;
import android.telephony.TelephonyManager;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import java.sql.Date;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    int sms;
    int voice ;
    long data;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //permissions
        //checkPermission();

        init();


        Calendar today = Calendar.getInstance();
        Calendar prev =  Calendar.getInstance();
        prev.add(Calendar.DATE, -30);

        long LL = prev.getTime().getTime();
        long RR = today.getTime().getTime();

        sms = smsCounter(LL, RR);
        voice = minCounter(LL, RR) / 60;
        data = getTransferMobile(LL, RR) / (1024 * 1024);

        TextView s = findViewById( R.id.txt_sms);
        s.setText(String.valueOf(sms));
        TextView v = findViewById( R.id.txt_voice);
        v.setText(String.valueOf(voice));
        TextView d = findViewById( R.id.txt_data);
        d.setText(String.valueOf(data));

        TextView t = findViewById(R.id.txt_init);
        t.setText(" Esta app muestra tu consumo de los servicios de Etecsa en los pasados 30 dias (Por los cuales usted ha sido cobrado) " +
                        "Para obtener consejos de que planes comprar,  comparta sus datos en telegram con nuestro bot  PlanesEtecsa");


    }


    void init() {
        int PERMISSION_ALL = 1;
        String[] PERMISSIONS = {
                android.Manifest.permission.READ_SMS,
                android.Manifest.permission.READ_CALL_LOG,
                android.Manifest.permission.READ_PHONE_STATE,
                android.Manifest.permission.INTERNET,
                android.Manifest.permission.ACCESS_NETWORK_STATE
        };
        if (!checkPermission(PERMISSIONS)) {
            ActivityCompat.requestPermissions(this, PERMISSIONS, PERMISSION_ALL);
        }

        boolean granted = false;
        AppOpsManager appOps = (AppOpsManager) getSystemService(Context.APP_OPS_SERVICE);
        int mode = appOps.checkOpNoThrow(AppOpsManager.OPSTR_GET_USAGE_STATS,
                android.os.Process.myUid(), getPackageName());

        if (mode == AppOpsManager.MODE_DEFAULT) {
            granted = (checkCallingOrSelfPermission(android.Manifest.permission.PACKAGE_USAGE_STATS) == PackageManager.PERMISSION_GRANTED);
        } else {
            granted = (mode == AppOpsManager.MODE_ALLOWED);
        }
        if (!granted) {
            Intent intent = new Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS);
            startActivity(intent);
        }

    }

//    void checkPermission() {
//        if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CALL_LOG)
//                != PackageManager.PERMISSION_GRANTED) {
//            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.READ_CALL_LOG}, 1);
//        }
//        if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_SMS)
//                != PackageManager.PERMISSION_GRANTED) {
//            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.READ_SMS}, 1);
//        }
//        if (checkSelfPermission(Manifest.permission.READ_PHONE_STATE) != PackageManager.PERMISSION_GRANTED) {
//
//            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.READ_PHONE_STATE}, 1);
//            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.PACKAGE_USAGE_STATS}, 1);
//
//        }
//    }

    boolean checkPermission(String... permissions) {
        if (permissions != null) {
            for (String permission : permissions) {
                if (ActivityCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                    return false;
                }
            }
        }
        return true;
    }

    int smsCounter(long L, long R) {
        int ans = 0;
        try {
            Cursor smsCursor = getContentResolver().query(Telephony.Sms.CONTENT_URI, null, null, null, null);

            int type = smsCursor.getColumnIndex(Telephony.Sms.TYPE);
            int date = smsCursor.getColumnIndex(Telephony.Sms.DATE);



            while (smsCursor.moveToNext()) {
                if (smsCursor.getInt(type) == Telephony.Sms.MESSAGE_TYPE_SENT) {
                    long longDate = Long.parseLong(smsCursor.getString(date));
                    if(longDate >= L && longDate <= R) ans++;
                }
            }

        } catch (Exception e) {
            //info.setText(e.getMessage());
        }

        return ans;
    }

    boolean NumberFilter(String number, int type) {
        if (type == CallLog.Calls.OUTGOING_TYPE && !number.startsWith("*99")) return true;
        if (type == CallLog.Calls.INCOMING_TYPE && !number.startsWith("99")) return true;
        return false;
    }

    int minCounter(long L, long R) {
        Cursor minCursor = getContentResolver().query(
                CallLog.Calls.CONTENT_URI, null, null, null, null);

        int ans = 0;

        int type = minCursor.getColumnIndex(CallLog.Calls.TYPE);
        int duration = minCursor.getColumnIndex(CallLog.Calls.DURATION);
        int number = minCursor.getColumnIndex(CallLog.Calls.NUMBER);
        int date = minCursor.getColumnIndex(CallLog.Calls.DATE);

        while (minCursor.moveToNext()) {
            if (NumberFilter(minCursor.getString(number), minCursor.getInt(type))) {

                long longDate = Long.parseLong(minCursor.getString(date));
                if(longDate >= L && longDate <= R) ans += minCursor.getInt(duration);
            }
        }
        return ans;
    }

    public long getTransferMobile(long lower, long upper) {
        TelephonyManager tm = (TelephonyManager) getSystemService(Context.TELEPHONY_SERVICE);

        if (checkSelfPermission(Manifest.permission.READ_PHONE_STATE) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    Activity#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for Activity#requestPermissions for more details.
            return 0;
        }
        String subs = tm.getSubscriberId();
        NetworkStatsManager networkStatsManager = (NetworkStatsManager) getApplicationContext().getSystemService(Context.NETWORK_STATS_SERVICE);
        NetworkStats.Bucket bucket;
        try {
            bucket = networkStatsManager.querySummaryForDevice(ConnectivityManager.TYPE_MOBILE,
                    subs,
                    lower,
                    upper);
        } catch (RemoteException e) {
            //info.setText(e.toString());
            return 1;
        }
        return bucket.getRxBytes() + bucket.getTxBytes();
    }



    public void shareTelegram(View a)
    {

        String message = "/calculate " + String.valueOf(voice) + " " + String.valueOf(sms) + " " + String.valueOf(data);

        Intent waIntent = new Intent(Intent.ACTION_SEND);
        waIntent.setType("text/plain");
        waIntent.setPackage("org.telegram.messenger");
        if (waIntent != null) {
            waIntent.putExtra(Intent.EXTRA_TEXT, message);//
            startActivity(Intent.createChooser(waIntent, "Share with"));
        }
        else
        {
            Toast.makeText(getApplicationContext(), "Telegram is not installed", Toast.LENGTH_SHORT).show();
        }

    }


}

