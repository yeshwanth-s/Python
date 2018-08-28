from urllib.request import urlopen
from urllib.error import HTTPError
from bs4    import BeautifulSoup
import nltk
import re
from nltk.tokenize import word_tokenize

def extract(url):
    try:
        html = urlopen(url)
        return html
    except HTTPError as e:
        print(e)
        return None

def beauty_soap(extr_url):
    try:
        bs = BeautifulSoup(extr_url,"lxml")
        para = bs.findAll("p")
        fh1 = bs.find("h1", {"id": "firstHeading"})
        return para,fh1
    except AttributeError as e:
        print(e)
        return None

def firstHeading(extr_url):

    try:
        bs = BeautifulSoup(extr_url,"lxml")
        fh1 = bs.find("h1",{"id":"firstHeading"})
        return fh1
    except AttributeError as e:
        print(e)
        return None

def nltk_para_alyzer(para,fh1):
    if para != "":
        extr_para = str(para)
        extr_para = re.sub(
            '<.*?>|[\[]([0-9_]+)[\]]|\,|\(|\)|\,|"|\'|\:|\;|\<|\>|\-|\=|\=|-|_|\.|\/|\!|\@|\#|\$|\%|\^|\&\|\*',
            "", extr_para)
        extr_para = re.sub('[\[]\w*\s\w*[\]]', "", extr_para)

        if fh1 != "":
            extr_para_h1 = str(fh1)
            extr_para_h1 = re.sub('<.*?>', "", extr_para_h1)


    return extr_para,extr_para_h1

def freq_dis(extr_para):
    word = word_tokenize(extr_para)
    nt = nltk.Text(word)
    fq = nltk.FreqDist(nt)
    print("Frequency of words:", fq.most_common(10))

url = input("Enter the URL:")
extr_url = extract(url)
bea_soap, fh1 = beauty_soap(extr_url)
extr_para, fh1 = nltk_para_alyzer(bea_soap,fh1)
print("Extracted Paragraph", extr_para)
print("First Heading: ", fh1)

freq_dis(extr_para)


