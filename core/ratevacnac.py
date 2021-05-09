import os,sys
import pandas as pd
import numpy as np
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)      
import matplotlib.pyplot as plt


#datos vacunacion
df1=pd.read_csv('vacunas/datos/primera.csv',sep=',').sort_values(by='fecha').set_index('fecha')
df2=pd.read_csv('vacunas/datos/segunda.csv',sep=',').sort_values(by='fecha').set_index('fecha')
df3=pd.read_csv('covid19-bolivia/confirmados.csv',sep=',').sort_values(by='Fecha').set_index('Fecha')
df4=pd.read_csv('covid19-bolivia/decesos.csv',sep=',').sort_values(by='Fecha').set_index('Fecha')


#ambas concentraciones de datos tienen distintos etiquetados.
#se replican los ordenes en distintos vectores.
dep_v=['Beni','Chuquisaca','Cochabamba','La Paz','Oruro','Pando','Potosi','Santa Cruz','Tarija']

data1 = df1.iloc[:,:].values.T
data2 = df2.iloc[:,:].values.T
data3 = df3.iloc[:,:].values.T
data4 = df4.iloc[:,:].values.T

var_v1=np.zeros((9,len(data1[0])))
var_v2=np.zeros((9,len(data2[0])))

for j in range(9):
    var_v1[j,0]=data1[j,0]
    var_v2[j,0]=data2[j,0]
    for i in range(1,len(data1[0])):
        var_v1[j,i]=data1[j,i]-data1[j,i-1]
        var_v2[j,i]=data2[j,i]-data2[j,i-1]       
        
y_v=df1.index.values       #Se recuperaron los datos de la fuente
y_c=df3.index.values       #con el indice dado por las fechas del reporte



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
#     plt.title('TASA DE VACUNACIÓN EN EL DEPARTAMENTO: '+dep_v[i]+'\n(último reporte en fuente: '+y_v[-1]+')\n',fontsize=80,fontproperties=prop)
#     plt.plot(y_v,mm_v1[i],label='Promedio 7 días',linewidth=15,color=tableau20[1],linestyle='-')
#     plt.plot(y_v,mm_v2[i],label='Promedio 7 días',linewidth=15,color=tableau20[5],linestyle='-')
#     plt.xticks(y_v[::7],fontsize=55,rotation=45,fontproperties=prop)
#     plt.ylabel('Vacunados/día',fontsize=55,fontproperties=prop)
#     plt.yticks(fontsize=65,fontproperties=prop)
#     plt.ylim(0,np.max(mm_v1[i]))
#     plt.gca().yaxis.grid(linestyle='--',linewidth=0.5,dashes=(5,15))
#     plt.gca().spines["top"].set_visible(False)    
#     plt.gca().spines["bottom"].set_visible(True)    
#     plt.gca().spines["right"].set_visible(False)    
#     plt.gca().spines["left"].set_visible(False)  
#     plt.gca().get_xaxis().tick_bottom()    
#     plt.gca().get_yaxis().tick_left()
#     plt.text(len(data1[0]), mm_v1[i,-1],'1er Dosis',fontsize=65,color=tableau20[0])
#     plt.text(len(data2[0]), mm_v2[i,-1],'2da Dosis',fontsize=65,color=tableau20[4])
#     plt.text(0,np.max(mm_v1[i])/2,"Data source: https://github.com/mauforonda/vacunas"    
#          "\nAutor: Telegram Bot: @Bolivian_Bot"    
#          "\nNota: Histórico acumulado", fontsize=30)  
#     plt.savefig('pics/ratevac'+dep_v[i]+'.png')
#     plt.close()

nac_v1 = mm_v2[0]+mm_v1[1]+mm_v1[2]+mm_v1[3]+mm_v1[4]+mm_v1[5]+mm_v1[6]+mm_v1[7]+mm_v1[8]
nac_v2 = mm_v2[0]+mm_v2[1]+mm_v2[2]+mm_v2[3]+mm_v2[4]+mm_v2[5]+mm_v2[6]+mm_v2[7]+mm_v2[8]

