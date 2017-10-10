# coding=utf-8
#! /usr/bin/env python2.7

"""
This code make the required changes to wordnetLoom tables
"""

import os
import codecs
import MySQLdb

def table_alter(db_name, u, p):
    # to open the database
    db = MySQLdb.connect(host="localhost", user=u, passwd=p)
    db.autocommit(True)
    cursor = db.cursor()

 
    sql_cmnd = "USE " + db_name + ";"
    cursor.execute(sql_cmnd)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

    # the tracker table
    sql_script_runner("tracker.sql", cursor, db_name, "$$")
    print("* Tracker tabeles... Done!")

    # a bunch of "ALTER" instructions
    sql_script_runner("alter.sql", cursor, db_name, ";")
    print("* All Alters ... Done!")

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    # to close the connection
    db.close()

    print ("Done! :) ")

def sql_script_runner(fileName, cursor, db_name, endChar):
    # a bunch of "ALTER" instructions
    path = os.getcwd() + '/sqlTables/'

    inputFile = codecs.open(path + fileName, encoding='utf-8')
    sqlScript = inputFile.read()
    inputFile.close()

    sqlScript = sqlScript.replace("db_name", db_name)
    sql_cmnds = sqlScript.split(endChar)

    for sql_cmnd in sql_cmnds:
        if sql_cmnd != "\n":
            if sql_cmnd == "DELIMITER" or sql_cmnd == "DELIMITER".lower():
                sql_cmnd = sql_cmnd + " " + endChar
            try:
                cursor.execute(sql_cmnd)
            except:
                print("error in : " + sql_cmnd)