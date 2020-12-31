#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

#yes, python2. screw you, guys, you can't "deprecate" a programming language

import urllib2,json,os,re,requests
import errno
from datetime import datetime

STARTPOINT="https://lobby.maps.at.rc3.world/main.json"
MAPSONLY=r'://[^/]+\.maps\.at\.rc3\.world/' # or False to consume everything
TARGETDIR="output"



def lh(txt): #lineheading
	while len(txt)<9:
		if len(txt)%2:
			txt=" " + txt
		else:
			txt=txt + " "

	return datetime.now().strftime("%H:%M:%S")+" ["+txt+"]  "
	
	
def getfile(url):
	return urllib2.urlopen(urllib2.quote(url).replace('%3A',':',1)).read() #yes, this sux, too lazy

def url2path(url):
	url=url.split('://')
	if len(url) < 2 or not url[1]:
		return None
	url=re.sub('\.+','.',url[1]) #safety third
	return url

def item_generator(json_input, keys):
    if isinstance(json_input, dict):
        for k, v in json_input.iteritems():
            if k in keys:
				if isinstance(v,str) or isinstance(v,unicode):
					yield v
            else:
                for child_val in item_generator(v, keys):
                    yield child_val
    elif isinstance(json_input, list):
        for item in json_input:
            for item_val in item_generator(item, keys):
                yield item_val

def getlinksfrom(json):
	a = []
	for x in item_generator(json,['value','image']):
		a.append(x.encode('utf-8'))
	return a

def process(url, path=""):
	url=requests.compat.urljoin(url,path).split("#")[0]
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
		else:
			raise

	with open(TARGETDIR+"/"+savepath,"wb") as f:
		f.write(data)

	print lh("OK")+"Successfully wrote " + savepath
	
	if os.path.splitext(url)[1].lower()=='.json':
		try:
			data = json.loads(data)
		except:
			print lh("ERROR")+"bad json data or something at " +url
			return False
			
		links=getlinksfrom(data)

		for link in links:
			if not MAPSONLY or link.find('://')==-1 or re.findall(MAPSONLY,link):
				process(url,link)
			else:
				print lh("SKIP")+"Refusing to process remote "+link

	return True

process(STARTPOINT)
