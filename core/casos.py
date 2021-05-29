
import os,sys
import pandas as pd
import numpy as np
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)      
import matplotlib.pyplot as plt

_n=115.131 
#datos casos diarios
df3=pd.read_csv('covid19-bolivia/confirmados.csv',sep=',').sort_values(by='Fecha').set_index('Fecha')
df4=pd.read_csv('covid19-bolivia/decesos.csv',sep=',').sort_values(by='Fecha').set_index('Fecha')


#ambas concentraciones de datos tienen distintos etiquetados.
#se replican los ordenes en distintos vectores.
dep_c=['La Paz','Cochabamba','Santa Cruz','Oruro','Potosí','Tarija','Chuquisaca','Beni','Pando']
c_dep = _n*(1/100)*np.array([27.03,17.52,26.42,4.92,8.23,4.81,5.78,4.19,1.10])  #el porcentaje
                                                                                    #que corresponde 

data3 = df3.iloc[:,:].values.T
data4 = df4.iloc[:,:].values.T

var_c=np.zeros((9,len(data3[0])))  #creamos una nueva variable 
var_m=np.zeros((9,len(data4[0])))  #iniciada en 0

for j in range(9):
    var_c[j,0]=data3[j,0]/c_dep[j]  #El primer dato es igual a los nuevos casos
    var_m[j,0]=data4[j,0]/c_dep[j]  #dando el inicio del acumulado
    for i in range(1,len(data3[0])):
        var_c[j,i]=(data3[j,i]-data3[j,i-1])/c_dep[j]
        var_m[j,i]=(data4[j,i]-data4[j,i-1])/c_dep[j]

y_c=df3.index.values       #con el indice dado por las fechas del reporte

mean_df_c = df3.rolling(7,min_periods=1).mean()
mean_df_m = df4.rolling(7,min_periods=1).mean()

mean_dc = mean_df_c.iloc[:,:].values.T  
mean_dm = mean_df_m.iloc[:,:].values.T 

var_mc=np.zeros((9,len(mean_dc[0])))
var_mm=np.zeros((9,len(mean_dm[0])))

for j in range(9):
    var_mc[j,0]=(mean_dc[j,0]/c_dep[j])
    var_mm[j,0]=(mean_dc[j,0]/c_dep[j])
    for i in range(1,len(data3[0])):
        var_mc[j,i]=(mean_dc[j,i]-mean_dc[j,i-1])/c_dep[j]
        var_mm[j,i]=(mean_dm[j,i]-mean_dm[j,i-1])/c_dep[j]

# plt.style.use('dark_background')

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

<<<<<<< HEAD
for i in range(1): #len(dep_c)):
    plt.figure(figsize=(90,60))
    plt.title('NUEVOS CASOS/DÍA POR 100\'000 HAB EN EL DEPARTAMENTO: '+dep_c[i]+'\n(último reporte en fuente: '+y_c[-1]+')\n',fontsize=150,fontproperties=prop)
    plt.plot(y_c,var_c[i],label='Nuevos Casos/día',linewidth=5,color=tableau20[0],linestyle='-',marker='.', markersize=15,markeredgecolor='red',markerfacecolor='r')
    plt.plot(y_c,var_mc[i],label='Promedio 7 días',linewidth=15,color=tableau20[1],linestyle='-')
    plt.plot(y_c,var_m[i],label='Fallecimientos/día',linewidth=15,color=tableau20[7],linestyle='-')
    plt.legend(loc='upper left',fontsize=80)
    plt.yticks(fontsize=100,fontproperties=prop)
    plt.xticks(y_c[::28],fontsize=80,rotation=45,fontproperties=prop)
=======
for i in range(len(dep_c)):
    fig = plt.figure(figsize=(35,25))
    #Color del fondo
    fig.patch.set_facecolor(tableau20[0])
    plt.axes().patch.set_facecolor(tableau20[0])
    plt.subplots_adjust(top=0.80)
    plt.title('NUEVOS CASOS/DÍA POR 100\'000 HAB EN EL DEPARTAMENTO:\n'+dep_c[i]+'\n(último reporte en fuente: '+y_c[-1]+')\n',fontsize=65,fontproperties=prop,color=tableau20[1])
    plt.plot(y_c,var_c[i],label='Nuevos Casos/día',linewidth=5,color=tableau20[2],linestyle='-',marker='.', markersize=15,markeredgecolor='yellow',markerfacecolor='r')
    plt.plot(y_c,var_mc[i],label='Promedio 7 días',linewidth=5,color=tableau20[3],linestyle='-')
    plt.plot(y_c,var_m[i],label='Fallecimientos/día',linewidth=5,color=tableau20[4],linestyle='-')
    plt.legend(loc='upper left',fontsize=50)
    plt.yticks(fontsize=50,fontproperties=prop,color=tableau20[1])
    plt.xticks(y_c[::28],fontsize=35,rotation=45,fontproperties=prop,color=tableau20[1])
>>>>>>> d10c5ea380422d7434777954834b851b03200933
    plt.ylim(0,2*np.max(var_mc[i]))  
    plt.ylabel('Casos/día',fontsize=60,fontproperties=prop,color=tableau20[1])
    plt.gca().yaxis.grid(linestyle='--',linewidth=1,dashes=(5,15))
    plt.gca().spines["top"].set_visible(False)    
    plt.gca().spines["bottom"].set_visible(True)    
    plt.gca().spines["right"].set_visible(False)    
    plt.gca().spines["left"].set_visible(False)  
    plt.gca().get_xaxis().tick_bottom()    
    plt.gca().get_yaxis().tick_left()
    plt.subplots_adjust(bottom=0.2)
    plt.text(0,-13,"Data source: https://github.com/mauforonda/covid19-bolivia"    
       "\nAutor: Telegram Bot: @Bolivian_Bot"    
       "\nNota: Histórico acumulado",fontsize=35,fontproperties=prop,color=tableau20[1]);
    plt.savefig('pics/cov'+dep_c[i]+'.png')
    plt.close(fig)

