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

#datos vacunacion
df1=pd.read_csv('vacunas/datos/primera.csv',sep=',').sort_values(by='fecha').set_index('fecha')
df2=pd.read_csv('vacunas/datos/segunda.csv',sep=',').sort_values(by='fecha').set_index('fecha')
#ambas concentraciones de datos tienen distintos etiquetados.
#se replican los ordenes en distintos vectores.
dep_v=['Beni','Chuquisaca','Cochabamba','La Paz','Oruro','Pando','Potosi','Santa Cruz','Tarija']


data1 = df1.iloc[:,:].values.T
data2 = df2.iloc[:,:].values.T

var_v1=np.zeros((9,len(data1[0])))
var_v2=np.zeros((9,len(data2[0])))


for j in range(9):
    var_v1[j,0]=data1[j,0]
    var_v2[j,0]=data2[j,0]
    for i in range(1,len(data1[0])):
        var_v1[j,i]=data1[j,i]-data1[j,i-1]
        var_v2[j,i]=data2[j,i]-data2[j,i-1]       

y_v=df1.index.values       #Se recuperaron los datos de la fuente

v_v1 = df1.rolling(7,min_periods=1).mean()
v_v2 = df2.rolling(7,min_periods=1).mean()

mv_v1 = v_v1.iloc[:,:].values.T   
mv_v2 = v_v2.iloc[:,:].values.T   

mm_v1=np.zeros((9,len(data1[0])))
mm_v2=np.zeros((9,len(data2[0])))

for j in range(9):
    mm_v1[j,0]=mv_v1[j,0]
    mm_v2[j,0]=mv_v2[j,0]
    for i in range(1,len(data1[0])):
        mm_v1[j,i]=mv_v1[j,i]-mv_v1[j,i-1]
        mm_v2[j,i]=mv_v2[j,i]-mv_v2[j,i-1]

        
#====================================
#=           Creador de imagenes      =
#====================================

#Generador de imagenes  VACUNAS

plt.style.use('dark_background')

from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from matplotlib import font_manager as fm, rcParams

fpath = os.path.join(r'MonoLisaSimpson-Regular.ttf')
prop = fm.FontProperties(fname=fpath)
fname = os.path.split(fpath)[1]


bol = mpimg.imread('bol.jpg')
imagebox = OffsetImage(bol,zoom=2)

# These are the "Tableau 20" colors as RGB.    
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)   

# for i in range(len(dep_v)):
#     plt.figure(figsize=(45,38))
#     plt.title('\nVACUNACIONES EN EL DEPARTAMENTO: '+dep_v[i]+'\n(último reporte en fuente: '+y_v[-1]+')\n',fontsize=80,fontproperties=prop)
#     plt.plot(y_v,data1[i],linewidth=15,color=tableau20[0])
#     plt.plot(y_v,data2[i],linewidth=15,color=tableau20[4])
#     plt.xticks(y_v[::7],fontsize=55,rotation=45,fontproperties=prop)
#     plt.ylabel('Vacunados ',fontsize=55,fontproperties=prop)
#     plt.yticks(fontsize=65,fontproperties=prop)
#     plt.ylim(0,np.max(data1[i])+5000)
#     plt.gca().yaxis.grid(linestyle='--',linewidth=0.5,dashes=(5,15))
#     plt.gca().spines["top"].set_visible(False)    
#     plt.gca().spines["bottom"].set_visible(True)    
#     plt.gca().spines["right"].set_visible(False)    
#     plt.gca().spines["left"].set_visible(False)  
#     plt.gca().get_xaxis().tick_bottom()    
#     plt.gca().get_yaxis().tick_left()
#     plt.text(len(data1[0]), data1[i,-1],'1er Dosis',fontsize=65,color=tableau20[0],fontproperties=prop)
#     plt.text(len(data2[0]), data2[i,-1],'2da Dosis',fontsize=65,color=tableau20[4],fontproperties=prop)
#     plt.text(0,30000,"Data source: https://github.com/mauforonda/vacunas"    
#         "\nAutor: Telegram Bot: @Bolivian_Bot"    
#         "\nNota: Histórico acumulado",fontsize=30,fontproperties=prop);
#     plt.savefig('pics/vac'+dep_v[i]+'.png')
#     plt.close()

nacional1=data1[0]+data1[1]+data1[2]+data1[3]+data1[4]+data1[5]+data1[6]+data1[7]+data1[8]
nacional2=data2[0]+data2[1]+data2[2]+data2[3]+data2[4]+data2[5]+data2[6]+data2[7]+data2[8]

op=int(len(nacional1)/1.12)
firma = AnnotationBbox(imagebox,(20,nacional1[op]))

plt.figure(figsize=(45,38))
plt.title('\nVACUNACIÓN A NIVEL NACIONAL\n(último reporte en fuente: '+y_v[-1]+')\n',fontsize=80,fontproperties=prop)
plt.plot(y_v,nacional1,linewidth=15,color=tableau20[0])
plt.plot(y_v,nacional2,linewidth=15,color=tableau20[4])
plt.xticks(y_v[::7],fontsize=55,rotation=45,fontproperties=prop)
plt.ylabel('Vacunados',fontsize=55,fontproperties=prop)
plt.ylim(0,np.max(nacional1))
plt.yticks(fontsize=65,fontproperties=prop)
plt.gca().yaxis.grid(linestyle='--',linewidth=0.5,dashes=(5,15))
plt.gca().spines["top"].set_visible(False)    
plt.gca().spines["bottom"].set_visible(True)    
plt.gca().spines["right"].set_visible(False)    
plt.gca().spines["left"].set_visible(False)  
plt.gca().get_xaxis().tick_bottom()    
plt.gca().get_yaxis().tick_left()
plt.gca().add_artist(firma)
plt.text(len(data1[0]), nacional1[-1],'1er Dosis',fontsize=65,color=tableau20[0],fontproperties=prop)
plt.text(len(data2[0]), nacional2[-1],'2da Dosis',fontsize=65,color=tableau20[4],fontproperties=prop)
plt.text(55,8000,"Data source: https://github.com/mauforonda/vacunas"    
       "\nAutor: Telegram Bot: @Bolivian_Bot"    
       "\nNota: Histórico acumulado",fontsize=30,fontproperties=prop);  
plt.savefig('pics/vacNac.png')
plt.close()
