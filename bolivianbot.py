# ==================================
# =           KungFluBot           =
# ==================================


"""

   Este bot esta pensado para desplegar 
   información respecto a covid19.


"""

#Librerias
import telebot, json
from telebot import types
import numpy as np 

import time, os, sys
sys.path.insert(0, 'core/')


import datos
from datos import *


estados = np.load('core/estados.npy',allow_pickle='TRUE')
fechas = np.load('core/fechas.npy',allow_pickle='TRUE')

       
#Se almacena como clave : valor, el recorrido del usuario en el bot
if(os.path.exists('bins/knownUsers.npy')):
	aux         = np.load('bins/knownUsers.npy', allow_pickle='TRUE') 
	knownUsers  = aux.tolist()
else:
	knownUsers = []
#Registro de usuarios conocidos. Queda realizar una funcion que guarde
#el registro en disco y los vuelva a leer cada vez que el bot inicie






commands = {'start'		:	'Inicia el bot',
            'thanks'	:	'Agradecimientos y referencias',
            'help' 		:	'Información de uso',
            'exec' 		:	'Terminal (Only Admin)'}

#Comandos que el bot contiene para operar. chequear entre las opciones
#que contiene el fatherbot para desplegar los comandos 



_token_='6b697373206d7920617373'



# =======================================
# =           El Menu del bot           =
# = El esqueleto de conformación y una  =
# = clase para imprimir colores en la   = 
# = terminal.                           =
# =======================================



menu = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
menu.add('☢️ Esteriliza con UV','⚠️Facebook leak 🇧🇴','☣️🇧🇴 Info covid19 📈\n última actualización: '+flag_date)

info_menu = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
info_menu.add('📈Reporte Nacional 🇧🇴','📈Reporte por Departamento 📝','🏥 Contactos de emergencia en 🇧🇴','🔙Atrás')

inf_dep = types.ReplyKeyboardMarkup(row_width=5,resize_keyboard=True,one_time_keyboard=False)
inf_dep.add('La Paz','Cochabamba','Santa Cruz','Potosí','Oruro','Pando','Beni','Chuquisaca','Tarija','🔙Atrás')

uv_menu = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=False)
uv_menu.add('Video Informativo','Consejos prácticos','🔙Atrás')

fb_menu = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True,one_time_keyboard=False)
fb_menu.add('👁️', '¿mi número se filtró? 🔎','🔙Atrás')



# ======  End of El Menu del bot  =======


#La función get_user_step, se usa para registrar a un nuevo cliente
#y si este existe en el registro, obtener donde se encuentra en el bot

def get_user_step(uid):
       if uid in userStep:      #Busca si existe la llave uid 
           return userStep[uid] #y retorna el valor almacenado de ubicacion 
       else:
           knownUsers.append(uid)   #En caso de no existir el uid registrado 
           userStep[uid] = 0        #se lo almacena y se inicia su ubicacion en cero
           np.save('bins/knownUsers.npy', knownUsers)   #en cada nuevo registro, actualiza.
           return  userStep[uid]


def jsonKeys2int(x):
    if isinstance(x, dict):
            return {int(k):v for k,v in x.items()}
    return x


def sv():
    with open('bins/userStep.json', 'w') as file:
        json.dump(userStep,file)
            


#La funcion que registra los actos solo en consola servidor
#puede ser en un log sobre las respuestas tambien. En este caso
#para considerar 

def listener(messages):
    for m in messages:
        if m.content_type in ["text", "sticker", "pinned_message", "photo", "audio"] :
            with open('bins/log.txt', 'a') as _log:
                _log.write(str(m.chat.id)+'->'+str(m.chat.username)+':'+str(get_user_step(m.chat.id))+'\n')
            sv()

            

#Inicializamos el bot

#creamos el objeto Telegram Bot
bot = telebot.TeleBot(token)
#asignamos nuestra funcion listener al bot
bot.set_update_listener(listener)


# =======================================
# = Flujo de trabajo y comandos del Bot =
# =======================================


