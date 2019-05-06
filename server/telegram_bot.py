import pulp
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from planes import *
from dp import *
from lo import *

cnt_planes = len(planes)


TOKEN = '747519216:AAHACI0i8OATvyv7BzSCKjmNlZjOmtiFr_k'



def get_sol(plan_list, limit_voice, limit_sms, limit_data):

    #result = get_solution_ga(plan_list, limit_voice, limit_sms, limit_data)
    result = get_solution_lo(plan_list, limit_voice, limit_sms, limit_data)
   
    return result
    

    
def get_plan(idx):
    msg = ''
    if planes[idx].voice != 0:
        msg += str(planes[idx].voice) + ' minutos de Voz'
    if planes[idx].sms != 0:
        msg += str(planes[idx].sms) + ' mensajes'
    if planes[idx].data != 0:
        msg += str(planes[idx].data) + ' mg de datos'
    return msg
    

def calculate(bot, update):
    chat_id = update.message.chat_id
    print(chat_id)
    msg = update.message.text
    msg = msg.split()
    print(msg)
    V = None
    S = None
    D = None
    try:
        V = int(msg[1])
        S = int(msg[2])
        D = int(msg[3])
    except:
        update.message.reply_text('Datos incorrectos')
        return
    print(V, S, D)
    sol = get_sol(planes, V, S, D)
    print(sol)
    res = 'Usted deberia comprar los siguiente planes \n'
    for i in range(sol):
        if int(sol[i]) != 0:
            #print(sol[i])
            res += str(int(sol[i])) 
            res += ( ' Plan de ' if int(sol[i]) == 1 else ' Planes de ' ) + i + '\n'
            #print(sol[i])
    print(res)
    update.message.reply_text(res)
    
    

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('calculate', calculate))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()