# coding=utf-8
#! /usr/bin/env python2.7

"""
This code creates the required tables for wordnetLoom and handles data migration from wordnet princeton to the new
tables.

The sql_scripts used to create the tables is saved in wordnetLoom_Db_creator/sqlTables/schema_prepare.sql
alter.sql makes changes to the created database and is a way of keeping this code parallel with WordnetLoom which is underder development
attributes.sql contains the attributes used in related fields based on WordnetLoom setting
"""

import os
import time
import codecs
import MySQLdb

def db_creator(inputFileName, db_name, new_db,lexicon, u, p, data_folder):
    # to create the database
    db = MySQLdb.connect(host="localhost", user=u, passwd=p)
    db.autocommit(True)
    cursor = db.cursor()
    allDone = False                # used to identify when is the time for the final alter to the tables
                                   #  <------ to be set
    if lexicon == 2:               #  <------ 4 items to be set "lang", "id_lexicon", "domain", "example", "extra_data"
        lang = "en"
        id_lexicon = "2"
        domain = "2"  # en-princeton
        example = ",'Corpus example for ["
        path = os.getcwd() + '/data/en_wnet/'
        extra_data = False
    else:
        lang = "pt"
        id_lexicon = "1"
        domain = "1"  # pt-wordnet
        example = ",'Exemplo de corpus para ["
        path = os.getcwd() + '/data/' + data_folder + '/'
        extra_data = True          # True if the data file has some extra information for synsets.
                                    # format of the data must be handled in "data_line_format_process"
    mappingFile = "mapp_n.txt"

    # This is for keeping Princetone format ID
    srcF = open(path + mappingFile)
    mapp = srcF.readlines()
    srcF.close()
    mapDic = {}
    for line in mapp:
        line = line.replace("\n", "")
        mapDic.update({line.split(" ")[1]: line.split(" ")[0]})

    if new_db == 'y':
        sql_cmnd = "DROP DATABASE IF EXISTS " + db_name + ";"
        cursor.execute(sql_cmnd)

        sql_cmnd = "CREATE DATABASE " + db_name + " DEFAULT CHARACTER SET utf8;"
        cursor.execute(sql_cmnd)

        sql_cmnd = "USE " + db_name + ";"
        cursor.execute(sql_cmnd)

        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # to create all the tables using an sql_script (schema_prepare.sql)
        sql_script_runner("schema_prepare.sql", cursor, db_name, ';')

        print("* Tables are created")

        # to insert fix primary data (such as name of relations and name of the lexicons) to the corresponding tables
        # this data is currently set for 2 wordnets (Portuguese and English)
        # to make changes, use files saved in ".../data/table_default_values/"

        # table 5-text gets the entries while data is inserted into other tables

        print("* Inserting primary data into tables")

        # ---- table 17- lexicon
        table_name = "lexicon"
        text_update = True
        insert_into_table_fromTablefile(table_name, cursor, text_update)
        print("  table lexicon ... Done!")

        # ---- table 19- domain
        table_name = "domain"
        text_update = True
        insert_into_table_fromTablefile(table_name, cursor, text_update)
        print("  table domain ... Done!")

        # ---- table 16- part_of_speech
        table_name = "part_of_speech"
        text_update = True
        insert_into_table_fromTablefile(table_name, cursor, text_update)
        print("  table part_of_speech ... Done!")

        # ---- table 20- domain_allowed_posses
        table_name = "domain_allowed_posses"
        text_update = False
        insert_into_table_fromTablefile(table_name, cursor, text_update)
        print("  table domain_allowed_posses ... Done!")

        # ---- table 13- relation_type
        table_name = "relation_type"
        text_update = True
        insert_into_table_fromTablefile(table_name, cursor, text_update)
        print("  table relation_type ... Done!")

        # ---- table 15- relation_argument
        table_name = "relation_argument"
        text_update = True
        insert_into_table_fromTablefile(table_name, cursor, text_update)
        print("  table relation_argument ... Done!")

        # ---- table 14- relation_test
        table_name = "relation_test"
        text_update = True
        insert_into_table_fromTablefile(table_name, cursor, text_update)
        print("  table relation_test ... Done!")

        # ---- table 22- attribute_type
        sql_script_runner("attributes.sql", cursor, db_name, ";")

        print("  attributes ... Done!")

    else:
        sql_cmnd = "USE " + db_name + ";"
        cursor.execute(sql_cmnd)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

    # to migrate the data from Princetone wordnet into the corresponsing tables in WordnetLoom

    #data file
    inputFile = codecs.open(path + "wnl_" + inputFileName[0], encoding='utf-8')
    wordNet_data = inputFile.readlines()
    inputFile.close()

    #index file
    inputFile = codecs.open(path + "wnl_" + inputFileName[1], encoding='utf-8')
    wordNet_indx = inputFile.readlines()
    inputFile.close()

    #error file
    errorFile = codecs.open(path + "error_" + inputFileName[0] + "_" + db_name + ".txt", "w", encoding='utf-8')

    #to create a dictionary of the index file to make the process faster
    indexFileDictionary = {}
    for line in wordNet_indx:
        line = line.replace("\n", "")
        parts = line.split(" ")
        indexFileDictionary.update({parts[0]: line[len(parts[0])+1:]})

    # relationType_ids in the relation_type table
    synset_relationType_id, sense_relationType_id = relationType_id_extraction(cursor, lang)

    # pos_ids in the pos table
    pos_id = pos_id_extraction(cursor)

    # domain_ids in the pos table
    domain_id = domain_id_extraction(cursor)

    # similar to ids in relation_type table
    sql_cmnd = "select relation_type.id from relation_type, text where relation_type.name = text.id and text.text = 'pt_syn_Similar-to';"
    cursor.execute(sql_cmnd)
    ans = cursor.fetchall()
    pt_sim_id = str(ans[0][0])

    sql_cmnd = "select relation_type.id from relation_type, text where relation_type.name = text.id and text.text = 'en_syn_Similar-to';"
    cursor.execute(sql_cmnd)
    ans = cursor.fetchall()
    en_sim_id = str(ans[0][0])

    # variables to keep track of the number of entries in each table
    wrd_table_id = id_retrieve("word","none", cursor,"table") + 1
    sense_table_id = id_retrieve("sense", "none", cursor,"table") + 1
    synset_table_id = id_retrieve("synset", "none", cursor,"table") + 1
    synset_relation_table_id = id_retrieve("synset_relation", "none", cursor,"table") + 1
    sense_to_synset_table_id = id_retrieve("sense_to_synset", "none", cursor,"table") + 1
    sense_relation_table_id = id_retrieve("sense_relation", "none", cursor,"table") + 1
    synset_attribute_table_id = id_retrieve("synset_attribute", "none", cursor,"table") + 1
    sense_attribute_table_id = id_retrieve("sense_attribute", "none", cursor,"table") + 1

    #exporting data from wordnet.data file to wordnetLoom tabales
    later_insert = {}                 # to save information about senses that must be inserted into the tables later on
    insert_no_more = set([])          # to stop multiple entries for ambiguous words

    if synset_table_id == 1 :
        synset_start = 0              # refers to the database which is being created
    else:
        synset_start = synset_table_id - 1

    print("* Migrating data from Princetone format into wordnetLoom database")

    lineCnt = 0
    for synsetIndex in range(len(wordNet_data)):

        if lexicon == 2:
            comment = "'no-comment'"
        else:
            # to handle special comments based on the synsets
            lineCnt += 1
            if lineCnt < 17282:
                comment = "'ready'"
            elif lineCnt > 17281 and lineCnt < 30378:
                comment = "'unchecked'"
            else:
                comment = "'added_synset'"

        #try:
        dataLine = wordNet_data[synsetIndex]
        dataLine = dataLine.replace("\n", "")
        data = data_line_format_process(dataLine, lang, extra_data)
        thisSynsetPos = data[0]
        synsetWrds = data[1]
        synsetConnections = data[2]
        synsetRelationTypes = data[3]
        connectedSynsetPos = data[4]

        synsetExtraInfo = data[5]
        synsetDefinition = synsetExtraInfo[6]
        sim_to = synsetExtraInfo[0]
        en_mapped_pos = synsetExtraInfo[1]
        if synsetExtraInfo[2] != "NULL" and synsetExtraInfo[2] in domain_id.keys():
            domain = domain_id[synsetExtraInfo[2]]
        sumo = "NULL"
        if synsetExtraInfo[3] != "NULL" or synsetExtraInfo[4] != "NULL":
            sumo = "'sumo: " + synsetExtraInfo[3] + "   " + synsetExtraInfo[4] + "'"
            sumo = sumo.replace("NULL", "")
        if synsetExtraInfo[5] != "NULL":
            comment = comment + "," + synsetExtraInfo[5]
        #if sim_to != "NULL" and thisSynsetPos != en_mapped_pos:
        #    comment = comment + ",'but the pos in similar to relation do not match'"

        # ---- table 8-synset
        sql_cmnd = "INSERT INTO synset VALUES(" + str(synset_table_id) + ",1);"    #split field in synset table is considered to be 1 for all entries
        cursor.execute(sql_cmnd)

        #working_indx = synset_table_id - synset_start

        # ---- table 6-synset_relation
        for i in range(len(synsetConnections)):      # this loop is for relation between synsets of a language
            rt = synsetRelationTypes[i]
            id = synset_relationType_id[rt][1]
            sql_cmnd = "INSERT INTO synset_relation VALUES(" + str(synset_relation_table_id) + "," + id + "," + str(int(synsetConnections[i]) + synset_start) + "," + str(synset_table_id) + ");"
            cursor.execute(sql_cmnd)
            synset_relation_table_id += 1

        if sim_to != "NULL":                      # to connect Portuguese synsets to corresponding synset in English
            sql_cmnd = "INSERT INTO synset_relation VALUES(" + str(synset_relation_table_id) + "," + pt_sim_id + "," + str(sim_to) + "," + str(synset_table_id) + ");"
            cursor.execute(sql_cmnd)
            synset_relation_table_id += 1

            sql_cmnd = "INSERT INTO synset_relation VALUES(" + str(synset_relation_table_id) + "," + en_sim_id + "," + str(synset_table_id) + "," + str(sim_to) + ");"
            cursor.execute(sql_cmnd)
            synset_relation_table_id += 1

        # ---- table 7-synset_attribute
        #--- comment
        comment = "concat_ws('\n', text, " + comment + ")"

        text_table_id = id_retrieve("text", "none", cursor, "table") + 1
        txt_sql_cmnd = "INSERT INTO text VALUES(" + str(text_table_id) + "," + comment + ");"
        cursor.execute(txt_sql_cmnd)
        synset_attribute = text_table_id

        text_table_id += 1

        "1 is referring to the first entry in attribute_type table which is synset_comment"
        sql_cmnd = "INSERT INTO synset_attribute VALUES(" + str(synset_attribute_table_id) + "," + str(synset_table_id) + ",1," + str(synset_attribute)+ ");"
        cursor.execute(sql_cmnd)
        synset_attribute_table_id += 1

        #--- definition
        txt_sql_cmnd = "INSERT INTO text VALUES(" + str(text_table_id) + ",'" + synsetDefinition + "');"
        cursor.execute(txt_sql_cmnd)
        synset_attribute = text_table_id

        text_table_id += 1

        "4 is referring to the forth entry in attribute_type table which is synset_definition"
        sql_cmnd = "INSERT INTO synset_attribute VALUES(" + str(synset_attribute_table_id) + "," + str(synset_table_id) + ",4," + str(synset_attribute) + ");"
        cursor.execute(sql_cmnd)
        synset_attribute_table_id += 1

        # --- Princeton format ID
        txt_sql_cmnd = "INSERT INTO text VALUES(" + str(text_table_id) + ",'" + mapDic[str(synset_table_id - synset_start)] + "');"
        cursor.execute(txt_sql_cmnd)
        synset_attribute = text_table_id

        text_table_id += 1

        "5 is referring to the fifth entry in attribute_type table which is synset_princetonId"
        sql_cmnd = "INSERT INTO synset_attribute VALUES(" + str(synset_attribute_table_id) + "," + str(synset_table_id) + ",5," + str(synset_attribute) + ");"
        cursor.execute(sql_cmnd)
        synset_attribute_table_id += 1

        # --- Sumo
        if sumo != "NULL":
            txt_sql_cmnd = "INSERT INTO text VALUES(" + str(text_table_id) + "," + sumo + ");"
            cursor.execute(txt_sql_cmnd)
            synset_attribute = text_table_id

            text_table_id += 1

            "3 is referring to the third entry in attribute_type table which is synset_sumo"
            sql_cmnd = "INSERT INTO synset_attribute VALUES(" + str(synset_attribute_table_id) + "," + str(synset_table_id) + ",3," + str(synset_attribute) + ");"
            cursor.execute(sql_cmnd)
            synset_attribute_table_id += 1

        #------------------------------------------ senses
        for i in range(len(synsetWrds)):
            wrd = synsetWrds[i]

            if indexFileDictionary.has_key(wrd):
                data = index_line_format_process(indexFileDictionary[wrd].replace("\n", ""))
            elif indexFileDictionary.has_key(wrd.lower()):
                data = index_line_format_process(indexFileDictionary[wrd.lower()].replace("\n", ""))
            else:
                errorFile.write("%s from synset %d are not in the index file" % (wrd, synsetIndex + 1))
                print("%s or %s from synset %d are not in the index file" % (wrd, wrd.lower(), synsetIndex + 1))
                continue

            if data[0] == 'n':
                posTag = lang + " n"
            elif data[0] == 'v':
                posTag = lang + " v"
            elif data[0] == 'r':
                posTag = lang + " adv"
            elif data[0] == 'a':
                posTag = lang + " adj"
            else:
                posTag = "UNKNOWN"

            sensePos = str(pos_id[posTag])
            wrd_senses = data[1]
            sense_pointers = data[2]            # not sure if they are useful!!!

            if wrd not in insert_no_more:

                if wrd.find("(BR)") != -1:
                    word = wrd.replace("~(BR)", "")
                    txt_sql_cmnd_part2 = ",'Brazilian-Portuguese');"
                    #txt_sql_cmnd = "INSERT INTO text VALUES(" + str(text_table_id) + ",'Brazilian-Portuguese');"
                    #cursor.execute(txt_sql_cmnd)
                    #sense_attribute = text_table_id
                    #text_table_id += 1
                else:
                    word = wrd.replace("~(PT)", "")
                    txt_sql_cmnd_part2 = ",'no_sense_attribute for " + word.replace("'", "''") + "');"
                    #txt_sql_cmnd = "INSERT INTO text VALUES(" + str(text_table_id) + ",'no_sense_attribute for " + word.replace("'","''") + "');"
                    #cursor.execute(txt_sql_cmnd)
                    #sense_attribute = text_table_id
                    #text_table_id += 1

                word = word.replace("_", " ")  # there is "_" in Princeton data in multi word expressions

                # ---- table 1- word
                if "'" in wrd:
                    sql_cmnd = "INSERT INTO word VALUES(" + str(wrd_table_id) + ",'" + word.replace("'","''") + "'," + id_lexicon + ");"
                else:
                    sql_cmnd = "INSERT INTO word VALUES(" + str(wrd_table_id) + ",'" + word + "'," + id_lexicon + ");"
                cursor.execute(sql_cmnd)

                # ---- table 21-corpus_example
                if "'" in wrd:
                    sql_cmnd = "INSERT INTO corpus_example VALUES(" + str(wrd_table_id) + example + word.replace("'","''") + "]'," + str(wrd_table_id) + ");"
                else:
                    sql_cmnd = "INSERT INTO corpus_example VALUES(" + str(wrd_table_id) + example + word + "]'," + str(wrd_table_id) + ");"
                cursor.execute(sql_cmnd)

                if len(wrd_senses) > 1:
                    insert_no_more.add(wrd)

                # ---- table 12-sense
                sense_num = 1
                for wrd_sense in wrd_senses: # each word sense is the synset id it belongs to
                    sql_cmnd = "INSERT INTO sense VALUES(" + str(sense_table_id) + "," + str(sense_num) + "," + str(domain) + "," + str(
                        wrd_table_id) + ",'" + sensePos + "'," + id_lexicon + ");"
                    cursor.execute(sql_cmnd)

                    sense_num += 1

                    # ---- table 11-sense_attribute
                    txt_sql_cmnd = "INSERT INTO text VALUES(" + str(text_table_id) + txt_sql_cmnd_part2
                    cursor.execute(txt_sql_cmnd)
                    sense_attribute = text_table_id
                    text_table_id += 1

                    #2 is referring to the second entry in attribute_type table which is sense_comment"
                    sql_cmnd = "INSERT INTO sense_attribute VALUES(" + str(sense_attribute_table_id) + "," + str(
                        sense_table_id) + ",2," + str(sense_attribute) + ");"
                    cursor.execute(sql_cmnd)
                    sense_attribute_table_id += 1

                    if wrd_sense not in later_insert.keys():
                        later_insert.update({wrd_sense: [wrd + "##" + str(sense_table_id)]})
                    else:
                        if (wrd + "##" + str(sense_table_id)) not in later_insert[wrd_sense]:
                            later_insert[wrd_sense].append(wrd + "##" + str(sense_table_id))

                    sense_table_id += 1

                wrd_table_id += 1

        sense_relation_temp = []

        # ---- table 9-sense_to_synset
        working_indx = synset_table_id - synset_start
        synset_senses = later_insert[str(working_indx)]
        for synset_sense in synset_senses:
            wrd = synset_sense.split("##")[0]
            sense_id = int(synset_sense.split("##")[1])
            try:
                if lexicon == "2":
                    sense_index = synsetWrds.index(wrd) + 1
                else:
                    sense_index = synsetWrds.index(wrd)
            except:
                errorFile.write(" ***** couldn't find %s in synset %d in lexicon %d\n" % (wrd,working_indx,lexicon))
                print(" ***** couldn't find %s in synset %d in lexicon %d\n" % (wrd, working_indx, lexicon))
                continue

            sql_cmnd = "INSERT INTO sense_to_synset VALUES(" + str(sense_to_synset_table_id) + "," + str(
                sense_id) + "," + str(synset_table_id) + "," + str(sense_index) + ");"
            cursor.execute(sql_cmnd)
            sense_to_synset_table_id += 1

            sense_relation_temp.append(sense_id)      # to be used later for synonymy relation in sense relation table

        # ---- table 10-sense_relation   (Just synonymy)
        #this loop enters all synonymy relations among a synset words into sense_relation table
        if len(sense_relation_temp) > 1:
            for i in range(len(sense_relation_temp)):
                for j in range(i+1, len(sense_relation_temp)):
                    sql_cmnd = "INSERT INTO sense_relation VALUES(" + str(sense_relation_table_id) + "," + str(sense_relation_temp[i]) + "," + str(sense_relation_temp[j]) + "," + sense_relationType_id["=s"][1] + ");"
                    cursor.execute(sql_cmnd)
                    sense_relation_table_id += 1
                    sql_cmnd = "INSERT INTO sense_relation VALUES(" + str(sense_relation_table_id) + "," + str(sense_relation_temp[j]) + "," + str(sense_relation_temp[i]) + "," + sense_relationType_id["=s"][1] + ");"
                    cursor.execute(sql_cmnd)
                    sense_relation_table_id += 1

        synset_table_id += 1

        if lexicon == 2:
            print ("   en synset %d ... Done!" % (synsetIndex + 1))
        else:
            print ("   %s synset %d ... Done!" % (lang,synsetIndex + 1))


        #except:
        #    errorFile.write(" ***** problem in synset %d\n"%(synsetIndex))
        #    continue

    if lexicon != 2:
        path = os.getcwd() + '/data/dumps/' + db_name + "_dump_en_"+ lang +".sql"
        terminalCommand = " mysqldump --user=" + u + " --password=" + p + " " + db_name + " > " + path + ";"
        os.system(terminalCommand)
        time.sleep(20)

        text_update_func(cursor)
        allDone = True

    if allDone:
        # the tracker table
        sql_script_runner("tracker.sql", cursor, db_name, "$$")
        print("* Tracker tabeles... Done!")

        # a bunch of "ALTER" instructions
        sql_script_runner("alter.sql", cursor, db_name, ";")
        print("* All Alters ... Done!")

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    # to close the connection
    db.close()
    errorFile.close()

    print ("Done! :) ")