# START
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid in knownUsers:
        userStep[cid] = 0
        bot.send_message(cid, "Hola 👋👋 "+str(m.chat.username)+" que bueno verte nuevamente.",disable_notification= False)
        time.sleep(0.4)
    else:
        bot.send_message(cid, "Hola 👋👋 "+str(m.chat.username)+', te doy la Bienvenida!',disable_notification= False)
        time.sleep(0.3)
        bot.send_message(cid, "Te voy registrando...",disable_notification= True)
        get_user_step(cid);

    bot.send_message(cid, "Iniciando el bot...",disable_notification= True)
    time.sleep(0.1)
    bot.send_message(cid, "🤖  Listo  ✅... \nPor favor use los botones.",reply_markup=menu,disable_notification= True)
	
   # AYUDA
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    userStep[cid] = 0
    help_text = "Hola, este bot muestra los datos covid19 en Bolivia\n"
    help_text += "Tambien despliega información de utilidad que se actualiza diariamente.\n"
    help_text += "Comandos disponibles: \n"
    bot.send_message(cid, help_text,reply_markup=menu)
    for key in commands:
        help_textk = "/" + key + ": "
        help_textk += commands[key] + "\n"
        bot.send_message(cid, help_textk,reply_markup=menu)


# EXEC COMANDO
@bot.message_handler(commands=['exec'])
def command_exec(m):
    cid = m.chat.id
    userStep[cid] = 0
    if cid == master:  # cid del admin!
        bot.send_message(cid, "Ejecutan en consola: " + m.text[len("/exec"):])
        bot.send_chat_action(cid, 'typing')
        time.sleep(1)
        exec_ = os.popen(m.text[len("/exec"):])
        result = exec_.read()
        bot.send_message(cid, "Resultado: " + result,reply_markup=menu)
    else:
        bot.send_message(cid, "PERMISO DENEGADO, solo el Admin puede acceder",reply_markup=menu)
        print(color.RED + " ¡PERMISO DENEGADO! " + color.ENDC)


# thanks COMANDO
@bot.message_handler(commands=['thanks'])
def command_exec(m):
    cid = m.chat.id
    userStep[cid] = 0
    bot.send_chat_action(cid, 'typing')
    about='''Este bot fue construido por Industrias Bot 💪💻 puede contactarse en el siguiente enlace: 
    📲 https://t.me/radiontech \n
    👨‍💻 El repositorio del proyecto se encuentra en: 
    🌐 https://github.com/jpcrespo/covidbotbolivia
    Los datos se actualizan automáticamente cada día a las 00:00, tomando como fuente los siguientes repositorios: 
    🌐   1. https://github.com/mauforonda/vacunas    
    🌐   2. https://github.com/mauforonda/covid19-bolivia
    La base de datos de los números filtrados en Facebook fue gracias a: \n🐦 https://twitter.com/ccuencad'
    Unos capos totales.''' 
    bot.send_message(cid,about,disable_web_page_preview=True)
    bot.send_message(cid,'Puedes invitarme un café ☕\nBTC:\nbc1q8muceqt42f84zcw7gfmdxyxsg7kk9wxcfp7d9e\nADA:\naddr1q8p8s8ewvh7k0c48kp5t09wfhhmnjhr0283p73326m5cfrrvy58pxn65ppndqfwvah966zhm53323tw6ff3kujld43nq6nj8wl')
    bot.send_message(cid,'Menú principal:',reply_markup=menu)






# =========================================================================
# =           Sección de despligue de menus internos y acciones           =
# =========================================================================



# MENU PRINCIPAL
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 0)
def main_menu(m):
    cid = m.chat.id
    text = m.text
    if text == "☢️ Esteriliza con UV":
    	bot.send_message(cid, "Use un método fácil, barato y eficiente de esterilización: Luz UV-C", reply_markup =uv_menu)
    	userStep[cid] = 1
    elif text == "⚠️Facebook leak 🇧🇴":  # CAMARA
        bot.send_message(cid, "Averígue si sus datos fueron comprometidos (solo Bolivia).", reply_markup=fb_menu)
        userStep[cid] = 4

    elif text == '☣️🇧🇴 Info covid19 📈\n última actualización: '+flag_date:
    	  bot.send_message(cid,'Información Actualizada Covid19 en Bolivia')
    	  bot.send_message(cid,'''Los datos de nuevos casos y fallecimientos se obtiene de la web
        🌐	https://paho-covid19-response-who.hub.arcgis.com\nEl sitio oficial del gobierno Nacional no tiene un servicio de datos para monitoreo epidemiológico que entregue data regularmente (dejó de actualizarse regularmente desde Octubre de 2020 y paró completamente el 22 de Noviembre) por lo que se recogen datos de La Organización Panamericana de la Salud (OPS).''',reply_markup=info_menu)
    	  userStep[cid] = 2
    else:
        command_text(m)



