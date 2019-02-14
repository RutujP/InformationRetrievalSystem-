import glob
import re
import pprint
import os
import operator
import sys
#from nltk.tokenize import word_tokenize
from collections import Counter
import collections
from datetime import datetime
#from nltk.stem import PorterStemmer
from nltk import PorterStemmer
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pickle



#tf_lem= defaultdict(int)
#df_lem = defaultdict(int)
#max_tf = []
#most_commom_termdoc=[]

count=0 #to maintain counter 
j=0 # 
token=[]# stores generating tokens
index=0 # for index calculation
ps_lem = {} # Posting files for storing lemmas
ps_stem = {} # Posting file for storing stems
lemmas={} # lemma store dictionary
stems={} # stem store dictionary
l_gap={} # for storing gaps
s_gap={} # for storing gaps
delta={} # for encoded delta 
gamma={} # for encoded gamma
docmaxtfl=[] # max doc frequency 
doclst=[] # maximum doc list

tf_lem= defaultdict(int)

# original Path in my PC 
#path = 'C:\\Users\\Rutuj\\Desktop\\IR FILES\\Cranfield\\*'
path=sys.argv[1]+'/*'
no_terms1=0

no_terms2=0



files=glob.glob(path)
start1=datetime.now()

for file in files:
    with open(file, 'r') as f:
        index=index+1
        #f=open(file, 'r')
        #for words in f:
        print("accessing for lemmas",str(index))
        words=f.read()
        text = re.sub(r'<.*?>',"", words)   # Removes SGML Tags
        txt = re.sub(r'[,-]'," ", text)     # Removes comma and hyphen, replaces with space
        txt1 = re.sub(r'[^\w\s]','',txt)    # Removes punctuation marks
        res = re.sub(r'[^A-Za-z]'," ",txt1) # Removes numbers and special characters
        res1=res.lower()                    # Lower-case the tokens
        tokens=res1.split()
        doclen = len(tokens)
        doclst.append((index,doclen))
        #tokens = word_tokenize(res1)
        token.extend(tokens)
        #if (len(tokens) > 0):
            #print(tokens)
        #folder = os.listdir(path)

        f_token = [w for w in tokens if w not in stopwords.words('english')]

        #print(f_token)
        #print(len(f_token))
        #print(index)
        #------------Lemma-------------#
        lemma = WordNetLemmatizer()
        lem=[]
        for ft in f_token:
            lem.append(lemma.lemmatize(ft))
        #print(lem)
        lemc = collections.Counter(lem)
        max_tflem = lemc.most_common(1)
        for key, value in max_tflem:
            max_tfl= value
            docmaxtfl.append((index,max_tfl))


        for t, tf in lemc.items():
            ds = [index, tf, max_tfl, doclen]
            dlist = []
            if t in ps_lem:
                ps_lem[t].append(ds)
            else:
                dlist.append(ds)
                ps_lem[t] = dlist
d= {}
d = collections.OrderedDict(sorted(ps_lem.items()))
for t in d.items():
    no_terms1+=1


with open('Index_v1_uncompressed.txt','w') as file:
    file.write("Term \t DF \t [DOCID, TF, Max_TF, DocLen] \n")
    for t, tf in d.items():
        df_lem = str(len(tf))
        file.write(t+":\t")
        file.write(df_lem+"\t")
        file.write(str(tf))
        file.write("\n")

with open('Index_v1_uncompressed.txt','r') as file:
    txt1=file.read()
bfile1=open('Index_v1_uncompressed.bin','wb')
pickle.dump(txt1,bfile1)
bfile1.close()
end1=datetime.now()

start2=datetime.now()
for file in files:
    with open(file, 'r') as f:
        index = index + 1
        #print(index)
        print("accessing stems",str(index))
        words = f.read()
        text = re.sub(r'<.*?>', "", words)  
        txt = re.sub(r'[,-]', " ", text)  
        txt1 = re.sub(r'[^\w\s]', '', txt)  
        res = re.sub(r'[^A-Za-z]', " ", txt1)  
        res1 = res.lower()
        tokens = res1.split()
        doclen = len(tokens)
        doclst.append((index, doclen))
        # tokens = word_tokenize(res1)
        token.extend(tokens)
        # if (len(tokens) > 0):
        # print(tokens)
        # folder = os.listdir(path)

        f_token = [w for w in tokens if w not in stopwords.words('english')]

        ps = PorterStemmer()
        stem = []
        for ft in f_token:
            stem.append(ps.stem(ft))

        stemc = collections.Counter(stem)
        max_tfstem = stemc.most_common(1)
        for key, value in max_tfstem:
            max_tfs = value

        for t, tf in stemc.items():
            dst = [index, tf, max_tfs, doclen]
            slist = []
            if t in ps_stem:
                ps_stem[t].append(dst)
            else:
                slist.append(dst)
                ps_stem[t] = slist


