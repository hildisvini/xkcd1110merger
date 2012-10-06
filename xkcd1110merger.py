#!/usr/bin/python
#-*- coding: utf-8 -*-

from urllib2 import Request, urlopen, URLError, HTTPError
from urllib import urlretrieve
import os
import sys
import time
from PIL import Image
import re


def getSinglePart(url, imageName, directory):
    
    imageUrl = url + imageName

    req = Request(imageUrl)

    try: response = urlopen(req)
    
    except HTTPError, e:
         print e.code, imageName
         return 0
    except URLError, e:
         print e.reason, imageName
         return 0
    else:
         data = response.read()
         
    try:
        urlretrieve(imageUrl, directory + imageName)   
    except: 
        print '--> failed ' + imageName + '!'


def downloadImages(url, directory):
    for w in range(50): # the maximal part position number is 48
        w += 1
        for n in range(50):
            n += 1
            imageName = str(n) + 'n' + str(w) +  'w' + '.png'
            getSinglePart("%s" % (url), imageName, directory)
            
            imageName = str(n) + 's' + str(w) +  'w' + '.png'
            getSinglePart("%s" % (url), imageName, directory)
            
            imageName = str(n) + 'n' + str(w) +  'e' + '.png'
            getSinglePart("%s" % (url), imageName, directory)
            
            imageName = str(n) + 's' + str(w) +  'e' + '.png'
            getSinglePart("%s" % (url), imageName, directory)
            
            time.sleep(1) # saves from connection issues
            

def resizeParts(directory, partSize, resizedTo):
    parts = os.listdir(directory)
    
    if not os.path.exists(directory + resizedTo): # checks, if directory for saving resized parts exists
        os.makedirs(directory + resizedTo)

    for part in parts: # for each file in directory: open, resize and save again
        try:
            i = Image.open(directory + part)
            i = i.resize ((partSize, partSize), Image.ANTIALIAS)
            i.save(directory + resizedTo + part, 'PNG')
            
        except IOError:
            pass
            
    print 'Image parts resized successfully!'
    


def mergeParts(directory, partSize, resizedTo):
    
    resizedTo = 'resized_to_%s/' %partSize # name, the directory where resized parts are stored
    
    imgHeight = partSize * (13 + 19 + 1) # max north and south image positions 
    imgWidth = partSize * (33 + 48 +1) # max east and west image positions 
    
    img = Image.new('1', (imgWidth, imgHeight)) # creates a background image for merging
    
    parts = os.listdir(directory + resizedTo)
    
    for part in parts:
        i = Image.open(directory + resizedTo + part)      
        
        # gets coordinates of a single part from the filename
        n = re.findall('([0-9]+)([a-z])([0-9]+)([a-z])', part) 
        
        if n[0][1] == 'n': 
            y = 256*(14 - int(n[0][0]))
        else: 
            y = 256*(13 + int(n[0][0]))
        
        if n[0][3] == 'w': 
            x = 256*(34 - int(n[0][2]))
        else: 
            x = 256*(33 + int(n[0][2]))
  
        img.paste(i, (x, y))

    img.save(directory+'xkcd.png') 

    print 'Image parts merged successfully!' 



if __name__ == "__main__":
    url = 'http://imgs.xkcd.com/clickdrag/'
    partSize = 256 # resize original image parts to this size.
    directory = 'tmp/'
    
    if not os.path.exists(directory): # checks, if directory for saving parts exists
        os.makedirs(directory)
    
    resizedTo = 'resized_to_%s/' %partSize # name, the directory where resized parts are stored   
        
    downloadImages(url, directory)
    resizeParts(directory, partSize, resizedTo)
    mergeParts(directory, partSize, resizedTo)
