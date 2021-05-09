import os,sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df1=pd.read_csv('vacunas/datos/primera.csv',sep=',').sort_values(by='fecha').set_index('fecha')
df2=pd.read_csv('vacunas/datos/segunda.csv',sep=',').sort_values(by='fecha').set_index('fecha')

departamentos_v=['Beni','Chuquisaca','Cochabamba','La Paz','Oruro','Pando','Potosi','Santa Cruz','Tarija']

data1 = df1.iloc[:,:].values.T
data2 = df2.iloc[:,:].values.T

# En el caso de la presentación de datos del Nacional
# se plantea obtener los nuevos casos diarios. Igual que en
# vacunaciones pero solo para obtener la última actualización del día.
var_v1=np.zeros((9,len(data1[0])))
var_v2=np.zeros((9,len(data2[0])))


for j in range(9):
    var_v1[j,0]=data1[j,0]
    var_v2[j,0]=data2[j,0]
    for i in range(1,len(data1[0])):
        var_v1[j,i]=data1[j,i]-data1[j,i-1]
        var_v2[j,i]=data2[j,i]-data2[j,i-1]
        
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
        

y_v=df1.index.values       #Para los gráficos de las vacunas
departamentos_v=['Beni','Chuquisaca','Cochabamba','La Paz','Oruro','Pando','Potosi','Santa Cruz','Tarija']


#Generador de imagenes  VACUNAS

import os
from matplotlib import font_manager as fm, rcParams

fpath = os.path.join(r'C:\Users\xaxe_\AppData\Local\Microsoft\Windows\Fonts\MonolisaSimpson-Regular.ttf')
prop = fm.FontProperties(fname=fpath)
fname = os.path.split(fpath)[1]

plt.style.use('dark_background')

from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

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

for i in range(len(departamentos_v)):
    plt.figure(figsize=(20,15))
    plt.title('Tasa de Vacunación en el Departamento: '+departamentos_v[i]+'\n(último reporte en fuente: '+y_v[-1]+')\n',fontsize=35)

    plt.plot(y_v,var_v1[i],label='Nuevos Casos/día',linewidth=0.5,color=tableau20[0],linestyle='-',marker='.', markersize=5,markeredgecolor='red',markerfacecolor='r')
    plt.plot(y_v,var_v2[i],label='Nuevos Casos/día',linewidth=0.5,color=tableau20[5],linestyle='-',marker='.', markersize=7,markeredgecolor='green',markerfacecolor='r')
    plt.plot(y_v,mm_v1[i],label='Promedio 7 días',linewidth=5,color=tableau20[1],linestyle='-')
    plt.plot(y_v,mm_v2[i],label='Promedio 7 días',linewidth=5,color=tableau20[5],linestyle='-')
    plt.xticks(y_v[::7],fontsize=15,rotation=45)
    plt.ylabel('Vacunados/día',fontsize=20)
    plt.yticks(fontsize=20)
    plt.ylim(0,np.max(var_v1[i]))
    plt.gca().yaxis.grid(linestyle='--',linewidth=0.5,dashes=(5,15))
    plt.gca().spines["top"].set_visible(False)    
    plt.gca().spines["bottom"].set_visible(True)    
    plt.gca().spines["right"].set_visible(False)    
    plt.gca().spines["left"].set_visible(False)  
    plt.gca().get_xaxis().tick_bottom()    
    plt.gca().get_yaxis().tick_left()
    plt.text(len(data1[0]), mm_v1[i,-1],'1er Dosis',fontsize=20,color=tableau20[0])
    plt.text(len(data2[0]), mm_v2[i,-1],'2da Dosis',fontsize=20,color=tableau20[4])
    plt.text(0,2500,"Data source: https://github.com/mauforonda/vacunas"    
         "\nAutor: Telegram Bot: @Bolivian_Bot"    
         "\nNota: Histórico acumulado", fontsize=12)  
    #plt.savefig('pics/vac'+departamentos_v[i]+'.png')

nac_v1 = mm_v2[0]+mm_v1[1]+mm_v1[2]+mm_v1[3]+mm_v1[4]+mm_v1[5]+mm_v1[6]+mm_v1[7]+mm_v1[8]
nac_v2 = mm_v2[0]+mm_v2[1]+mm_v2[2]+mm_v2[3]+mm_v2[4]+mm_v2[5]+mm_v2[6]+mm_v2[7]+mm_v2[8]


plt.figure(figsize=(40,20))
plt.title('\nTasa de Vacunación Nacional.'+'\n(último reporte en fuente: '+y_v[-1]+')\n',fontsize=75,fontproperties=prop,color='yellow')
plt.plot(y_v,nac_v1,label='Promedio de 7 días - 1 Dosis',linewidth=5,color=tableau20[1],linestyle='-')
plt.plot(y_v,nac_v2,label='Promedio de 7 días - 2 Dosis',linewidth=5,color=tableau20[5],linestyle='-')
plt.xticks(y_v[::7],fontsize=35,rotation=45,fontproperties=prop)
plt.ylabel('\nVacunados/día\n',fontsize=40,fontproperties=prop)
plt.yticks(fontsize=35,fontproperties=prop)
plt.ylim(0,np.max(nac_v1))
plt.gca().yaxis.grid(linestyle='--',linewidth=0.5,dashes=(5,15))
plt.gca().spines["top"].set_visible(False)    
plt.gca().spines["bottom"].set_visible(True)    
plt.gca().spines["right"].set_visible(False)    
plt.gca().spines["left"].set_visible(False)  
plt.gca().get_xaxis().tick_bottom()    
plt.gca().get_yaxis().tick_left()

plt.text(len(y_v)-4, nac_v1[-1]+200,'1er Dosis',fontsize=35,color=tableau20[1],fontproperties=prop)
plt.text(len(y_v)-4, nac_v2[-1]+200,'2da Dosis',fontsize=35,color=tableau20[5],fontproperties=prop)
plt.text(0,10000,"Data source: https://github.com/mauforonda/vacunas"    
         "\nAutor: @Bolivian_Bot Telegram"    
         "\nNota: Histórico acumulado.", fontsize=20,fontproperties=prop);  
plt.savefig('vacu.png',bbox_inches='tight')



