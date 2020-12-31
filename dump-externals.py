#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

#yes, python2. screw you, guys, you can't "deprecate" a programming language


#WARN - this is very slow is servers are nonresponding; hangs indefinetely on streams

import urllib2,json,os,re,requests
import errno
from datetime import datetime

SOURCEFILE="external_urls.txt"
TARGETDIR="externals"



def lh(txt): #lineheading
	while len(txt)<9:
		if len(txt)%2:
			txt=" " + txt
		else:
			txt=txt + " "

	return datetime.now().strftime("%H:%M:%S")+" ["+txt+"]  "
	
	
def getfile(url):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0')]
	return opener.open(url).read()

def url2path(url):
	url=url.split('://')
	if len(url) < 2 or not url[1]:
		return None
	url=re.sub('\.+','.',url[1]) #safety third
	return url


def getsave(url):
	url=url.split("#")[0]
	print lh("PENDING")+"Processing "+url
	
	savepath = url2path(url)
	if savepath is None: #wasnt a real url
		print lh("NOPE")+"That wasn't a real URL"
		return False

	if savepath.find('/')==-1:
		savepath += "/"
		
	if(os.path.normpath(os.path.dirname(savepath)) == os.path.normpath(savepath)):
		savepath += "/"+"_index"

	if os.path.exists(TARGETDIR+"/"+savepath):
		print lh("DUPE")+"File "+savepath+" already exists"
		return True
		
	try:
		data = getfile(url)
	except:
		print lh("NOPE")+"oh, crap, no "+url+" for you."
		return False
	


	folder=TARGETDIR+"/"+os.path.dirname(savepath)
	
	try:
		os.makedirs(folder)
	except OSError as e:
		if e.errno == errno.EEXIST and os.path.isdir(folder):
			pass
		elif e.errno == errno.EEXIST:
			os.rename(folder, folder+"_____index")
			os.makedirs(folder)
			os.rename(folder+"_____index", folder + "/_index" )
			if os.path.exists(TARGETDIR+"/"+savepath):
				print lh("DUPE")+"File "+savepath+" already exists (double checked)"
				return True
		else:
			raise



	with open(TARGETDIR+"/"+savepath,"wb") as f:
		f.write(data)

	print lh("OK")+"Successfully wrote " + savepath

	return True

with open(SOURCEFILE) as source:
    for link in source.readlines():
        getsave(link.strip())
