#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from distutils.core import setup
from bin import version
import py2exe,sys,os
from os import curdir,sep

sys.argv.append('py2exe')
excludes = ['bsddb', 'email', 'tmp', 'log', 'codesnip', 'ftpupload', 'conf']
tmpldir = (curdir+sep+"bin"+sep)
data_files = []

for files in os.listdir(tmpldir):
    if files.endswith('.tmpl'):
        f1 = tmpldir + files
        if os.path.isfile(f1):
            f2 = (curdir+sep+"bin"), [f1]
            data_files.append(f2)

setup(
    name='JBooking-Manager',
    version=str(version.program.version),
    packages=['bin'],
    url='https://github.com/BaileySN/JBooking-Manager',
    license='GPL3',
    author='Guenter Bailey',
    author_email='office@bailey-solution.com',
    description="Manager API for Joomla BookingCalendar and easy FTP Upload Tool.",
    data_files = data_files,
    options = {"py2exe": {"optimize": 2,
                          "packages": ['bin'],
                          "excludes": excludes,
                          }
    },
    console=[{
	"script":"jbooking-manager.py",
	}],
	zipfile="jbookingmanlib.zip",
)
