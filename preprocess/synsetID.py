# coding=utf-8
#! /usr/bin/env python2.7

"""
This code creates a mapping file to replace the synset offsets included in wordnet data and index files with increnental
numbers starting from 1.
Then it replaces all the occurrences of old offsets with the new numbers in both data and index files.

2017 Chakaveh Saedi <chakaveh.saedi@di.fc.ul.pt>
"""

import os
import codecs

def offset_replace(inputFileName, mapTag, newWordnet, lexicon, commnt_cnt,data_folder):
    #mapTag = mapTag.replace(" ","")
    if newWordnet == True:
        print("\n* creating mapping file")

        if lexicon == 1:
            dataPath = os.getcwd() + '/data/' + data_folder +'/'
        else:
            dataPath = os.getcwd() + '/data/en_wnet/'

        inputFile = codecs.open(dataPath + inputFileName[0], encoding='utf-8')
        src = inputFile.readlines()
        inputFile.close()

        #to create the mapping file
        mapFile = open(dataPath + "mapp_" + mapTag.replace(" ","") + ".txt",'w')

        for i in range(commnt_cnt,len(src)):
            lineParts = src[i].split(" ")
            offset_old = lineParts[0]
            offset_new = i-commnt_cnt+1
            mapFile.write("%s %d\n"%(offset_old,offset_new))
        mapFile.close()

        print("   ... Done!")

        #-------------------------------------------------
        print("\n* Offset mapping ... it may take a while")

        print("  editing data file")

        #to edit the files
        mapF = open(dataPath + "mapp_" + mapTag.replace(" ","") + ".txt")
        mapping = mapF.readlines()
        mapF.close()

        #output data file
        outputFile = codecs.open (dataPath + "wnl_" + inputFileName[0],'w',encoding= 'utf-8')
        cnt = 1
        for mapp in mapping:
            mapp = mapp.replace("\n","")
            mapData = mapp.split(" ")
            old = mapData[0] + mapTag
            new = mapData[1] + mapTag
            for i in range(commnt_cnt,len(src)):
                if src[i].find(mapData[0],0,len(mapData[0])) == 0:
                    src[i] = src[i].replace(mapData[0],mapData[1],1)
                src[i] = src[i].replace(old,new)
            cnt += 1

        for i in range(commnt_cnt,len(src)):
            outputFile.write(src[i])
        outputFile.close()

        print("   ... Done!")

        print("  editing index file")

        #output index file
        inputFile = codecs.open(dataPath + inputFileName[1],encoding='utf-8')
        src = inputFile.readlines()
        inputFile.close()

        outputFile = codecs.open(dataPath + "wnl_" + inputFileName[1],'w',encoding= 'utf-8')
        for mapp in mapping:
            mapp = mapp.replace("\n", "")
            mapData = mapp.split(" ")
            old = mapData[0]
            new = mapData[1]
            for i in range(len(src)):
                src[i] = src[i].replace(old,new)

        for i in range(len(src)):
            outputFile.write(src[i])
        outputFile.close()
        print("   ... Done!")



