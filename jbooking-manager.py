#! /usr/bin/env python3
# -*- conding: utf-8 -*-
###########################################################################################################
# JBooking-Manager   <https://github.com/BaileySN/jbooking-manager>                                       #
# Copyright (C) [2015]  [Guenter Bailey]                                                                  #
#                                                                                                         #
# This program is free software;                                                                          #
# you can redistribute it and/or modify it under the terms of the GNU General Public License              #
# as published by the Free Software Foundation;                                                           #
# either version 3 of the License, or (at your option) any later version.                                 #
#                                                                                                         #
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;               #
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.               #
# See the GNU General Public License for more details.                                                    #
#                                                                                                         #
# You should have received a copy of the GNU General Public License along with this program;              #
# if not, see <http://www.gnu.org/licenses/>.                                                             #
###########################################################################################################
import os,csv
from os import curdir,sep
from bin import funcdb
from sys import exit
from optparse import OptionParser
import datetime
from bin import version

if not os.path.exists(curdir+sep+"conf"):
    print("create conf directory")
    os.makedirs(curdir+sep+"conf")
if not os.path.isfile(curdir+sep+"conf"+sep+"config.ini"):
    print("Create config.ini")
    from shutil import copyfile
    from time import sleep
    copyfile(curdir+sep+"bin"+sep+"config.tmpl", curdir+sep+"conf"+sep+"config.ini")
    print("Please check the config.ini first")
    sleep(2)
    exit(2)

import configparser
cfg = configparser.ConfigParser()
cfg.read(curdir+sep+"conf"+sep+"config.ini")

now = datetime.datetime.now()
currdate = now.strftime("%Y-%m-%d")

def checkfolder():
    if not os.path.exists(curdir+sep+"tmp"):
        if cfg['SYSTEM']['DEBUG'] == "True":
            print("create tmp directory")
        os.makedirs(curdir+sep+"tmp")

    if not os.path.exists(curdir+sep+"log"):
        if cfg['SYSTEM']['DEBUG'] == "True":
            print("create log directory")
        os.makedirs(curdir+sep+"log")

    if not os.path.exists(curdir+sep+"tmp"+sep+"ftpupload"):
        if cfg['SYSTEM']['DEBUG'] == "True":
            print("create ftpupload directory")
        os.makedirs(curdir+sep+"tmp"+sep+"ftpupload")

checkfolder()
db = funcdb.database()

def get_calendarid(calendarname):
    prefix = cfg['DATABASE']['DB_PREFIX']
    try:
        squery = """SELECT %sbookingcalendarforjoomla_calendars.`id` FROM %sbookingcalendarforjoomla_calendars
WHERE %sbookingcalendarforjoomla_calendars.`title` = '%s';""" %(prefix, prefix, prefix, calendarname)
        nameid = db.squery(squery)
        if cfg['SYSTEM']['DEBUG'] == "True":
            print("calid = "+str(nameid[0]))
        return nameid[0]
    except TypeError:
        if cfg['SYSTEM']['DEBUG'] == "True":
            print("calid = "+str("ERROR - Can't find Calendar"))
        return "error"

def get_statusid(calendarname, statusname):
    prefix = cfg['DATABASE']['DB_PREFIX']
    try:
        squery = """
SELECT %sbookingcalendarforjoomla_legenditems.`id`
FROM %sbookingcalendarforjoomla_legenditems WHERE %sbookingcalendarforjoomla_legenditems.`calendar` = '%s' AND
%sbookingcalendarforjoomla_legenditems.`title` = '%s' ;""" %(prefix, prefix, prefix, get_calendarid(calendarname), prefix, statusname)
        statid = db.squery(squery)
        if cfg['SYSTEM']['DEBUG'] == "True":
            print("statusid = "+str(statid[0]))
        return statid[0]
    except TypeError:
        if cfg['SYSTEM']['DEBUG'] == "True":
            print("statusid = "+str("error"))
        return "error"

