package com.example.myapplication;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;

public class SendMessage {
    public static String sendToTelegram(String data) {
        String urlString = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s";

        //Add Telegram token (given Token is fake)
        String apiToken = "747519216:AAHACI0i8OATvyv7BzSCKjmNlZjOmtiFr_k";

        //Add chatId (given chatId is fake)
        String chatId = "-310689220";
        String text = "/calculate " + data;

        urlString = String.format(urlString, apiToken, chatId, text);

        try {
            URL url = new URL(urlString);
            URLConnection conn = url.openConnection();
            InputStream is = new BufferedInputStream(conn.getInputStream());

            BufferedReader br = new BufferedReader(new InputStreamReader(is));
            String inputLine = "";
            StringBuilder sb = new StringBuilder();
            while ((inputLine = br.readLine()) != null) {
                sb.append(inputLine);
            }
            //You can set this String to any TextView
            String response = sb.toString();

            return response;

        } catch (IOException e) {
            e.printStackTrace();
        }

        return "Erro connecting";
    }
}