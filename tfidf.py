import string
import math
import collections
import sys
import os
from os import listdir
from os.path import isfile, join
import graph_tfidf
import numpy as np


#TODO:
#add genres for color coding?
#removing all punctuation gives us 'youre' and run-on words like 'MrBlah', etc
#option to write vocabulary big counts table to file?

vocabulary = {}
input_x = []
input_y = []
titles = []



def addtovocab(input_countfile, input_filenumber, numberOfFiles):
    with open(input_countfile, 'rU') as input_countf:
        for count_line in input_countf:
            word_and_count = count_line.split(",")
            vocab_word = word_and_count[0]
            if vocab_word in vocabulary:
                old_counts = vocabulary[vocab_word]
            else:
                old_counts = [0] * numberOfFiles
            old_counts[input_filenumber] = 1
            vocabulary[vocab_word] = old_counts

#First processes each file to add all of its vocabulary counts to the main vocabulary table;
#then calculates the tf-idf score for each document.
def calcTfidf(in_directory):
    allcounts = [ a for a in listdir(in_directory) if isfile(join(in_directory, a)) and "counts" in a ]
    numFiles = len(allcounts)
    filecount = 0
    for countfile in allcounts:
        addtovocab(countfile, filecount, numFiles)
        filecount += 1
    for again_countfile in allcounts:
        cntr = collections.Counter()
        with open(again_countfile, 'rU') as again_count:
            for wordAndCount in again_count:
                wAndC = wordAndCount.split(",")
                cntr[wAndC[0]] = int(wAndC[1])
        max = cntr.most_common(1)
        input_x.append(sum(cntr.values()))
        #input_x.append(len(list(cntr)))
        input_y.append(len(list(cntr)))
        cntr.update({k: tf(v, max) for k, v in cntr.items()})
        cntr.update({k1: idf(k1, v1, numFiles) for k1, v1 in cntr.items()})
        average_tfidf = sum(cntr.values()) / len(cntr)
#input_y.append(average_tfidf)
        titles.append(again_countfile.replace("_counts.txt", ""))
        cntr.clear()

#Generates a file with word counts
def getWordCounts(filepath):
    print filepath
    gotTitle = 0
    title = ""
    with open(filepath, 'rU') as infile:
        cnt = collections.Counter()
        for line in infile:
            if len(line.strip()) > 2:
                if "Title" in line and (gotTitle == 0):
                    title = getTitle(line)
                    gotTitle = 1
                else:
                    words = preprocess(line)
                    for word in words:
                        cnt[word] += 1            
    with open(title+".counts", 'w') as out:
        for k, v in cnt.iteritems():
            out.write(",".join([str(k),str(v)]))
            out.write("\n")
    #os.remove(filepath)
    cnt.clear()

def getTitle(titleLine):
    split = titleLine.split(":")
    titleWords = split[1].strip()
    return titleWords
    
def preprocess(sentence):
    out = sentence.translate(string.maketrans("",""), string.punctuation.replace("'", ""))
    out = out.lower()
    return out.split()

def tf(freq, max):
    number = max[0]
    return 0.5 + (0.5*(freq)/number[1])

def idf(word_value, tf_value, numberOfFiles):
    idf_value = math.log(numberOfFiles/sum(vocabulary[word_value]))
    return tf_value * idf_value

def testPrint():
    for idx, val in enumerate(titles):
        print val, ",", input_x[idx], ",", input_y[idx]

def graph():
    graph_tfidf.graph(input_x, input_y, titles)
    
def main():
    #This is if you've already downloaded all the txt files and are running the tfidf.py script with get_files.py
    input_directory = sys.argv[1]
    #mode is either genCounts or tfidf or all
    mode = sys.argv[2]
    #graph or print results option
    display = sys.argv[3]
    if ("genCounts" in mode or "all" in mode):
        allbooks = [ f for f in listdir(input_directory) if isfile(join(input_directory, f)) and "txt" in f ]
        for file in allbooks:
            getWordCounts(join(input_directory,file))
    if ("tfidf" in mode or "all" in mode):
        calcTfidf(input_directory)

    if "graph" in display:
        graph()
    elif "print" in display:
        testPrint()

if __name__ == "__main__":
    main()