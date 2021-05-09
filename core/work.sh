#!/bin/bash

sudo supervisorctl stop telegrambot


cd /home/pi/Desktop/telebot/botv2/core/


sudo rm -r vacunas covid19-bolivia pics
sudo rm estados.npy fechas.npy
git clone https://github.com/mauforonda/vacunas
git clone -b opsoms https://github.com/mauforonda/covid19-bolivia
mkdir pics

cd ..
cd ..
source bin/activate

cd /home/pi/Desktop/telebot/botv2/core/
python vac.py
python vacnac.py
python casos.py
python casosnac.py
python ratevac.py
python ratevacnac.py
python notif.py

git add covid19-bolivia/confirmados.csv covid19-bolivia/decesos.csv
git add vacunas/datos/primera.csv vacunas/datos/segunda.csv
git commit -m 'actualizando datos de la fuente'
git push origin master

sudo rm -r covid19-bolivia vacunas 
sudo rm ip.txt
sudo rm -r __pycache__

ifconfig > ip.txt
sudo supervisorctl start telegrambot

