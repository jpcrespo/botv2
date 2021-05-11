import os,sys
import pandas as pd
import numpy as np
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)      
import matplotlib.pyplot as plt

_n=1151.31 # factor de correción para llevar a 10^4 hab
c_dep = [26.99,17.53,26.48,4.93,8.21,4.81,5.76,4.20,8.21]

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
    var_v1[j,0]=data1[j,0]/(_n*c_dep[j])
    var_v2[j,0]=data2[j,0]/(_n*c_dep[j])
    for i in range(1,len(data1[0])):
        var_v1[j,i]=(data1[j,i]-data1[j,i-1])/(_n*c_dep[j])
        var_v2[j,i]=(data2[j,i]-data2[j,i-1])/(_n*c_dep[j])       
        
y_v=df1.index.values       #Se recuperaron los datos de la fuente

v_v1 = df1.rolling(7,min_periods=1).mean()
v_v2 = df2.rolling(7,min_periods=1).mean()
mv_v1 = v_v1.iloc[:,:].values.T   
mv_v2 = v_v2.iloc[:,:].values.T   


mm_v1=np.zeros((9,len(data1[0])))
mm_v2=np.zeros((9,len(data2[0])))


for j in range(9):
    mm_v1[j,0]=mv_v1[j,0]/(_n*c_dep[j])
    mm_v2[j,0]=mv_v2[j,0]/(_n*c_dep[j])
    for i in range(1,len(data1[0])):
        mm_v1[j,i]=(mv_v1[j,i]-mv_v1[j,i-1])/(_n*c_dep[j])
        mm_v2[j,i]=(mv_v2[j,i]-mv_v2[j,i-1])/(_n*c_dep[j])

plt.style.use('dark_background')

from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from matplotlib import font_manager as fm, rcParams

fpath = os.path.join(r'MonoLisaSimpson-Regular.ttf')
prop = fm.FontProperties(fname=fpath)
fname = os.path.split(fpath)[1]


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



for i in range(len(dep_v)):
    plt.figure(figsize=(90,60))
    plt.title('TASA DE VACUNACIÓN CADA 10\'000 HAB EN EL DEPARTAMENTO: '+dep_v[i]+'\n(último reporte en fuente: '+y_v[-1]+')\n',fontsize=150,fontproperties=prop)
    plt.plot(y_v,mm_v1[i],label='Promedio 7 días',linewidth=15,color=tableau20[1],linestyle='-')
    plt.plot(y_v,mm_v2[i],label='Promedio 7 días',linewidth=15,color=tableau20[5],linestyle='-')
    plt.xticks(y_v[::7],fontsize=80,rotation=45,fontproperties=prop)
    plt.ylabel('Vacunados/día',fontsize=85,fontproperties=prop)
    plt.yticks(fontsize=65,fontproperties=prop)
    plt.ylim(0,np.max(mm_v1[i]))
    plt.gca().yaxis.grid(linestyle='--',linewidth=3,dashes=(5,15))
    plt.gca().spines["top"].set_visible(False)    
    plt.gca().spines["bottom"].set_visible(True)    
    plt.gca().spines["right"].set_visible(False)    
    plt.gca().spines["left"].set_visible(False)  
    plt.gca().get_xaxis().tick_bottom()    
    plt.gca().get_yaxis().tick_left()
    plt.text(len(data1[0]), mm_v1[i,-1],'1er Dosis',fontsize=85,color=tableau20[0])
    plt.text(len(data2[0]), mm_v2[i,-1],'2da Dosis',fontsize=85,color=tableau20[4])
    plt.text(0,np.max(mm_v1[i])/2,"Data source: https://github.com/mauforonda/vacunas"    
         "\nAutor: Telegram Bot: @Bolivian_Bot"    
         "\nNota: Histórico acumulado", fontsize=50,fontproperties=prop)  
    plt.savefig('pics/ratevac'+dep_v[i]+'.png')
    plt.close()