# MENU INFO COVID
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def uvmain_menu(m):
    cid = m.chat.id
    txt = m.text
    if txt == "Video Informativo":
    	bot.send_chat_action(cid,'upload_video')
    	bot.send_video(cid, open('bins/video.mp4', 'rb'), supports_streaming=True)
    	bot.send_message(cid,'Si desea asesoramiento no dude en contactar:\nhttps://t.me/radiontech',reply_markup=uv_menu)
    

    elif txt == 'Consejos prácticos':
    	bot.send_chat_action(cid,'typing')
    	time.sleep(1)
    	bot.send_message(cid,datos.getMessage(),reply_markup=uv_menu)


    elif txt == "🔙Atrás":  # HD
        userStep[cid] = 0
        bot.send_message(cid, "Menu Principal:", reply_markup=menu)
    else:
        command_text(m)




# MENU INFO COVID
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def infomain_menu(m):
    cid = m.chat.id
    txt = m.text
    if txt == "📈Reporte Nacional 🇧🇴":
        bot.send_message(cid,'Reporte Nacional díario, última fecha de actualización en la fuente: '+fechas[0])
        bot.send_message(cid, 'Nuevos casos 🤒 '+str(int(np.sum(estados[0])))+
    '\nFallecimientos ⚰️ '+str(int(np.sum(estados[1])))+
    '\nVacunados 1era Dosis 💉 '+str(int(np.sum(estados[2])))+
    '\nVacunados 2da  Dosis 💉 '+str(int(np.sum(estados[3]))))

        bot.send_message(cid,'Reporte díario vacunación, último día actualizado en la fuente: '+fechas[1])
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/ratevacNac.png', 'rb'))
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/covNac.png', 'rb'))
        bot.send_message(cid,'''El 6 de septiembre de 2020 el SEDES Santa Cruz reporta una actualización que incrementa 1570 casos al conteo acumulado de decesos. Según un comunicado del Ministerio de Salud, el incremento es resultado de una revisión retrospectiva de datos y no corresponden al día mencionado.''')
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/vacNac.png', 'rb'),reply_markup=info_menu)

    elif txt == '📈Reporte por Departamento 📝':
    	userStep[cid] = 3
    	bot.send_message(cid,'Se muestran los datos desagregados por cada Departamento',reply_markup=inf_dep)

    elif txt == '🏥 Contactos de emergencia en 🇧🇴':
        bot.send_chat_action(cid,'typing')
        inff= ''' Páginas web del sistema de salud a nivel nacional:
        Caja Petrolera de Salud
        🌐 https://www.cps.org.bo
        Caja Nacional de Salud
        🌐 https://www.cns.gob.bo
        Caja de Salud de la Banca Privada 
        🌐 https://portal.csbp.com.bo
        Caja Nacional de Caminos
        🌐 http://www.cajasaludcaminos.gob.bo
        Caja de Salud Cordes 
        🌐 https://www.sistemacordes.org
        Caja Bancaria Estatal de salud 
        🌐 https://www.cbes.org.bo
        Cossmil 
        🌐 https://www.cossmil.mil.bo/#/inicio
        Seguro Integral de Salud SINEC
        🌐 http://sinec.org.bo
        Seguro Social Universitario
        🌐 http://www.ssulapaz.org
        '''

        bot.send_message(cid,inff,reply_markup=info_menu,disable_web_page_preview=True)


    elif txt == "🔙Atrás":  # HD
        userStep[cid] = 0
        bot.send_message(cid, "Menu Principal:", reply_markup=menu)
    else:
        command_text(m)



