#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from distutils.core import setup
from bin import version
import py2exe,sys

sys.argv.append('py2exe')

excludes = ['bsddb', 'email', 'tmp', 'log', 'codesnip', 'ftpupload', 'conf']

setup(
    name='JBooking-Manager',
    version=str(version.program.version),
    packages=['bin'],
    url='https://github.com/BaileySN/JBooking-Manager',
    license='GPL3',
    author='Guenter Bailey',
    author_email='office@bailey-solution.com',
    description="Manager API for Joomla BookingCalendar and easy FTP Upload Tool.",
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
