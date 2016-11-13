from bs4 import BeautifulSoup
import urllib2
import os,re,sys

def getLink(link,url):
    link = str(link.get('href'))
    if 'http' in link:
        fullLink = link
    else:
        fullLink = 'http://www.onehourheatandair.com/'+ link
    #print(fullLink)
    return(fullLink)


def getContent(fullLink):
    text = False
    try:
        url = fullLink
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(url,headers=hdr)
        content =  urllib2.urlopen(req).read()
        soup = BeautifulSoup(content,"html.parser")


        #content = urllib2.urlopen(fullLink).read()
        #soup = BeautifulSoup(content,"html.parser")
        #soup.i.extract()
        text = soup.find("div", { "class" : "post-view" })
        text = re.sub('<[^<]+?>', '', str(text))
        print('got 1')
    except Exception as err:
        print('failed 1')
        pass
    return(text)

def outToArticle(text,fileName):
    with open(fileName, 'a') as file:
        file.write(str(text))

if __name__ == "__main__":
    fileName = '/Users/danrusu/code/contentScraper/articles/hvac2.txt'
    numPages = 15
    innerpages = True

    for i in range(1,numPages+1):
        url = 'https://www.hvac.com/blog/page/'+str(i)
        #url = 'http://www.onehourheatandair.com/blog'
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(url,headers=hdr)
        content =  urllib2.urlopen(req).read()
        soup = BeautifulSoup(content,"html.parser")
        if innerpages:
            #for link in soup.find_all("a", { "class" : "more" }):
            for link in soup.find_all('a'):
                try:
                    #print(link)
                    fullLink = getLink(link,url)
                    text = getContent(fullLink)
                    if text:
                        outToArticle(text,fileName)
                except Exception as err:
                    print(err)
                print('done 1 article')
            print('COMPLETED: ' + url)
                #break
        else:
            try:
                text = getContent(url)
                outToArticle(text,fileName)
            except Exception as err:
                print(err)
            print('done 1 article')
        print('COMPLETED: ' + url)