@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 3)
def infodep_menu(m):
    cid = m.chat.id
    txt = m.text
    if txt == "La Paz":
      bot.send_message(cid,'Reporte Nacional díario, última fecha de actualización en la fuente: '+fechas[0])
      bot.send_message(cid, 'Nuevos casos 🤒 '+str(int(estados[0,0]))+'\nFallecimientos ⚰️ '+str(int(estados[1,0]))+'\nVacunados 1era Dosis 💉 '+str(int(estados[2,0]))+'\nVacunados 2da  Dosis 💉 '+str(int(estados[3,0])))
      bot.send_message(cid,'Reporte díario vacunación, último día actualizado en la fuente: '+fechas[1])
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/ratevacLa Paz.png', 'rb'))
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/covLa Paz.png', 'rb'))
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/vacLa Paz.png', 'rb'),reply_markup=inf_dep)

    elif txt == 'Cochabamba':
        bot.send_message(cid,'Reporte Nacional díario, última fecha de actualización en la fuente: '+fechas[0])
        bot.send_message(cid, 'Nuevos casos 🤒 '+str(int(estados[0,1]))+
    '\nFallecimientos ⚰️ '+str(int(estados[1,1]))+
    '\nVacunados 1era Dosis 💉 '+str(int(estados[2,1]))+
    '\nVacunados 2da  Dosis 💉 '+str(int(estados[3,1])))
        bot.send_message(cid,'Reporte díario vacunación, último día actualizado en la fuente: '+fechas[1])
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/ratevacCochabamba.png', 'rb'))

        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/covCochabamba.png', 'rb'))

        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/vacCochabamba.png', 'rb'),reply_markup=inf_dep)

    elif txt == 'Santa Cruz':
        bot.send_message(cid,'Reporte Nacional díario, última fecha de actualización en la fuente: '+fechas[0])
     

        bot.send_message(cid, 'Nuevos casos 🤒 '+str(int(estados[0,2]))+
    '\nFallecimientos ⚰️ '+str(int(estados[1,2]))+
    '\nVacunados 1era Dosis 💉 '+str(int(estados[2,2]))+
    '\nVacunados 2da  Dosis 💉 '+str(int(estados[3,2])))
        bot.send_message(cid,'Reporte díario vacunación, último día actualizado en la fuente: '+fechas[1])
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/ratevacSanta Cruz.png', 'rb'))
        
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/covSanta Cruz.png', 'rb'))
        bot.send_message(cid,'''El 6 de septiembre de 2020 el SEDES Santa Cruz reporta una actualización que incrementa 1570 casos al conteo acumulado de decesos. Según un comunicado del Ministerio de Salud, el incremento es resultado de una revisión retrospectiva de datos y no corresponden al día mencionado.''')
   
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/vacSanta Cruz.png', 'rb'),reply_markup=inf_dep)

    elif txt == 'Potosí':
      bot.send_message(cid,'Reporte Nacional díario, última fecha de actualización en la fuente: '+fechas[0])
      bot.send_message(cid, 'Nuevos casos 🤒 '+str(int(estados[0,4]))+'\nFallecimientos ⚰️ '+str(int(estados[1,4]))+'\nVacunados 1era Dosis 💉 '+str(int(estados[2,4]))+'\nVacunados 2da  Dosis 💉 '+str(int(estados[3,4])))
      bot.send_message(cid,'Reporte díario vacunación, último día actualizado en la fuente: '+fechas[1])
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/ratevacPotosí.png', 'rb'))
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/covPotosí.png', 'rb'))
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/vacPotosi.png', 'rb'),reply_markup=inf_dep)

    elif txt == 'Oruro':
      bot.send_message(cid,'Reporte Nacional díario, última fecha de actualización en la fuente: '+fechas[0])
      bot.send_message(cid, 'Nuevos casos 🤒 '+str(int(estados[0,3]))+'\nFallecimientos ⚰️ '+str(int(estados[1,3]))+'\nVacunados 1era Dosis 💉 '+str(int(estados[2,3]))+'\nVacunados 2da  Dosis 💉 '+str(int(estados[3,3])))
      bot.send_message(cid,'Reporte díario vacunación, último día actualizado en la fuente: '+fechas[1])
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/ratevacOruro.png', 'rb'))
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/covOruro.png', 'rb'))
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/vacOruro.png', 'rb'),reply_markup=inf_dep)

    elif txt == 'Pando':
      bot.send_message(cid,'Reporte Nacional díario, última fecha de actualización en la fuente: '+fechas[0])
      bot.send_message(cid, 'Nuevos casos 🤒 '+str(int(estados[0,8]))+'\nFallecimientos ⚰️ '+str(int(estados[1,8]))+'\nVacunados 1era Dosis 💉 '+str(int(estados[2,8]))+'\nVacunados 2da  Dosis 💉 '+str(int(estados[3,8])))
      bot.send_message(cid,'Reporte díario vacunación, último día actualizado en la fuente: '+fechas[1])
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/ratevacPando.png', 'rb'))
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/covPando.png', 'rb'))
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/vacPando.png', 'rb'),reply_markup=inf_dep)

    elif txt == 'Beni':
      bot.send_message(cid,'Reporte Nacional díario, última fecha de actualización en la fuente: '+fechas[0])
      bot.send_message(cid, 'Nuevos casos 🤒 '+str(int(estados[0,7]))+'\nFallecimientos ⚰️ '+str(int(estados[1,7]))+'\nVacunados 1era Dosis 💉 '+str(int(estados[2,7]))+'\nVacunados 2da  Dosis 💉 '+str(int(estados[3,7])))
      bot.send_message(cid,'Reporte díario vacunación, último día actualizado en la fuente: '+fechas[1])
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/ratevac.png', 'rb'))
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/covBeni.png', 'rb'))
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/vacBeni.png', 'rb'),reply_markup=inf_dep)


    elif txt == 'Chuquisaca':
      bot.send_message(cid,'Reporte Nacional díario, última fecha de actualización en la fuente: '+fechas[0])
      bot.send_message(cid, 'Nuevos casos 🤒 '+str(int(estados[0,6]))+'\nFallecimientos ⚰️ '+str(int(estados[1,6]))+'\nVacunados 1era Dosis 💉 '+str(int(estados[2,6]))+'\nVacunados 2da  Dosis 💉 '+str(int(estados[3,6])))
      bot.send_message(cid,'Reporte díario vacunación, último día actualizado en la fuente: '+fechas[1])
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/ratevacChuquisaca.png', 'rb'))
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/covChuquisaca.png', 'rb'))
      bot.send_chat_action(cid,'upload_photo')
      bot.send_photo(cid, open('core/pics/vacChuquisaca.png', 'rb'),reply_markup=inf_dep)

    elif txt == 'Tarija':
        bot.send_message(cid,'Reporte Nacional díario, última fecha de actualización en la fuente: '+fechas[0])
       

        bot.send_message(cid, 'Nuevos casos 🤒 '+str(int(estados[0,5]))+
    '\nFallecimientos ⚰️ '+str(int(estados[1,5]))+
    '\nVacunados 1era Dosis 💉 '+str(int(estados[2,5]))+
    '\nVacunados 2da  Dosis 💉 '+str(int(estados[3,5])))
        bot.send_message(cid,'Reporte díario vacunación, último día actualizado en la fuente: '+fechas[1])
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/ratevacTarija.png', 'rb'))

       
        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/covTarija.png', 'rb'))

        bot.send_chat_action(cid,'upload_photo')
        bot.send_photo(cid, open('core/pics/vacTarija.png', 'rb'),reply_markup=inf_dep)

    elif txt == '🔙Atrás':
        userStep[cid] = 2
        bot.send_message(cid, "Menu Principal:", reply_markup=info_menu)
    else:
        command_text(m)



