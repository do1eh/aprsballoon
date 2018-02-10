import sqlite3;

# Installation der nötigen Software und Erstellen von Testdaten
#
# Bebötigte Software:
#  *AFSK
#  *py-audio
#  *SQLITE 
#
# # Installation:
# Ausführlich auf http://midnightcheese.com/2015/12/super-simple-aprs-position-beacon/
# 
# Kurzfassung:
# sudo apt-get install python-pip python-dev
# sudo apt-get install python-pyaudio
# sudo pip install afsk
#
# Vorbereiten von Testdaten
# Um 300 Testdaten in einer Testdatenbank zu erzeugen um das Programm Testen zu können
# muss einfach einmalig dieses Python-script ausgeführt werden:
#
#
db = sqlite3.connect('baloon.db');

cursor = db.cursor()
cursor.execute('''
   CREATE TABLE baloondata(id INTEGER PRIMARY KEY, height integer,
                       lat real, long real , temp real, pressure real)
''')

idnr=1;
height=100;
latc=51.095390;
longc=6.850072;
temp=25.1;
pressure=1009;

for x in range(0, 300):

   cursor.execute('''INSERT into baloondata(id, height,lat,long,temp,pressure) values(?,?,?,?,?,?)''',(idnr,height,latc,longc,temp,pressure));

   idnr+=1;
   height+=5;
   latc+=0.000001;
   longc+=0.000002;
   temp-=0.3;
   pressure-=1;


db.commit()
db.close();