def get_bookingid(calendarname, date):
    prefix = cfg['DATABASE']['DB_PREFIX']
    try:
        squery = """
SELECT %sbookingcalendarforjoomla_statuses.`id` FROM %sbookingcalendarforjoomla_statuses
WHERE %sbookingcalendarforjoomla_statuses.`calendar` = '%s' AND %sbookingcalendarforjoomla_statuses.`date` = '%s';""" %(prefix, prefix, prefix, get_calendarid(calendarname), prefix, date)
        statsid = db.squery(squery)
        if cfg['SYSTEM']['DEBUG'] == "True":
            print("bookingid = "+str(statsid[0]))
        return statsid[0]
    except TypeError:
        if cfg['SYSTEM']['DEBUG'] == "True":
            print("bookingid = "+str("error"))
        return "error"

def get_booking_status(currentdate):
    dbname = cfg['DATABASE']['DB']
    prefix = cfg['DATABASE']['DB_PREFIX']
    query = """SELECT %sbookingcalendarforjoomla_calendars.`title`,
%sbookingcalendarforjoomla_legenditems.`color`,
%sbookingcalendarforjoomla_legenditems.`title`,
%sbookingcalendarforjoomla_statuses.`status` FROM %s.%sbookingcalendarforjoomla_legenditems
INNER JOIN %s.%sbookingcalendarforjoomla_calendars ON %sbookingcalendarforjoomla_legenditems.`calendar` = %sbookingcalendarforjoomla_calendars.`id`
INNER JOIN %s.%sbookingcalendarforjoomla_statuses ON %sbookingcalendarforjoomla_legenditems.`id` = %sbookingcalendarforjoomla_statuses.`status`
WHERE %sbookingcalendarforjoomla_statuses.`date` >= '%s';""" %(prefix, prefix, prefix,prefix,dbname, prefix, dbname, prefix, prefix, prefix, dbname, prefix, prefix, prefix, prefix, currentdate)
    status = db.query(query)
    return status

def set_booking(calendarname, bookdate, statusname):
    prefix = cfg['DATABASE']['DB_PREFIX']
    query = """insert INTO %sbookingcalendarforjoomla_statuses(`calendar`, `date`, `status`)
VALUES ('%s', '%s', '%s');""" %(prefix, get_calendarid(calendarname), bookdate, get_statusid(calendarname, statusname))
    db.insert(query)

def upd_booking(calendarname, date, statusname):
    calid = get_calendarid(calendarname)
    prefix = cfg['DATABASE']['DB_PREFIX']
    query = """UPDATE %sbookingcalendarforjoomla_statuses SET `status` = '%s'
WHERE %sbookingcalendarforjoomla_statuses.`calendar` = '%s' AND
%sbookingcalendarforjoomla_statuses.`date` = '%s';""" %(prefix, get_statusid(calendarname, statusname), prefix, calid, prefix, date)
    db.insert(query)

def del_booking(calendarname, date):
    prefix = cfg['DATABASE']['DB_PREFIX']
    try:
        delquery = """DELETE FROM %sbookingcalendarforjoomla_statuses WHERE
%sbookingcalendarforjoomla_statuses.`calendar` = '%s' AND %sbookingcalendarforjoomla_statuses.`date` = '%s';""" %(prefix, prefix, get_calendarid(calendarname), prefix, date)
        db.insert(delquery)
    except TypeError:
        return "error"

def upset_booking(calendarname, date, statusname):
    try:
        if str(get_bookingid(calendarname, date)) != str("error"):
            upd_booking(calendarname, date, statusname)
            if cfg['SYSTEM']['DEBUG'] == "True":
                print("update = "+calendarname+" - "+str(date)+" - "+statusname)
        else:
            set_booking(calendarname, date, statusname)
            if cfg['SYSTEM']['DEBUG'] == "True":
                print("insert = "+calendarname+" - "+str(date)+" - "+statusname)
        return "ok"
    except IOError:
        return "error"
        pass

def ftp_transport():
    import ftplib
    FTPPATH = cfg['FTP']['FTP_LOCAL_PATH']
    FTP_UPLOAD_FILETYPE = [".html", ".htm"]

    if "None" == FTPPATH:
        FTPPATH = (curdir+sep+"tmp"+sep+"ftpupload"+sep)
    elif FTPPATH != None:
        if not os.path.exists(FTPPATH):
            print("Path: "+FTPPATH+" not exists")
            exit(2)

    ftp = ftplib.FTP(cfg['FTP']['FTP_URL'])
    try:
        ftp.login(cfg['FTP']['FTP_USER'], cfg['FTP']['FTP_PASSWORD'])
        ftp.cwd(cfg['FTP']['FTP_REMOTE_PATH'])
        for file in os.listdir(FTPPATH):
            if file.endswith(tuple(FTP_UPLOAD_FILETYPE)):
                tfile = open(FTPPATH+file, 'rb')
                ftp.storbinary('STOR '+ file, tfile)
                tfile.close()
                if cfg['SYSTEM']['DEBUG'] == "True":
                    print("File: "+file+" Uploaded")
        ftp.quit()
        ftp.close()
        print("FTP Upload to "+cfg['FTP']['FTP_URL']+" Successful")
    except:
        print("FTP Upload Error")
        ftp.quit()
        ftp.close()
        exit(2)

