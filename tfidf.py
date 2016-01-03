import string
import collections
import sys
from os import listdir
from os.path import isfile, join


def process(filepath):
    with open(filepath, 'rU') as infile:
        cnt = collections.Counter()
        for line in infile:
            if len(line.strip()) > 2:
                if "Title" in line:
                    getTitle(line)
                else:
                    words = preprocess(line)
                    for word in words:
                        cnt[word] += 1            
        max = cnt.most_common(1)
        cnt.update({k: divide(v, max) for k, v in cnt.items()})
        average_tfidf = sum(cnt.values()) / len(cnt)
        print average_tfidf, ",", len(cnt)
        cnt.clear()

def getTitle(titleLine):
    split = titleLine.split(":")
    titleWords = split[1].strip()
    print titleWords
    

def preprocess(sentence):
    out = sentence.translate(string.maketrans("",""), string.punctuation)
    out = out.lower()
    return out.split()

def divide(freq, max):
    number = max[0]
    return 0.5 + (0.5*(freq)/number[1])
    
def main():
    input_directory = sys.argv[1]
    allbooks = [ f for f in listdir(input_directory) if isfile(join(input_directory, f)) and "txt" in f]
        # for folder in allbooks:
        #files = [fi for fi in listdir(join(input_directory,folder))]
    for file in allbooks:
        process(join(input_directory,file))

main()