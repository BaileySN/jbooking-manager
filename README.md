# JBooking-Manager

JBooking-Manager kann man als API für Joomla Booking Calendar und als FTP Client ansehen.

Dabei kann das Programm über die CMD Bedient werden.

Für die Verwendung der Pakete gibt es 2 Möglichkeiten:

1. Einmal die Pakete von GitHub (auch Sourcen genannt) verwenden. Die Vorteile sind ein besseres Update- und Versionsmanagement. **Bevorzugt**

2. Oder die verwendung der Kompilierten **exe** Datei, dies aber leider durch die Lizenz auf dem [Download Server](https://dl.bscn.at/JBooking-Manager/) liegen muss. 

*Wichtig: Die exe Version wird zeitverzögert erstellt, somit sind die Bugfixes und  neue Features zuerst auf Github.*

**Inhalt**

[**Config.ini**](#configini)

---

[**Einrichtung Git Version**](#einrichtung-direkt-von-github)

[**Verwendung**](#verwendung-git-version)

---

[**Einleitung exe Version**](#verwendung-der-bereits-kompilierten-version-auch-exe-version-genannt)

[**Download**](#download-der-exe--zip-dateien)

[**Einrichtung**](#einrichtung-exe-version)

[**Verwendung**](#verwendung-exe-version)



## Einrichtung (direkt von GitHub)

Für die Verwendung benötigt man folgende Pakete noch zusätzlich zu Python 3.4.x.

Windows Pakete liegen auch auf unserem [Download Server](https://dl.bscn.at/JBooking-Manager/Source/) bereit.

* Python 3.4.x
* PyMySQL ab 0.7.2 Installation über pip
* pip

Man kann die erforderlichen Pakete auch über *pip* installieren.
```
pip install -r requirements.txt
```

## config.ini

Vor der ersten Inbetriebnahme muss die *config.ini* angepasst werden, sonst gibt das Programm beim starten eine Fehlermeldung aus.

```
# -*- coding: utf-8 -*-

[SYSTEM]
# Debugging aktivieren
# DEBUG = True
# Erweiterte Ausgabe
#
DEBUG =

[DATABASE]
# Datenbank Einstellungen
#
# DB = <Datenbank>
# DB_HOST = <Datenbank Server IP oder DNS>
# DB_USER = <Datenbank Benutzer>
# DB_PASSWORD = <Passwort vom Benutzer>
# DB_PREFIX = <Datenbank Prefix z.B.: jo34_ von Joomla vorgegeben>
#
DB =
DB_HOST =
DB_USER =
DB_PASSWORD =
DB_PREFIX = jo34_

[FTP]
# FTP Einstellungen
#
# FTP_URL = <FTP Server URL/IP>
# FTP_USER = <FTP Benutzer>
# FTP_PASSWORD = <FTP Benutzer Passwort>
# FTP_UPLOAD_FILETYPE = <Dateitypen die Hochgeladen werden sollen mit Komma getrennt>
# FTP_LOCAL_PATH = <Anderen Pfad fuer das hochladen der Daten ueber FTP
#
FTP_URL =
FTP_USER =
FTP_PASSWORD =
FTP_UPLOAD_FILETYPE = .html, .htm
FTP_REMOTE_PATH = images/tirol/preise/
FTP_LOCAL_PATH = None
```

## Verwendung (Git Version)

Das Programm JBooking-Manager kann man über die Konsole unter Linux, Windows oder Mac mit dem Kommando 
`python3 jbooking-manager.py --<option>` verwenden.


**Folgende Funktionen sind derzeit vorhanden:**

* Hilfe Aufrufen:
```
python3 jbooking-manager.py --help
Usage: JBooking-Manager v0.4 options

Options:
  -h, --help            show this help message and exit
  --update_booking      Update Booking Status. without option --csv it use the
                        default file under tmp/booking.csv
  --csv=CSVFILE         CSV File for Booking update.
  --set_booking         set direct booking status: --calendar=Room1
                        --bookingdate=2016-08-01 --status=Free
  --calendar=calendar_name
                        existing calendarname in JoomlaBooking
  --bookingdate=booking_date
                        date for Booking YYYY-m-d (example: 2016-08-01)
  --status=booking_status
                        Booking Status (example: Free or Booked
  --get_booking_list    get booking list from DB. starts with current date.
  --ftpupload           Upload files from tmp/ftpupload to FTP Server.
```


* Joomla Booking Calendar über eine CSV Datei Status und Buchungen hinzufügen / aktualisieren.
```
python3 jbooking-manager.py --update_booking --csv=tmp/bookingfile.csv
```
Falls die Option --csv nicht verwendet wird, versucht es die Datei booking.csv unter /tmp zu finden.


* Buchungsstatus direkt über die CMD setzen
```
python3 jbooking-manager.py --set_booking --calendar=Zimmername --bookingdate=Buchungsdatum --status=Booked
```

* FTP Daten hochladen
```
python3 jbooking-manager.py --ftpupload
```
Es werden dabei die html Dateien von *tmp/ftpupload* auf den jeweiligen Server hochgeladen.
Die Platzierung kann über die [*config.ini*](#configini) bei **FTP_REMOTE_PATH** festgelegt werden.

---

## Verwendung der bereits Kompilierten Version (auch exe Version genannt)

### Download der EXE / ZIP Dateien

[JBooking-Manager Download](https://dl.bscn.at/JBooking-Manager/)

Die *EXE* Version ist ein Installer, der das Archiv unter *C:\Bailey-Solution\jbooking-manager* oder man gibt einen anderen Pfad an entpackt.

Die *ZIP* Version braucht man nur in das gewünschte Verzeichnis entpacken.

Die *EXE* und *ZIP* Pakete sind mit einer Versionsnummer versehen um so leichter die aktuelle Version zu finden, auch braucht man nichts mehr nachinstallieren.

### Einrichtung (exe Version)

Man braucht nur noch mehr die [*config.ini*](#configini) anpassen.

### Verwendung (exe Version)

Das Programm wird über die Konsole (somit ist es leichter mit einem externem Programm zu Arbeiten) mit folgendem Befehl `jbooking-manager.exe --<option>` im entpacktem Verzeichnis aufgerufen.


**Folgende Funktionen sind derzeit vorhanden:**

* Hilfe Aufrufen:
```
C:\Bailey-Solution\jbooking-manager: jbooking-manager.exe --help
Usage: JBooking-Manager v0.4 options

Options:
  -h, --help            show this help message and exit
  --update_booking      Update Booking Status. without option --csv it use the
                        default file under tmp/booking.csv
  --csv=CSVFILE         CSV File for Booking update.
  --set_booking         set direct booking status: --calendar=Room1
                        --bookingdate=2016-08-01 --status=Free
  --calendar=calendar_name
                        existing calendarname in JoomlaBooking
  --bookingdate=booking_date
                        date for Booking YYYY-m-d (example: 2016-08-01)
  --status=booking_status
                        Booking Status (example: Free or Booked
  --get_booking_list    get booking list from DB. starts with current date.
  --ftpupload           Upload files from tmp/ftpupload to FTP Server.
```


* Joomla Booking Calendar über eine CSV Datei Status und Buchungen hinzufügen / aktualisieren.
```
C:\Bailey-Solution\jbooking-manager: jbooking-manager.exe --update_booking --csv=tmp/bookingfile.csv
```
Falls die Option --csv nicht verwendet wird, versucht es die Datei booking.csv unter /tmp zu finden.


* Buchungsstatus direkt über die CMD setzen
```
C:\Bailey-Solution\jbooking-manager: jbooking-manager.exe --set_booking --calendar=Zimmername --bookingdate=Buchungsdatum --status=Booked
```

* FTP Daten hochladen
```
C:\Bailey-Solution\jbooking-manager: jbooking-manager.exe --ftpupload
```
Es werden dabei die html Dateien von *tmp/ftpupload* auf den jeweiligen Server hochgeladen.
Die Platzierung kann über die [*config.ini*](#configini) bei **FTP_REMOTE_PATH** festgelegt werden.
