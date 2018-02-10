import sqlite3,time,math,os;

# Testscript das die Daten beim Aufstieg eines Testballons simuliert und daraus entsprechende APRS packtets 
# erzeugt und diese über die Soundkarte ausgibt.
#
# Autor: Ralf Lüsebrink, DO1EH
# Datum: 08.02.2018
#
# Voraussetzungen:
# Alle Software wie im Python-script "createMockData.py" beschrieben ist installiert und das Script wurde 
# einmalig ausgeführt.
#
# Kurzbeschreibung:
# Aus der Testdatenbank wird alle 2 Sekunden ein Datensatz geholt und in ein APRS-Positionspaket im compressed 
# Format umgewandelt und mit Hilfe von AFSK auf der Soundkarte ausgegeben.
#
# Das APRS compressed-Format
# Das compressed Format basiert auf der BASE-81 kompression. So ist es möglich die Koordinaten und die Höhe 
# mit weit weniger Zeichen darzustellen als im klassischen Format. So bleibt mehr Platz für Telemetrie-Daten
#
# Klassisches APRS Positionsframe:
# 
#   Format:         /DDMM.hhN/DDDMM.hhW$CSE/SPD/comments...    
#   Bespiel:        /5117.16N/00681.44EOBallon Test de DO1EH
#
# Compressed Format:
# 
#   Format:         /YYYYXXXXOcsT    mit y=lat x=long c=course s=speed oder cs=hoehe T=Compression Type
#
# Beschreibung der Berechnung der Koordinaten
# / und O legen das Symbol (in diesem Fall das Ballonsymbol) fest wie die Station auf der APRS-Karte erscheinen 
# soll.  Die Koordinaten werden mit base81 codiert und in ASCII-Werte umgerechnet uindem 33 subtrahiert wird.
# So entsteht jeweils ein 4 stelliger ASCII String. Eine genaue Beschreibung findet sich unter
# http://www.aprs.org/doc/APRS101.PDF ab Seite 37.
#
# Leider habe ich noch nicht herausgefunden wie die Höhe berechnet wird. Hier wir in der Dokumentaion nur das 
# Dekodieren, nicht aber das Encodieren beschrieben.
#
# Als Compresion Type T nehmen wie einfach #T=00110000 =48 an. 



# Berechnet aus einem Längengrad (z.B.6.850072) den String im comressed-Format
def compress_long(longitude):
    
    
    basis=int(190463*(180+longitude));

    a=basis/(91**3);
    resta=basis%(91**3); 

    b=resta/(91**2);
    restb=resta%(91**2); 

    c=restb/91;
    d=restb%91;

    
    a=a+33;
    b=b+33;
    c=c+33; 
    d=d+33;

    return chr(a)+chr(b)+chr(c)+chr(d);

# Berechnet aus einem Breitengrad (z.B.51.095390) den String im comressed-Format
def compress_lat(latitude):
    
    
    basis=int(380926*(90-latitude));

    

    a=basis/(91**3);
    resta=basis%(91**3); 

    b=resta/(91**2);
    restb=resta%(91**2); 

    c=restb/91;
    d=restb%91;

    
    a=a+33;
    b=b+33;
    c=c+33; 
    d=d+33;

    return chr(a)+chr(b)+chr(c)+chr(d);

# Falls in den berechneten Koordinaten im comressed-Format Sonderzeichen wie
# ' oder " vorkommen, müssen diese mit \ ecpaed werden, damit AFSK diese verarbeiten kann.
def autoescape(zeichenkette):
   zeichenkette=zeichenkette.replace("\'","\\\'");
   zeichenkette=zeichenkette.replace("`","\\`");
   zeichenkette=zeichenkette.replace("\"","\\\"");
   zeichenkette=zeichenkette.replace("\'","\\\'");

   return zeichenkette;


# Hier beginnt das eigentlicke Programm:

# 1. Datenbank connecten:
db = sqlite3.connect('baloon.db');
cursor = db.cursor()

#Testdaten holen
cursor.execute('''SELECT * FROM baloondata''')
all_rows = cursor.fetchall()

# Testdatenformat:
# row[0]=id
# row[1]=height
# row[2]=lat
# row[3]=long
# row[4]=temp
# row[5]=pressure


for row in all_rows:
     
    # T berechnen im compressed Fomat (#T=00110000 =48):
     T=chr(48+33);

     # Text für Telemetrie zusammenbauen:
     telemetrie="Hoehe:"+str(row[1])+"m-Temp:"+str(row[4])+"C-Druck:"+str(row[5])+"hPa";
     #Koordinaten berechnen und komplettes Frame zusammensetzen:
     packetstring=autoescape("/"+compress_lat(row[2])+compress_long(row[3])+"000"+T+telemetrie)

     # Zur Kontrolle einmal ausgeben damit man beim Test auch etwas sieht
     print packetstring;
     # Frame als 1k2 AFSK Signal auf der Soundkarte ausgeben und dabei alle Fehler Ausgaben untedrücken.
     os.system("aprs -c DO1EH "+packetstring+" 2>/dev/null"); 
     # Vor dem nächsten Frame 2 Sekunden Pause machen
     time.sleep(2);

db.commit()
db.close();