bol2 = mpimg.imread('bol.jpg')
imagebox2 = OffsetImage(bol2,zoom=2)
firma2 = AnnotationBbox(imagebox2,(10,np.max(nac_v1)/1.7))

plt.figure(figsize=(45,38))
plt.title('\nTasa de Vacunación Nacional.'+'\n(último reporte en fuente: '+y_v[-1]+')\n',fontsize=75,fontproperties=prop)
plt.plot(y_v,nac_v1,label='Promedio de 7 días - 1 Dosis',linewidth=15,color=tableau20[1],linestyle='-')
plt.plot(y_v,nac_v2,label='Promedio de 7 días - 2 Dosis',linewidth=15,color=tableau20[5],linestyle='-')
plt.xticks(y_v[::7],fontsize=55,rotation=45,fontproperties=prop)
plt.ylabel('\nVacunados/día\n',fontsize=55,fontproperties=prop)
plt.yticks(fontsize=65,fontproperties=prop)
plt.ylim(0,np.max(nac_v1))
plt.gca().yaxis.grid(linestyle='--',linewidth=0.5,dashes=(5,15))
plt.gca().spines["top"].set_visible(False)    
plt.gca().spines["bottom"].set_visible(True)    
plt.gca().spines["right"].set_visible(False)    
plt.gca().spines["left"].set_visible(False)  
plt.gca().get_xaxis().tick_bottom()    
plt.gca().get_yaxis().tick_left()
plt.gca().add_artist(firma2)
plt.text(len(y_v)-4, nac_v1[-1]+1000,'1er Dosis',fontsize=65,color=tableau20[1],fontproperties=prop)
plt.text(len(y_v)-4, nac_v2[-1]+1000,'2da Dosis',fontsize=65,color=tableau20[5],fontproperties=prop)
plt.text(0,15000,"Data source: https://github.com/mauforonda/vacunas"    
         "\nAutor: @Bolivian_Bot Telegram"    
         "\nNota: Histórico acumulado.", fontsize=30,fontproperties=prop);  
plt.savefig('pics/ratevacNac.png')
plt.close()



from datetime import date
from datetime import datetime
now = datetime.now()

with open('datos.py', 'a') as f:
    mss=str(now.day)+'/'+str(now.month)+'/'+str(now.year)
    mss1=str(now.day)+'/'+str(now.month)+'/'+str(now.year)+'-'+str(now.hour)+":"+str(now.minute)
    f.write("\n")
    f.write("flag_date = '" )    #ultima actualización de consulta a la fuente y generación de imagenes
    f.write(mss)
    f.write("'")
    f.write("\n")
    f.write("act_mss = '")          #las notificaciones que manda al admin con hora de ejecución.
    f.write(mss1)
    f.write("'")


#se guarda un array actualizado con los datos: 
# casos_dia     
# muertos_día    
# vacunados_1    
# vacunados_2    


muertos_dia=np.zeros(9)
casos_dia=np.zeros(9)
for j in range(9):
    muertos_dia[j]=data4[j,-1]-data4[j,-2]
    casos_dia[j]=data3[j,-1]-data3[j,-2]


estados =  [[casos_dia[0],casos_dia[1],casos_dia[2],casos_dia[3],casos_dia[4],casos_dia[5],casos_dia[6],casos_dia[7],casos_dia[8]],
            [muertos_dia[0],muertos_dia[1],muertos_dia[2],muertos_dia[3],muertos_dia[4],muertos_dia[5],muertos_dia[6],muertos_dia[7],muertos_dia[8]],
            [var_v1[3],var_v1[2],var_v1[7],var_v1[4],var_v1[6],var_v1[8],var_v1[1],var_v1[0],var_v1[5]],
            [var_v2[3],var_v2[2],var_v2[7],var_v2[4],var_v2[6],var_v2[8],var_v2[1],var_v2[0],var_v2[5]]]


uac = [y_c[-1],y_v[-1]]
np.save('estados.npy',estados)   #los valores de cada día actualizado y mostrar resumen.
np.save('fechas.npy',uac)        #Guarda las últimas fechas donde se llenaron las fuentes. 

