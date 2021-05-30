import os,sys
import pandas as pd
import numpy as np
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)      
import matplotlib.pyplot as plt

_n=115.131 # factor de correción para llevar a 10^4 hab

#datos vacunacion
df1=pd.read_csv('vacunas/datos/primera.csv',sep=',').sort_values(by='fecha').set_index('fecha')
df2=pd.read_csv('vacunas/datos/segunda.csv',sep=',').sort_values(by='fecha').set_index('fecha')

#ambas concentraciones de datos tienen distintos etiquetados.
#se replican los ordenes en distintos vectores.
dep_v=['Beni','Chuquisaca','Cochabamba','La Paz','Oruro','Pando','Potosi','Santa Cruz','Tarija']
c_dep = _n*(1/100)*np.array([4.19,5.78,17.52,27.03,4.92,1.10,8.23,26.42,4.81])  #el porcentaje

data1 = df1.iloc[:,:].values.T
data2 = df2.iloc[:,:].values.T

var_v1=np.zeros((9,len(data1[0])))
var_v2=np.zeros((9,len(data2[0])))

for j in range(9):
    var_v1[j,0]=data1[j,0]/c_dep[j]
    var_v2[j,0]=data2[j,0]/c_dep[j]
    for i in range(1,len(data1[0])):
        var_v1[j,i]=(data1[j,i]-data1[j,i-1])/c_dep[j]
        var_v2[j,i]=(data2[j,i]-data2[j,i-1])/c_dep[j]       
        
y_v=df1.index.values       #Se recuperaron los datos de la fuente

v_v1 = df1.rolling(7,min_periods=1).mean()
v_v2 = df2.rolling(7,min_periods=1).mean()
mv_v1 = v_v1.iloc[:,:].values.T   
mv_v2 = v_v2.iloc[:,:].values.T   


mm_v1=np.zeros((9,len(data1[0])))
mm_v2=np.zeros((9,len(data2[0])))


for j in range(9):
    mm_v1[j,0]=mv_v1[j,0]/(_n*c_dep[j]/100)
    mm_v2[j,0]=mv_v2[j,0]/(_n*c_dep[j]/100)
    for i in range(1,len(data1[0])):
        mm_v1[j,i]=(mv_v1[j,i]-mv_v1[j,i-1])/(_n*c_dep[j]/100)
        mm_v2[j,i]=(mv_v2[j,i]-mv_v2[j,i-1])/(_n*c_dep[j]/100)




from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from matplotlib import font_manager as fm, rcParams

fpath = os.path.join(r'MonoLisaSimpson-Regular.ttf')
prop = fm.FontProperties(fname=fpath)
fname = os.path.split(fpath)[1]


# These are the "Tableau 20" colors as RGB.    
tableau20 = [(48,48,48), (240,240,240), (59,170,6), (61,167,249),    
             (230,0,0)]    
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)   



for i in range(len(dep_v)):
    fig = plt.figure(figsize=(35,25))
    #Color del fondo
    fig.patch.set_facecolor(tableau20[0])
    plt.axes().patch.set_facecolor(tableau20[0])
    plt.subplots_adjust(top=0.78)
    plt.title('TASA DE VACUNACIÓN CADA 100\'000 HAB EN EL DEP:\n'+dep_v[i]+'\n(último reporte en fuente: '+y_v[-1]+')\n',fontsize=75,fontproperties=prop,color=tableau20[1])
    plt.plot(y_v,mm_v1[i],label='Promedio 7 días',linewidth=5,color=tableau20[3],linestyle='-')
    plt.plot(y_v,mm_v2[i],label='Promedio 7 días',linewidth=5,color=tableau20[2],linestyle='-')
    plt.xticks(y_v[::7],fontsize=50,rotation=45,fontproperties=prop,color=tableau20[1])
    plt.ylabel('\nVacunados/día\n',fontsize=60,fontproperties=prop,color=tableau20[1])
    plt.yticks(fontsize=50,fontproperties=prop,color=tableau20[1])
    #plt.ylim(0,np.max(mm_v1[i]))
    plt.gca().yaxis.grid(linestyle='--',linewidth=1,dashes=(5,15))
    plt.gca().spines["top"].set_visible(False)    
    plt.gca().spines["bottom"].set_visible(True)    
    plt.gca().spines["right"].set_visible(False)    
    plt.gca().spines["left"].set_visible(False)  
    plt.gca().get_xaxis().tick_bottom()    
    plt.gca().get_yaxis().tick_left()
    plt.subplots_adjust(bottom=0.3)
    plt.text(len(data1[0]), mm_v1[i,-1],'1er Dosis',fontsize=35,color=tableau20[3])
    plt.text(len(data2[0]), mm_v2[i,-1],'2da Dosis',fontsize=35,color=tableau20[2])
    plt.text(0,-180,"Data source: https://github.com/mauforonda/vacunas"    
         "\nAutor: Telegram Bot: @Bolivian_Bot"    
         "\nNota: Histórico acumulado", fontsize=50,fontproperties=prop,color=tableau20[1])  
    plt.savefig('pics/ratevac'+dep_v[i]+'.png')
    plt.close()