"""
Program starts here
"""
class App():
    def __init__(self):
        usage = "usage: JBooking-Manager v%s options" %(version.program.version)
        parser = OptionParser(usage=usage)
        parser.add_option("--update_booking", action="store_true", default=False, dest="csvload",
                          help="Update Booking Status. without option --csv it use the default file under tmp/booking.csv")
        parser.add_option("--csv", default=False, dest="csvfile", metavar="CSVFILE",
                          help="CSV File for Booking update.")
        parser.add_option("--set_booking", action="store_true", default=False, dest="setbooking",
                          help="set direct booking status: --calendar=Room1 --bookingdate=2016-08-01 --status=Free")
        parser.add_option("--calendar", default=False, dest="calendar", metavar="calendar_name",
                          help="existing calendarname in JoomlaBooking")
        parser.add_option("--bookingdate", default=False, dest="bookingdate", metavar="booking_date",
                          help="date for Booking YYYY-m-d (example: 2016-08-01)")
        parser.add_option("--status", default=False, dest="status", metavar="booking_status",
                          help="Booking Status (example: Free or Booked")
        parser.add_option("--get_booking_list", default=False, dest="bookinglist", action="store_true",
                          help="get booking list from DB. starts with current date.")
        parser.add_option("--ftpupload", action="store_true", default=False, dest="ftpserv",
                          help="Upload files from tmp/ftpupload to FTP Server.")
        (options, args) = parser.parse_args()

        if options.ftpserv:
            ftp_transport()
            exit(2)

        elif options.csvload:
            if options.csvfile:
                if cfg['SYSTEM']['DEBUG'] == "True":
                    print(options.csvfile)
                self.csv_load(options.csvfile)
                exit(2)
            else:
                if not os.path.isfile(curdir+sep+"tmp"+sep+"booking.csv"):
                    print("File : "+curdir+sep+"tmp"+sep+"booking.csv"+" not exists")
                    exit(1)
                else:
                    self.csv_load(curdir+sep+"tmp"+sep+"booking.csv")

                exit(2)

        elif options.bookinglist:
            self.get_bookings(currdate)

        elif options.setbooking:
            if options.calendar and options.bookingdate and options.status:
                self.add_booking(options.calendar, options.bookingdate, options.status)
                exit(2)
            else:
                print("use options: --calendar=Room1 --bookingdate=2016-08-01 --status=Booked")
                print("Options")
                print("======================================================================")
                parser.print_help()
                exit(1)

        else:
            parser.print_help()
            exit(1)

    def csv_load(self, filepath):
        data = csv.reader(open(filepath, 'r'), delimiter=';', quotechar='"')
        for row in data:
            calname = row[0]
            bookdate = row[1]
            statname = row[2]

            if cfg['SYSTEM']['DEBUG'] == "True":
                print(calname+" - "+bookdate+" - "+statname)

            errcode = upset_booking(calname, bookdate, statname)
            if str(errcode) != str("error"):
                print(calname+" - "+bookdate+" - "+statname+" = Success")
            else:
                print(calname+" - "+bookdate+" - "+statname+" = Error")

    def get_bookings(self, currentdate):
        print(get_booking_status(currentdate))

    def add_booking(self, calendarname, bookdate, statusname):
        if cfg['SYSTEM']['DEBUG'] == "True":
            print(calendarname+" - "+bookdate+" - "+statusname)

        errcode = upset_booking(calendarname, bookdate, statusname)
        if str(errcode) != str("error"):
            print(calendarname+" - "+bookdate+" - "+statusname+" = Success")
        else:
            print(calendarname+" - "+bookdate+" - "+statusname+" = Error")


if __name__ == "__main__":
    app = App()