@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 4)
def fbmain_menu(m):
    cid = m.chat.id
    txt = m.text
    if txt == '👁️':
        bot.send_chat_action(cid,'typing')
        bot.send_message(cid,"En el filtrado de datos de Facebook del 2021 se expusieron casi 3 millones de cuentas Bolivianas, puede buscar si su número se encuentra vulnerable.")
        bot.send_message(cid,'Puede asociar su número con la siguiente información:')
        bot.send_message(cid,'Nombres, apellidos, sexo, ciudad, estado civil, trabajo',reply_markup=fb_menu)
    elif txt == '¿mi número se filtró? 🔎':
        markup = types.ForceReply(selective=False)
        target_n =  bot.send_message(cid,"Ingrese su número 591: ",reply_markup=markup);
        bot.register_next_step_handler(target_n,busqueda)
    elif txt == '🔙Atrás':
        userStep[cid] = 0
        bot.send_message(cid, "Menu Principal:", reply_markup=menu)
        
    else:
        command_text(m)
 
def busqueda(m):
    cid=m.chat.id
    nn=m.text
    if nn.isdigit():
        n1=int(nn)
        n2=59100000000+n1
        _a=np.where(data == n2)
        if(n1>60000000 and n1<79999999):
            bot.send_message(cid,"Revisando en la base . . .🔍️🔍️🔍️")
            if (len(_a[0])==0):
                bot.send_message(cid,"Su número no esta en la filtración ✔️",reply_markup=fb_menu)
            else:
                bot.send_message(cid,"Su número ESTA en la filtración, tenga cuidado ⚠️")
                bot.send_message(cid,"Facebook asociado: https://facebook.com/"+str(fibu[_a[0][0]]),reply_markup=fb_menu)
            
        else:
            bot.send_message(cid,"No es un número de Bolivia o esta mal escrito.",reply_markup=fb_menu)
    
    else:
        bot.send_message(cid,"Dato introducido no válido",reply_markup=fb_menu)
    