def insert_into_table_fromTablefile(table_name, cursor, text_update):

    fields_indx = set([])

    path = os.getcwd() + '/data/table_default_values/'

    inputFile = codecs.open(path + table_name, encoding='utf-8')
    tableData = inputFile.readlines()
    inputFile.close()

    if text_update == True:
        #number of entries in text table so far
        text_table_id = id_retrieve("text", "none", cursor,"table")
        txt_sql_cmnd = "INSERT INTO text VALUES(" + str(text_table_id + 1) + ","

        # to identify which fields are going to be stored in text table
        fields = tableData[0].split("\t")
        for i in range(len(fields)):
            if fields[i].find("(text)")!=-1:
                fields_indx.add(i)

    for i in range(1, len(tableData)):
        sql_cmnd = "INSERT INTO " + table_name + " VALUES("
        row = tableData[i]
        row = row.replace("\n","")
        fields = row.split("\t")
        if text_update == False:
            for j in range(len(fields)):
                sql_cmnd += fields[j] + ","
            sql_cmnd += ");"
            sql_cmnd = sql_cmnd.replace(",)",")")
            cursor.execute(sql_cmnd)
        else:
            for j in range(len(fields)):
                if j in fields_indx:
                    txt_sql_cmnd += "'" + fields[j] + "',"
                    sql_cmnd += str(text_table_id + 1) + ","
                    txt_sql_cmnd += ");"
                    txt_sql_cmnd = txt_sql_cmnd.replace(",)", ")")
                    txt_sql_cmnd = txt_sql_cmnd.replace("\\", "")
                    cursor.execute(txt_sql_cmnd)
                    text_table_id += 1
                    txt_sql_cmnd = "INSERT INTO text VALUES(" + str(text_table_id + 1) + ","
                else:
                    if table_name == "part_of_speech" and j == 3:
                        sql_cmnd += "'" + fields[j] + "',"
                    else:
                        sql_cmnd += fields[j] + ","
            sql_cmnd += ");"
            sql_cmnd = sql_cmnd.replace(",)", ")")
            cursor.execute(sql_cmnd)

            #if table_name == "relation_type":
            #    print(i)

