# aprsballoon
Erzeugung von Telemetriedaten eines Stratosphärenballons aus eine SQLite Db als APRS-Packet

Testscript das die Daten beim Aufstieg eines Testballons simuliert und daraus entsprechende APRS packets 
 erzeugt und diese über die Soundkarte ausgibt.

 Autor: Ralf Lüsebrink, DO1EH
 Datum: 08.02.2018

 Voraussetzungen:
 Alle Software wie im Python-script "createMockData.py" beschrieben ist installiert und das Script wurde 
 einmalig ausgeführt.

 Benötigte Software:
  *AFSK
  *py-audio
  *SQLITE 

 Installation:
 Ausführlich auf http://midnightcheese.com/2015/12/super-simple-aprs-position-beacon/
 
 Kurzfassung:
 sudo apt-get install python-pip python-dev
 sudo apt-get install python-pyaudio
 sudo pip install afsk

 Kurzbeschreibung:
 Aus der Testdatenbank wird alle 2 Sekunden ein Datensatz geholt und in ein APRS-Positionspaket im compressed 
 Format umgewandelt und mit Hilfe von AFSK auf der Soundkarte ausgegeben.