s= {}
s = collections.OrderedDict(sorted(ps_stem.items()))
for t in s.items():
    no_terms2+=1

with open('Index_v2_uncompressed.txt','w') as file:
    file.write("Term \t DF \t [DOCID, TF, Max_TF, DocLen] \n")
    for t, tf in s.items():
        df_stem = str(len(tf))
        file.write(t+":\t")
        file.write(df_stem+"\t")
        file.write(str(tf))
        file.write("\n")

#f.write(len(i-1)
#length[i+1]['docID']


with open('Index_v2_uncompressed.txt','r') as file:
    txt2=file.read()
bfile2=open('Index_v2_uncompressed.bin','wb')
pickle.dump(txt2,bfile2)
bfile2.close()
end2=datetime.now()


def unary(num):
        unarystr = ""
        i = 0
        while i < num:
            unarystr += str(1)
            i += 1
            unarystr = unarystr + str(0)
        return unarystr


def gamma(num):
        binary = str(bin(num))
        offset = binary[3:]
        offsetlen = len(offset)
        length = unary(offsetlen)
        gammastr = str(length) + str(offset)
        return gammastr

def delta(num):
        binary = str(bin(num))
        offset = binary[3:]
        offbin = binary[2:]
        gcode = gamma(len(offbin))
        deltastr = gcode + offset
        return deltastr

start3=datetime.now()
block = ''
for t,v in d.items():
    block += str(len(t))
    block+= t



termstr = ""
with open('Index_v1_compressed.txt','w') as file:
    cnt = 0
    file.write("Term String:\n" + block + "\n")
    for t, v in d.items():
        cnt += 1
        doclist = []
        gaplist = []
        for j in v:
            doclist.append(j[0])
        for j in doclist[:1]:
            gaplist.append(j)

        for blk in range((len(doclist) - 1)):
            gaplist.append(doclist[blk + 1] - doclist[blk])
        binarystr = ""

        for i in gaplist:
            gammacode = str(gamma(i))
            binarystr += gammacode
        file.write("\n" + binarystr + "\n")

        termstr += str(len(t))
        termstr += t
        if (cnt % 8 == 0):
            index = len(termstr)
            file.write("\n" + str(index) + "\n")

with open('Index_v1_compressed.txt','r') as file:
    txt3=file.read()
bfile3=open('Index_v1_compressed.bin','wb')
pickle.dump(txt3,bfile3)
bfile3.close()
end3=datetime.now()
start4=datetime.now()
front = ''
for t,v in s.items():
    front += str(len(t))
    front+= t

"""
with open('Index_Version1.txt', 'w') as file:
    for term, tf in dictLemma.items():
        docFreq = str(len(tf))
        file.write(term+":\t")
        file.write(docFreq+"\t")
        file.write(str(tf))
        file.write("\n")       
        #tf_lem[index]=defaultdict(int)
        #or w in lem:
          #  tf_lem[i][w] += 1

        #for w in set(lem):
         #   if w not in ps_lem.keys():
          #      ps_lem[w]={}
           #     ps_lem[w][index] = []

            #ps_lem[w][index]= tf_lem[index][w]
            #df_lem[w]+=1
"""



termstr = ""
with open('Index_v2_compressed.txt','w') as file:
    cnt = 0
    file.write("Term String:\n" + front + "\n")

    for t, v in s.items():
        cnt += 1
        doclist = []
        gaplist = []
        for j in v:
            doclist.append(j[0])
        for j in doclist[:1]:
            gaplist.append(j)

        for blk in range((len(doclist) - 1)):
            gaplist.append(doclist[blk + 1] - doclist[blk])

        binarystr = ""

        for i in gaplist:
            deltacode = str(delta(i))
            binarystr += deltacode
        file.write("\n" + binarystr + "\n")

        termstr += str(len(t))
        termstr += t
        if (cnt % 8 == 0):
            index = len(termstr)
            file.write("\n" + str(index) + "\n")

with open('Index_v2_compressed.txt','r') as file:
    txt4=file.read()
bfile4=open('Index_v2_compressed.bin','wb')
pickle.dump(txt4,bfile4)
bfile4.close()
end4=datetime.now()

os.remove("Index_v1_uncompressed.txt")
os.remove("Index_v2_uncompressed.txt")
os.remove("Index_v1_compressed.txt")
os.remove("Index_v2_compressed.txt")