def index_line_format_process(indxline):
    sense_pointers = []
    senses = []

    index_line_parts = indxline.split(" ")

    sensePos = index_line_parts[0]
    senseCnt = int(index_line_parts[1])
    sensePointerCnt = int(index_line_parts[2])

    if sensePointerCnt != 0:
        for i in range(3, 3 + sensePointerCnt):
            sense_pointers.append(index_line_parts[i])

        i += 3

        for j in range(i, i + senseCnt):
            senses.append(index_line_parts[j])
    else:
        for i in range(5, 5 + senseCnt):
            senses.append(index_line_parts[i])

    data = (sensePos,senses,sense_pointers)
    return data

def data_line_format_process(dataLine,lang, extra_data):
    # This function processes each line of a data file.
    # There are some extra information in Portuguese data file

    # <------ to be changed if there are extra information in data file. There is no need for any change,
    #  if the data file is completely compatible with Princeton format.

    synsetWrds = []
    synsetConnections = []
    synsetRelationTypes = []
    connectedSynsetPos = []

    toIgnore = set()                    # for entries that are already in the list with (PT) or (BR) tags

    dataLineParts = dataLine.split(" ")

    if dataLineParts[2] == 'n':
        thisSynsetPos = lang + " n"
    elif dataLineParts[2] == 'v':
        thisSynsetPos = lang + " v"
    elif dataLineParts[2] == 'r':
        thisSynsetPos = lang + " adv"
    elif dataLineParts[2] == 'a':
        thisSynsetPos = lang + " adj"

    wrdCnt = int(dataLineParts[3], 16)

    indx = 4
    for i in range(wrdCnt):
        if "~(PT)" in dataLineParts[indx] or "~(BR)" in dataLineParts[indx]:
            temp = dataLineParts[indx].replace("~(PT)", "")
            temp = temp.replace("~(BR)", "")
            toIgnore.add(temp)           #for cases where the tagged word is already entered  - tag = (PT)/(BR)

        if dataLineParts[indx] not in toIgnore:
            synsetWrds.append(dataLineParts[indx])
        indx += 2

    connCnt = int(dataLineParts[indx])
    indx += 1
    wrongSyns = ["0","N","W","P"]
    for i in range(connCnt):
        if dataLineParts[indx + 1][0] not in wrongSyns:
            synsetRelationTypes.append(dataLineParts[indx])
            indx += 1
            synsetConnections.append(dataLineParts[indx])
            indx += 1
            connectedSynsetPos.append(dataLineParts[indx])
            indx += 1
            # the next field is 0000 or 000 in portuguese wordnet which is not used in this code
            indx += 1
        else:
            indx += 4

    gloss = dataLine.split("|")[1]
    gloss = gloss.replace("\n","")
    gloss = gloss.replace("'","''")

    mapping = "NULL"
    pos = "NULL"
    domain = "NULL"
    sumo_type = "NULL"
    sumo_val = "NULL"
    comment = "NULL"

    if not extra_data:
        extra_info = (mapping, pos, domain, sumo_type, sumo_val, comment, gloss)
    else:
        gloss = gloss.replace("COMMENT ","")
        gloss = gloss.replace("'", "")
        gloss = gloss.split(" ")
        if gloss[1] != "UNMAPPED":
            mapping = gloss[1]
        pos = gloss[2]
        domain = gloss[3]
        sumo_type = gloss[4]
        sumo_val= gloss[5]
        if len(gloss) > 6 :
            comment = "'" + gloss[6] + "'"
        definition = "no definition"
        extra_info = (mapping,pos,domain,sumo_type,sumo_val,comment,definition)
    data = (thisSynsetPos, synsetWrds, synsetConnections, synsetRelationTypes, connectedSynsetPos, extra_info)

    return data

