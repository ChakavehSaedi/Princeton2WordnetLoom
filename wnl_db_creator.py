# coding=utf-8
#! /usr/bin/env python2.7

"""
'db_creator.py'

Using princeton wordnet files, this code creates the database to be employed in WordnetLoom.

Accepts as input:
    --- wordnet files: data.pos and index.pos - pos = [noun, verb, adj, adv] --- ONLY Tested on Nouns

    variables to be set are tagged with   "<------ to be set"     in the code

2017 Chakaveh Saedi <chakaveh.saedi@di.fc.ul.pt>
"""

from datetime import datetime
import MySQLdb
import os
import time

from preprocess.synsetID import *
from preprocess.wordNet_indexFile_builder import *
from sqlTables.dataMigrate import *
from sqlTables.alterTables import *


user = "root"                                               #  <------ to be set  -  for the SQL connection
passwd = "???????"                                          #  <------ to be set  -  for the SQL connection
mapTag = " n "                                              #  <------ to be set  -  '[" n "," v "," a "," r "] according to the POS
en_newWordnetEntries = False                                #  <------ to be set  -  specifies if there is a new
                                                            #          version of the English wordnet to update the offsets
                                                            #          True   /   False
english_ready = True                                        #  <----- To use the previously made data-base for english-princeton
db_name = "??????????"                                      #  <------ to be set  - database name to be used in wordnetLoom [NOTE: if a database with this name already exists, IT WILL BE DELETED ]
lexicon = 1                                                 #  <------ to be set  -  1 or 2 or ....
                                                            #  2 is always English_Princeton in wordnetLoom setting
                                                            #  lexicon_number is important for setting sense_index
data_folder = "pt_wnet"                                     #  <------ to be set  - the folder in which wordnet files (other than English are saved)
                                                            #  This folder is in data folder   #"en_wnet" is for English Wordnet
newWordnetEntries = False                                   #  <------ to be set  -  specifies if there is a new
                                                            #          version of the wordnet to update the offsets
                                                            #          True   /   False


path = os.getcwd() + '/data/dumps/'

#----------------------------------------------------- English wordnet
if english_ready == False:
    # To create the database and fill the tables with entries of english wordnet data
    inputFileName = ["data.noun","index.noun"]
    lexicon = 2

    # ----------------------------------------------------- preprocess
    if en_newWordnetEntries == True:
        # to create an index file to helf speeding up the process
        commnt_cnt = index_creator(inputFileName, lexicon, data_folder)

        # to replace the offset in the data and index file with a sequential integer which will be used as synset_id later
        offset_replace(inputFileName, mapTag, en_newWordnetEntries, lexicon, commnt_cnt, data_folder)
    #------------------------------------------------------------------

    new_db = 'y'             # to create a new database
    db_creator(inputFileName, db_name, new_db, lexicon, user, passwd, data_folder)

    dump_path = path + db_name + "_dump_en.sql"
    terminalCommand = " mysqldump --user=" + user + " --password=" + passwd + " " + db_name + " > " + dump_path + " ;"
    os.system(terminalCommand)
    time.sleep(20)
else:
    # To create the database and load the data (english wordnet data) from a dump.sql file
    db = MySQLdb.connect(host="localhost", user=user, passwd=passwd)
    db.autocommit(True)
    cursor = db.cursor()
    sql_cmnd = "DROP DATABASE IF EXISTS "+ db_name+ ";"
    cursor.execute(sql_cmnd)
    sql_cmnd = "CREATE DATABASE " + db_name + " DEFAULT CHARACTER SET utf8;"
    cursor.execute(sql_cmnd)
    db.close()

    dump_path = path + "dump_en.sql"
    print("loading data ...")
    terminalCommand = " mysql --user=" + user + " --password=" + passwd + " " + db_name + " < " + dump_path + " ;"
    os.system(terminalCommand)
    time.sleep(30)

#-----------------------------------------------------  Wordnet in other Language
inputFileName = ["data.noun","index.noun"]
lexicon = 1

#----------------------------------------------------- preprocess
if newWordnetEntries == True:
    # to create an index file to helf speeding up the process
    commnt_cnt = index_creator(inputFileName, lexicon, data_folder)

    # to replace the offset in the data and index file with a sequential integer which will be used as synset_id later
    offset_replace(inputFileName, mapTag, newWordnetEntries, lexicon, commnt_cnt,data_folder)
# ------------------------------------------------------------------

new_db = 'n'       # to update the previously built/loaded database
db_creator(inputFileName, db_name, new_db,lexicon, user, passwd, data_folder)

dump_path = path + db_name + "_dump_all.sql"
terminalCommand = " mysqldump --user=" + user + " --password=" + passwd + " " + db_name + " > " + dump_path + " ;"
os.system(terminalCommand)
time.sleep(20)

print (str(datetime.now()))
