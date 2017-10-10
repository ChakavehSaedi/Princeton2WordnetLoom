# coding=utf-8
#! /usr/bin/env python2.7

"""
This codes creats the wordnet index file based on the input data file
NOTE: it does not decapotalize or sort the result as the English Princeton index file format states.

2017 Chakaveh Saedi <chakaveh.saedi@di.fc.ul.pt>

"""

import codecs
import os

def index_creator(inputFileName,lexicon, data_folder):
    if lexicon == 1:
        dataPath = os.getcwd() + '/data/'+ data_folder +'/'
    else:
        dataPath = os.getcwd() + '/data/en_wnet/'

    inputFile = codecs.open(dataPath + inputFileName[0], encoding='utf-8')
    src = inputFile.readlines()
    inputFile.close()

    outputFile = codecs.open(dataPath + inputFileName[1], "w", encoding='utf-8')

    seenWrds = set()
    wrdsInfos = {}

    commnt_cnt = 0
    i = 0
    while src[i][:2] == "  ":
        commnt_cnt += 1
        i += 1


    print ("* processing the data file")

    for i in range(commnt_cnt,len(src)):
        lineParts = src[i].split(" ")
        cur_synset = lineParts[0]
        cur_synset_pos = lineParts[2]

        cur_synset_wrdNum = int(lineParts[3], 16)

        cur_synset_wrds = []
        cur_synset_conTypes = []
        cur_synset_conSynset = []
        cur_synset_conPos = []

        "senses"
        indx = 4
        for cnt in range(cur_synset_wrdNum):
            cur_synset_wrds.append(lineParts[indx])
            indx += 2

        cur_synset_conNum = int(lineParts[indx])
        indx += 1

        "connected synsets"
        for cnt in range(cur_synset_conNum):
            cur_synset_conTypes.append(lineParts[indx])
            indx += 1

            cur_synset_conSynset.append(lineParts[indx])
            indx += 1

            cur_synset_conPos.append(lineParts[indx])
            indx += 2

        for wrd in cur_synset_wrds:
            if wrdsInfos.has_key(wrd):
                for conType in cur_synset_conTypes:
                    wrdsInfos[wrd][1].add(conType)
                wrdsInfos[wrd][2].append(cur_synset)
            else:
                ctype = set()
                for conType in cur_synset_conTypes:
                    ctype.add(conType)
                key = wrd
                info = [cur_synset_pos, ctype, [cur_synset]]    # [pos, connection_types, List of synsets]
                wrdsInfos.update({key:info})

    print ("   \n%d words extracted\n"%(len(wrdsInfos.keys())))
    cnt = 1

    print("* creating index file!")

    for key in wrdsInfos.keys():

        temp = key + " " + wrdsInfos[key][0] + " " + str(len(wrdsInfos[key][2])) + " " + str(len(wrdsInfos[key][1])) + " "
        for conType in wrdsInfos[key][1]:
            temp += conType + " "
        temp += str(len(wrdsInfos[key][2])) + " 0 "
        for synset in wrdsInfos[key][2]:
            temp += synset + " "

        temp += "\n"
        temp = temp.replace(" \n", "\n")

        outputFile.write(temp)

        cnt += 1

    return(commnt_cnt)