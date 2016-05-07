#!/usr/bin/env python3
# coding: utf-8
import pymysql
from os import curdir,sep
import configparser
cfg = configparser.ConfigParser()
cfg.read(curdir+sep+"conf"+sep+"config.ini")


class database:
    def __init__(self):
        self.connection = pymysql.connect(cfg['DATABASE']['DB_HOST'], cfg['DATABASE']['DB_USER'], cfg['DATABASE']['DB_PASSWORD'], cfg['DATABASE']['DB'])
        self.cursor = self.connection.cursor()

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            self.connection.rollback()

    def query(self, query):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        self.connection.rollback()
        return cursor.fetchall()

    def squery(self, query):
        cursor = self.connection.cursor(pymysql.cursors.Cursor)
        cursor.execute(query)
        self.connection.rollback()
        return cursor.fetchone()

    def idsens(self, queryid):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(queryid)
        self.connection.rollback()
        return cursor.fetchall()

    def __del__(self):
        try:
            self.connection.close()
        except:
            pass
