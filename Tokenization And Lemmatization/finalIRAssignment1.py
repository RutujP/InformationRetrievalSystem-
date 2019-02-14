# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 11:42:49 2018

@author: Rutuj
"""

import os
import sys
import glob
from datetime import datetime
from nltk.tokenize import word_tokenize
from xml.dom import minidom
from collections import Counter
import string
import collections
from nltk.stem import PorterStemmer
#from nltk.corpus import stopwords



#if not hasattr(sys, 'argv'):
 #   sys.argv  = ['']

startprogram= datetime.now()
tokenizer=[]

count=0


#def striphtml(data):
 #   p = re.compile(r'<.*?>')
  #  return p.sub('', data)

######## Used for parsing files and only carries the text content#################
def parse(file):
   doc = minidom.parse(file)
   d = doc.getElementsByTagName('TEXT')
   text = d[0].firstChild.data
   #print(text)
   return text
    
#removes all kind of punctuation

def removepunctuation(data):
    
    data = str.maketrans(({key: None for key in string.punctuation}))
    new_s = t.translate(data)
   # data=[l.strip(',') for l in data ]
   # data=[l.strip('.') for l in data]
    #data=[l.strip('') for l in data]
    return new_s
    
tokens=[]

paths='C:\\Users\\Rutuj\\Desktop\\IR FILES\\Cranfield\\*'

#pathname=sys.argv[1]
pathname = os.path.join(paths)
#print (pathname)
files=glob.glob(pathname)
for i in range(0,len(files)):
    t = parse(files[i])
    
    #s = "string. With. Punctuation?"
    
    #print(new_s)
    removepunc= removepunctuation(t)
    tokenizer= word_tokenize(removepunc)
    #print(tokenizer)
    temp = [ i for i in tokenizer if not i.isnumeric()]
    tokens.extend(temp)
    #cfreq=freq(tokenizer)
     #tokenizer funcn append
    #print(removepunc)
    count+=len(tokenizer)
print("the count of tokens are \n"+str(count))

un=0
i=0
j=0
#print("the tokens are "+str(tokens))
unqlist=Counter(tokens)
for i in tokens:
    if unqlist[i]==1:
        un=1
        j+=1
    else:
        un=0;
unique_words=set(tokens)
print("the count of unique words \n"+str(len(unique_words))) 
print("the count of unique tokens \n"+str(j))

word_frequency = collections.Counter(tokens).most_common(30) 
for i in word_frequency:
   print(i) 
#print("the tokens per document \n"+str(round(count/len(files))))  

progstop=datetime.now()
print("the program running time is \n"+str(progstop-startprogram))



stemmer=[]
counter=0
K=0
ps=PorterStemmer()
for i in tokens:
    stemmer.append(ps.stem(i))
    counter+=1

#print("the stem list is \n"+str(set(stemmer)))
print("the length of stems \n"+str(len(set(stemmer))))


#for word in stemmer:
#    if word in stopwords.words('english'):
 #       stemmer.remove(word)
        
#filtered_words=[word for word in stemmer if word not in stopwords.words('english') ]
#stemmer.extend(filtered_words)






stemlist=Counter(stemmer)
for i in stemmer:
    if stemlist[i]==1:
        flag=1
        K+=1
    else:
        flag=0
print("the count of unique stems is \n"+str(K))

#stem_frequency=collections.Counter(filtered_word_list).most_common(30)
stem_frequency=collections.Counter(stemmer).most_common(30)
for i in stem_frequency:
    print(i)

#print("the count of stems per doc is \n"+str(round(counter/len(files))))







   
   
        
        
      










#for i in range(0, 3):#files:
    #f=open(file,'r')
    #soup=BeautifulSoup(open(files[i]),'lxml')
    #f = soup.text

            
#    print(content)
 #   for count in f:
        #x=count.split(
   #     cut= striphtml(count)
  #      tokens= word_tokenize(cut)
        
    #    if '.' in tokens:
     #       tokens.remove('.')
                
      #  length=length+len(tokens)
        #print(tokens)
      #  print(tokens)
#print(length)


    
    


