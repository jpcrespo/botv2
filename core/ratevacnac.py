import os,sys
import pandas as pd
import numpy as np
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)      
import matplotlib.pyplot as plt

_n=1151.31 # factor de correción para llevar a 10^4 hab

#datos vacunacion
df1=pd.read_csv('vacunas/datos/primera.csv',sep=',').sort_values(by='fecha').set_index('fecha')
df2=pd.read_csv('vacunas/datos/segunda.csv',sep=',').sort_values(by='fecha').set_index('fecha')
df3=pd.read_csv('covid19-bolivia/confirmados.csv',sep=',').sort_values(by='Fecha').set_index('Fecha')
df4=pd.read_csv('covid19-bolivia/decesos.csv',sep=',').sort_values(by='Fecha').set_index('Fecha')


#ambas concentraciones de datos tienen distintos etiquetados.
#se replican los ordenes en distintos vectores.
dep_v=['Beni','Chuquisaca','Cochabamba','La Paz','Oruro','Pando','Potosi','Santa Cruz','Tarija']
# c_dep = _n*(1/100)*np.array([4.19,5.78,17.52,27.03,4.92,1.10,8.23,26.42,4.81])  #el porcentaje



data1 = df1.iloc[:,:].values.T
data2 = df2.iloc[:,:].values.T
data3 = df3.iloc[:,:].values.T
data4 = df4.iloc[:,:].values.T

var_v1=np.zeros((9,len(data1[0])))
var_v2=np.zeros((9,len(data2[0])))

for j in range(9):
    var_v1[j,0]=data1[j,0]/_n
    var_v2[j,0]=data2[j,0]/_n
    for i in range(1,len(data1[0])):
        var_v1[j,i]=(data1[j,i]-data1[j,i-1])/_n
        var_v2[j,i]=(data2[j,i]-data2[j,i-1])/_n
        
y_v=df1.index.values       #Se recuperaron los datos de la fuente
y_c=df3.index.values       #con el indice dado por las fechas del reporte



v_v1 = df1.rolling(7,min_periods=1).mean()
v_v2 = df2.rolling(7,min_periods=1).mean()
mv_v1 = v_v1.iloc[:,:].values.T   
mv_v2 = v_v2.iloc[:,:].values.T   

mm_v1=np.zeros((9,len(data1[0])))
mm_v2=np.zeros((9,len(data2[0])))


for j in range(9):
    mm_v1[j,0]=mv_v1[j,0]/_n
    mm_v2[j,0]=mv_v2[j,0]/_n
    for i in range(1,len(data1[0])):
        mm_v1[j,i]=(mv_v1[j,i]-mv_v1[j,i-1])/_n
        mm_v2[j,i]=(mv_v2[j,i]-mv_v2[j,i-1])/_n


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




nac_v1 = mm_v1[0]+mm_v1[1]+mm_v1[2]+mm_v1[3]+mm_v1[4]+mm_v1[5]+mm_v1[6]+mm_v1[7]+mm_v1[8]
nac_v2 = mm_v2[0]+mm_v2[1]+mm_v2[2]+mm_v2[3]+mm_v2[4]+mm_v2[5]+mm_v2[6]+mm_v2[7]+mm_v2[8]

bol = mpimg.imread('bol.jpg')
imagebox = OffsetImage(bol,zoom=1)
firma = AnnotationBbox(imagebox,(len(y_v)/2,30))


fig = plt.figure(figsize=(35,25))

#Color del fondo
fig.patch.set_facecolor(tableau20[0])
plt.axes().patch.set_facecolor(tableau20[0])


plt.subplots_adjust(top=0.80)
plt.title('\nTasa de Vacunación Nacional cada 10\'000 HAB' +'\n(último reporte en fuente: '+y_v[-1]+')\n',fontsize=75,fontproperties=prop,color=tableau20[1])
plt.plot(y_v,nac_v1,label='Promedio de 7 días - 1 Dosis',linewidth=5,color=tableau20[3],linestyle='-')
plt.plot(y_v,nac_v2,label='Promedio de 7 días - 2 Dosis',linewidth=5,color=tableau20[2],linestyle='-')
plt.xticks(y_v[::7],fontsize=50,rotation=45,fontproperties=prop,color=tableau20[1])
plt.ylabel('\nVacunados/día\n',fontsize=60,fontproperties=prop,color=tableau20[1])
plt.yticks(fontsize=50,fontproperties=prop,color=tableau20[1])
#plt.ylim(0,np.max(mm_v1))
plt.gca().yaxis.grid(linestyle='--',linewidth=1,dashes=(5,15))
plt.gca().spines["top"].set_visible(False)    
plt.gca().spines["bottom"].set_visible(True)    
plt.gca().spines["right"].set_visible(False)    
plt.gca().spines["left"].set_visible(False)  
plt.gca().get_xaxis().tick_bottom()    
plt.gca().get_yaxis().tick_left()
plt.gca().add_artist(firma)
plt.subplots_adjust(bottom=0.3)
plt.text(len(y_v), nac_v1[-1],'1er Dosis',fontsize=35,color=tableau20[3],fontproperties=prop)
plt.text(len(y_v), nac_v2[-1],'2da Dosis',fontsize=35,color=tableau20[2],fontproperties=prop)
plt.text(0,-18,"Data source: https://github.com/mauforonda/vacunas"    
         "\nAutor: @Bolivian_Bot Telegram"    
         "\nNota: Histórico acumulado.", fontsize=35,fontproperties=prop,color=tableau20[1]);  
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
            [_n*var_v1[3,-1],_n*var_v1[2,-1],_n*var_v1[7,-1],_n*var_v1[4,-1],_n*var_v1[6,-1],_n*var_v1[8,-1],_n*var_v1[1,-1],_n*var_v1[0,-1],_n*var_v1[5,-1]],
            [_n*var_v2[3,-1],_n*var_v2[2,-1],_n*var_v2[7,-1],_n*var_v2[4,-1],_n*var_v2[6,-1],_n*var_v2[8,-1],_n*var_v2[1,-1],_n*var_v2[0,-1],_n*var_v2[5,-1]]]


uac = [y_c[-1],y_v[-1]]
np.save('estados.npy',estados)   #los valores de cada día actualizado y mostrar resumen.
np.save('fechas.npy',uac)        #Guarda las últimas fechas donde se llenaron las fuentes. 



