"""
En este script se construyen desde las gráficas de los indicadores
a partir de los datos primarios.

Se intentan construir 3 indicadores que sean de utilidad a partir 
de los siguientes datos:
1. Acumulado diario de casos. La fuente reporta el acumulado de casos desde
el inicio de reportes. No se reporta los activos, recuperados. (inicialmente si lo hacian)
2. Descesos diarios.
3. Vacunas acumuladas diariamente.
Indicadores:
1. tasa de casos nuevos por día, se podría identificar las olas.
-> tasa de fallecimientos nuevos por día, podría identificar el saturamiento
del sistema de salud si llega a converger con la tasa de nuevos por día.
    Se muestran en el mismo gráfico para poder hacer la comparativa.
2. Curva de vacunación acumulada. Estas podrían ser buen indicador de metas 
donde faltaria sumar la información  obtjetivo.

3. Tasa de vacunación diaría. Permitiria ver el avance en las campanhas de
vacunación.  

"""

import os,sys
import pandas as pd
import numpy as np
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)      
import matplotlib.pyplot as plt



_n=1151.31

#datos vacunacion
df1=pd.read_csv('vacunas/datos/primera.csv',sep=',').sort_values(by='fecha').set_index('fecha').fillna(0)
df2=pd.read_csv('vacunas/datos/segunda.csv',sep=',').sort_values(by='fecha').set_index('fecha').fillna(0)
#ambas concentraciones de datos tienen distintos etiquetados.
#se replican los ordenes en distintos vectores.
dep_v=['Beni','Chuquisaca','Cochabamba','La Paz','Oruro','Pando','Potosi','Santa Cruz','Tarija']


data1 = df1.iloc[:,:].values.T/_n
data2 = df2.iloc[:,:].values.T/_n


y_v=df1.index.values       #Se recuperaron los datos de la fuente


        
#====================================
#=           Creador de imagenes      =
#====================================

#Generador de imagenes  VACUNAS



from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from matplotlib import font_manager as fm, rcParams

fpath = os.path.join(r'MonoLisaSimpson-Regular.ttf')
prop = fm.FontProperties(fname=fpath)
fname = os.path.split(fpath)[1]



# These are the "Tableau 20" colors as RGB.    
tableau20 = [(48,48,48), (240,240,240), (59,170,6), (61,167,249),    
             (230,0,0)]    

             #1[0] fondo plomo
             #2    blanco de titulos
             #3    rojo neon puntos
             #4    verdes
             #5    celestes   
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)   

nacional1=data1[0]+data1[1]+data1[2]+data1[3]+data1[4]+data1[5]+data1[6]+data1[7]+data1[8]
nacional2=data2[0]+data2[1]+data2[2]+data2[3]+data2[4]+data2[5]+data2[6]+data2[7]+data2[8]


fig = plt.figure(figsize=(35,25))

#Color del fondo
fig.patch.set_facecolor(tableau20[0])
plt.axes().patch.set_facecolor(tableau20[0])
plt.subplots_adjust(top=0.80)
plt.title('\nVacunación a nível Nacional cada 10\'000 HAB\n(último reporte en fuente: '+y_v[-1]+')\n',fontsize=75,fontproperties=prop,color=tableau20[1])
plt.plot(y_v,nacional1,linewidth=5,color=tableau20[3])
plt.plot(y_v,nacional2,linewidth=5,color=tableau20[2])
plt.xticks(y_v[::7],fontsize=50,rotation=45,fontproperties=prop,color=tableau20[1])
plt.ylabel('\nVacunados\n',fontsize=60,fontproperties=prop,color=tableau20[1])
#plt.ylim(0,np.max(nacional1))
plt.yticks(fontsize=50,fontproperties=prop,color=tableau20[1])
plt.gca().yaxis.grid(linestyle='--',linewidth=0.5,dashes=(5,15))
plt.gca().spines["top"].set_visible(False)    
plt.gca().spines["bottom"].set_visible(True)    
plt.gca().spines["right"].set_visible(False)    
plt.gca().spines["left"].set_visible(False)  
plt.gca().get_xaxis().tick_bottom()    
plt.gca().get_yaxis().tick_left()



bol = mpimg.imread('bol.jpg')
imagebox = OffsetImage(bol,zoom=1)
firma = AnnotationBbox(imagebox,(len(y_v)/2,np.max(nacional1)))


plt.gca().add_artist(firma)
plt.subplots_adjust(bottom=0.3)
plt.text(len(data1[0]), nacional1[-1],'1er Dosis',fontsize=35,color=tableau20[3],fontproperties=prop)
plt.text(len(data2[0]), nacional2[-1],'2da Dosis',fontsize=35,color=tableau20[2],fontproperties=prop)
plt.text(0,-2*np.mean(nacional1),"Data source: https://github.com/mauforonda/vacunas"    
       "\nAutor: Telegram Bot: @Bolivian_Bot"    
       "\nNota: Histórico acumulado",fontsize=35,fontproperties=prop,color=tableau20[1]);  
plt.savefig('pics/vacNac.png')
plt.close()
