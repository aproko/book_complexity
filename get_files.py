import urllib2
import urllib
import zipfile
import tfidf
import os
from os.path import join
from bs4 import BeautifulSoup

#TODO:
#make count input argument (how many books to process)
#add support for special chars - i.e. translate weird chards to English
#separate out so we can just download the files and get the .txt versus processing everything

response = urllib2.urlopen('http://www.gutenberg.org/robot/harvest?filetypes[]=txt&langs[]=en')
html = response.read()

soup = BeautifulSoup(html, 'html.parser')
links = soup.find_all('a')
count = 0      
for link in links:
    if count < 5:
        url = link.get('href')
        tmp_fn = url.split("/")
        filename = tmp_fn[len(tmp_fn)-1]
        if ("zip" in url and "etext" not in url and "-8" not in url):
            urllib.urlretrieve(url, filename)
            zip = zipfile.ZipFile(filename)
            zip.extractall()
            txt_filename = filename.replace(".zip", ".txt")
            if os.path.isfile(txt_filename):
                tfidf.getWordCounts(txt_filename)
            elif os.path.isdir(txt_filename.replace(".txt","")):
                actual_filename = join(txt_filename.replace(".txt", ""),txt_filename)
                tfidf.getWordCounts(actual_filename)
                os.rmdir(txt_filename.replace(".txt",""))
            os.remove(filename)
            count += 1
        elif "offset" in url:
            url = "http://www.gutenberg.org/robot/"+url
            new_response = urllib2.urlopen(url)
            new_html = new_response.read()
            new_soup = BeautifulSoup(new_html, 'html.parser')
            links.extend(new_soup.find_all('a'))
        

tfidf.calcTfidf(".")