def id_retrieve(table_name, search_str, cursor, search_for):
    if search_for == "table":
        # returns number of entries in the table
        txt_sql_cmnd = "select count(*) from " + table_name + ";"
        cursor.execute(txt_sql_cmnd)
        data = cursor.fetchall()
        text_table_id = data[0][0]
    else:
        # returns the id where the string has appeared in text table
        txt_sql_cmnd = "select * from text where text = '" + search_str + "';"
        cursor.execute(txt_sql_cmnd)
        data = cursor.fetchall()
        text_table_id = data[0][0]
    return text_table_id

def relationType_id_extraction(cursor, lang):

    path = os.getcwd() + '/data/table_default_values/relation_symbols'
    relFile = open(path)
    rel = relFile.readlines()
    relFile.close()

    relAbr = {}
    for line in rel:
        temp = line.replace("\n","")
        temp = temp.split("\t")
        relAbr.update({temp[0]:temp[1]})

    synset_relationType_id = {}
    sense_relationType_id = {}

    #to retrieve all the ralation names
    sql_cmnd = "select text.text from text, relation_type where relation_type.name = text.id;"
    cursor.execute(sql_cmnd)
    relation_names = cursor.fetchall()

    # to retreive all the ralation short_display_text
    sql_cmnd = "select text.text from text, relation_type where relation_type.short_display_text = text.id;"
    cursor.execute(sql_cmnd)
    relation_shortText = cursor.fetchall()

    # to replace the short_display_text with relation symbols
    relation_symbols = []
    for i in range(len(relation_shortText)):
        relation_symbols.append(relAbr[relation_shortText[i][0]])

    for i in range(len(relation_names)):
        if relation_names[i][0].find(lang +"_syn_") != -1:
            synset_relationType_id.update({relation_symbols[i]: (relation_names[i][0], str(i+1))})
        elif relation_names[i][0].find(lang + "_sns_") != -1 or relation_names[i][0].find(lang +"_Synonym") != -1:
            sense_relationType_id.update({relation_symbols[i]: (relation_names[i][0], str(i + 1))})


    return synset_relationType_id, sense_relationType_id

