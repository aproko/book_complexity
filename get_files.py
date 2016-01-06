import urllib2
import urllib
import zipfile
import tfidf
import os
import sys
from os.path import join
from bs4 import BeautifulSoup

#So now you can either download in a batch or download one by one and generate the counts files on the fly (if downloading very large amounts of text)
#TODO:
#X:make count input argument (how many books to process)
#add support for special chars - i.e. translate weird chards to English
#X:separate out so we can just download the files and get the .txt versus processing everything
#X:add option to read initial URL from file (so I can have my own list of URLs for toy example with genres)
#http://www.gutenberg.org/robot/harvest?filetypes[]=txt&langs[]=en

#how many books to process
maxcount = int(sys.argv[1])
#option is to either download or all
mode = sys.argv[2]
#file which contains the URL to mine (urls.md - don't save as txt file or program will attempt to read it during the analysis)
urlfile = sys.argv[3]

def processFile(filename):
    txt_filename = filename.replace(".zip", ".txt")
    if os.path.isfile(txt_filename):
        tfidf.getWordCounts(txt_filename)
    elif os.path.isdir(txt_filename.replace(".txt","")):
        actual_filename = join(txt_filename.replace(".txt", ""),txt_filename)
        tfidf.getWordCounts(actual_filename)
        os.rmdir(txt_filename.replace(".txt",""))


def downloadLink(url):
    tmp_fn = url.split("/")
    file_name = tmp_fn[len(tmp_fn)-1]
    
    #To make sure we're extracting only zip files that in the right format
    if ("zip" in url and "etext" not in url and "-8" not in url):
        urllib.urlretrieve(url, file_name)
        zip = zipfile.ZipFile(file_name)
        zip.extractall()
        os.remove(file_name)
        if "all" in mode:
            processFile(file_name)
        else:
            print file_name
        return 1
    else:
        return 0
        

def readInUrlFile(url_file):
    with open(url_file, 'rU') as u_file:
        cn = 0
        for line in u_file:
            if "robot" in line:
                response = urllib2.urlopen(line)
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser')
                links = soup.find_all('a')
                for link in links:
                    if cn < maxcount:
                        link_url = link.get('href')
                        if "offset" in link_url:
                            link_url = "http://www.gutenberg.org/robot/"+link_url
                            new_response = urllib2.urlopen(url)
                            new_html = new_response.read()
                            new_soup = BeautifulSoup(new_html, 'html.parser')
                            links.extend(new_soup.find_all('a'))
                        else:
                            cn += downloadLink(link_url)
            else:
                if cn < maxcount:
                    cn += downloadLink(line)

def main():
    readInUrlFile(urlfile)

if __name__ == "__main__":
    main()