# FILTRAR MENSAJES
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_text(m):

	cid = m.chat.id
	if(cid == master or cid == 1164696885):
		userStep[cid]=0
		if(m.text == 'log'):
			with open('bins/log.txt','rb') as lgs:
				userStep[cid]=0
				bot.send_document(master,lgs,reply_markup=menu)
		elif (m.text == 'send_ip'):
			os.popen('ifconfig > ip.txt')
			time.sleep(2)
			with open('ip.txt','rb') as ips:
				bot.send_document(master,ips,reply_markup=menu)
	elif(m.text.lower() in ['hola', 'hi', 'buenas', 'buenos dias']):
		userStep[cid] = 0
		bot.send_message(cid, 'Muy buenas, ' + str(m.from_user.first_name) + '. Me alegra verte de nuevo.', reply_markup=menu)
	elif (m.text.lower() in ['adios', 'aios', 'adeu', 'ciao','chau','bye']):
		UserStep[cid] = 0
		bot.send_message(cid, 'Hasta luego, ' + str(m.from_user.first_name) + '. Te echaré de menos.', reply_markup=menu)
	elif (m.text in ['La Paz','Cochabamba','Santa Cruz','Potosí','Oruro','Pando','Beni','Chuquisaca','Tarija',"🔙Atrás","📈Reporte Nacional 🇧🇴",'📈Reporte por Departamento 📝','🏥 Contactos de emergencia en 🇧🇴',"☢️ Esteriliza con UV", "⚠️Facebook leak 🇧🇴",'☣️🇧🇴 Info covid19 📈\n última actualización: '+flag_date,'Video Informativo','Consejos prácticos', '¿mi número se filtró? 🔎']):
		userStep[cid] = 0
		bot.send_message(cid, ' ',reply_markup=menu)
	elif (m.content_type in ["text", "sticker", "pinned_message", "photo", "audio"]):
		userStep[cid] = 0
		bot.send_message(cid,'🤔',reply_markup=menu)




def main_loop():
    print('Corriendo...')
    bot.polling(True)


if __name__ == '__main__':
    data = np.load('bins/bd_tb.npy',allow_pickle=True)
    fibu = np.load('bins/fibu.npy',allow_pickle=True)

#recuerda el último punto de ubicación de cada usuario para mantener un flujo
#continuo en la experiencia de usuario, ante cada actualización del bot
#pues se pone en espera y recompila las imagenes antes de poner de nuevo el bot a operar

    if(os.path.exists('bins/userStep.json')):
        with open('bins/userStep.json','r') as filex:
            userStep=json.load(filex,object_hook=jsonKeys2int) 
    else:
        userStep = {}  

    try:
        main_loop()
    
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)