def pos_id_extraction(cursor):
    pos_id = {}

    # to retreive all the pos names
    sql_cmnd = "select text.text, part_of_speech.id from text, part_of_speech where part_of_speech.name = text.id;"
    cursor.execute(sql_cmnd)
    pos_info = cursor.fetchall()

    for i in range(len(pos_info)):
        posName = pos_info[i][0]
        posId = pos_info[i][1]
        pos_id.update({posName: posId})

    return (pos_id)

def domain_id_extraction(cursor):
    domain_id = {}

    # to retreive all the pos names
    sql_cmnd = "select text.text, domain.id from domain,text where text.id = domain.name;"
    cursor.execute(sql_cmnd)
    domain_info = cursor.fetchall()

    for i in range(len(domain_info)):
        domainName = domain_info[i][0]
        domainId = domain_info[i][1]
        domain_id.update({domainName: domainId})

    return (domain_id)

def sql_script_runner(fileName, cursor, db_name, endChar):
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

def text_update_func(cursor):
    #this function updates the text in text table (relation description and relation tsts)

    path = os.getcwd() + '/data/table_default_values/'

    file_name = ["relationTests-wordnetLoom","relationDescription-wordnetLoom"]
    keyWrd = ["#tst:","#txt:"]

    for flIndx in range(len(file_name)):
        fl = file_name[flIndx]
        key = keyWrd[flIndx]

        srcF = codecs.open(path + fl, encoding='latin')
        def_tst = srcF.readlines()
        srcF.close()

        i = 0
        line = def_tst[i].replace("\r", "")
        line = line.replace("\n", "")
        while i < len(def_tst):
            search_str = line.split(":")[1]
            print("\n" + search_str)
            txt_sql_cmnd = "select * from text where text = '" + search_str + "';"
            cursor.execute(txt_sql_cmnd)
            data = cursor.fetchall()
            id = data[0][0]

            temp = []
            i += 1
            line = def_tst[i].replace("\r", "")
            line = line.replace("\n", "")
            line = line.replace("'", "")
            line = line.replace(",", "")
            while i < len(def_tst) and key not in line:
                temp.append(line)
                i += 1
                if i < len(def_tst):
                    line = def_tst[i].replace("\r", "")
                    line = line.replace("\n", "")

            desc = "concat_ws('\n',text"
            for itm in temp:
                desc += ",'" + itm + "'"
            desc += ")"
            sql_cmnd = "UPDATE text SET text= " + desc + " WHERE id =" + str(id) + ";"
            cursor.execute(sql_cmnd)

def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")