terms = ["reynolds", "nasa", "prandtl", "flow", "pressure", "boundary", "shock"]
for t, v in d.items():
    if t in terms:
        size = sys.getsizeof(v)
        df = str(len(v))
        print("\n")
        print("Term: ", t)
        print("DF:", df)
        tf = 0
        for i in v:
            tf += i[1]
        print("TF: ", tf)
        print("Inverted List size: ", size)

for t, v in d.items():
    if t == 'nasa':
        print("\nTerm:", t)
        df = str(len(v))
        print("DF of ", t, "is: ", df)
        countP = 0
        for i in v[:3]:
            countP += 1
            termFre = i[1]
            dlen = i[3]
            max_tf = i[2]
            print("\nNasa Posting List no.:", countP)
            print("TF: ", termFre)
            print("DocLength: ", dlen)
            print("Max TF: ", max_tf)

index1_dict = {}
for t, tf in d.items():
    df = len(tf)
    index1_dict[t] = df

max_val_index1 = max(index1_dict.values())
min_val_index1 = min(index1_dict.values())
maxtermindex2 = []
mintermindex2 = []
for k, v in index1_dict.items():
    if index1_dict[k] == max_val_index1:
        maxtermindex2.append(k)
    elif index1_dict[k] == min_val_index1:
        mintermindex2.append(k)
print("\nTerms from Index 1 with Largest df:")
print(maxtermindex2)
print("\nTerms from Index 1 with Smallest df:")
print(mintermindex2)

index2_dict = {}
for t, tf in s.items():
    df = len(tf)
    index2_dict[t] = df

maxvalindex2 = max(index2_dict.values())
minvalindex2 = min(index2_dict.values())
maxtermindex2 = []
mintermindex2 = []
for k, v in index2_dict.items():
    if index2_dict[k] == maxvalindex2:
        maxtermindex2.append(k)
    elif index2_dict[k] == minvalindex2:
        mintermindex2.append(k)
print("\nStems from index 2 with Largest df:")
print(maxtermindex2)
print("\nStems from index 2 with Smallest df:")
print(mintermindex2)

docmaxtfldict = dict(docmaxtfl)
max_tfdocid = max(docmaxtfldict.items(), key=operator.itemgetter(1))[0]
print("\nDocid with the largest maximum term frequency in collection: %s" % max_tfdocid)

maxdoclendict = dict(doclst)
maxdoclendocid = max(maxdoclendict.items(), key=operator.itemgetter(1))[0]
print("\nDocument iD with the largest document length in collection: %s" % maxdoclendocid)

print("Size of uncompressed index1 is: ",os.path.getsize("Index_v1_uncompressed.bin"))
print("Size of uncompressed index2 is: ",os.path.getsize("Index_v2_uncompressed.bin"))
print("Size of compressed index1 is: ",os.path.getsize("Index_v1_compressed.bin"))
print("Size of compressed index2 is: ",os.path.getsize("Index_v2_compressed.bin"))

print("Time to build uncompressed index1 is: ",end1-start1)
print("Time to build uncompressed index2 is: ",end2-start2)
print("Time to build compressed index1 is: ",end3-start3)
print("Time to build compressed index2 is: ",end4-start4)


"""dictLemma = collections.OrderedDict(sorted(dictionary1.items()))
nof1 = 0
for term in dictLemma.items():
    nof1+=1
"""

"""
with open('Index_Version1.txt', 'w') as file:
    for term, tf in dictLemma.items():
        docFreq = str(len(tf))
        file.write(term+":\t")
        file.write(docFreq+"\t")
        file.write(str(tf))
        file.write("\n")       
        #tf_lem[index]=defaultdict(int)
        #or w in lem:
          #  tf_lem[i][w] += 1

        #for w in set(lem):
         #   if w not in ps_lem.keys():
          #      ps_lem[w]={}
           #     ps_lem[w][index] = []

            #ps_lem[w][index]= tf_lem[index][w]
            #df_lem[w]+=1
"""
        #max_tf[f.name] = collections.Counter(lem).most_common(1)

#ds = [df_lem, ps_lem]
#d={}

#new_file = open("C:\\Users\\Rutuj\\.spyder-py3\\uncompressedlemmas.txt","wb")
path="C:\\Users\\Rutuj\\.spyder-py3\\uncompressedlemmas.txt"
new_file=open(path,'wb')


#for t in tf_lem[index]:
 #   d[t]=tuple(d[t] for d in ds)
    #new_file.write((''.join(chr(i) for i in d)).encode('charmap'))
 
