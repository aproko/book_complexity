import urllib2
import urllib
import zipfile
from bs4 import BeautifulSoup

response = urllib2.urlopen('http://www.gutenberg.org/robot/harvest?filetypes[]=txt&langs[]=te')
html = response.read()

soup = BeautifulSoup(html, 'html.parser')
for link in soup.find_all('a'):
    url = link.get('href')
    tmp_fn = url.split("/")
    filename = tmp_fn[len(tmp_fn)-1]
    if "zip" in url:
        urllib.urlretrieve(url, filename)
        zip = zipfile.ZipFile(filename)
        zip.extractall()

        