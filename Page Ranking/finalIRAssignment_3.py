"""
Created on Tue Nov 13 22:53:47 2018

@author: Rutuj
"""

from bs4 import BeautifulSoup
import os
from collections import Counter
import pprint
import sys
#import time
import nltk
nltk.download("wordnet")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
from nltk.stem import WordNetLemmatizer
#from collections import Counter
from collections import OrderedDict

from nltk import PorterStemmer

import re
import math
#from collections import Counter


#path = 'C:\\Users\\Rutuj\\Desktop\\IR FILES\\Cranfield\\*' #(static to my machine)



def get_questions_queries(file):
    
    file = open(file, "r").read()	
    x = re.split("Q[0-9]+:\n",file)

    d = {key : value.replace("\n","") for key, value in enumerate(x) if value != ""}

    return d
"""
 text = re.sub(r'<.*?>', "", words)  
        txt = re.sub(r'[,-]', " ", text)  
        txt1 = re.sub(r'[^\w\s]', '', txt)  
        res = re.sub(r'[^A-Za-z]', " ", txt1)  
        res1 = res.lower()
        tokens = res1.split()
        doclen = len(tokens)
        doclst.append((index, doclen))
"""
def get_query_tokens(d, stopwords):

    
    wordNet_Lemmatizer = WordNetLemmatizer()

    for k, x in d.items():
        tokens = []

        tokens.extend([i.replace(".","").replace(":","").replace("/","").replace("'","").replace(";","").replace("(","").replace(")","").replace("*","").replace("+","")
        .replace("1","").replace("2","").replace("3","").replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("9","").replace("0","").replace("+","").replace("=","")
        .strip(" ").lower() for i in x.replace("-"," ").replace(","," ").split(" ")])

        q_tokens = []

        for x in tokens:
            if x not in stopwords and x != "":
                q_tokens.append(wordNet_Lemmatizer.lemmatize(x))

        d[k] = q_tokens

    return d


stopwords = ['a', 'all', 'an', 'and', 'any', 'are', 'as', 'be', 'been', 'but', 'by', 'few', 'for',
             'have', 'he', 'her', 'here', 'him', 'his', 'how', 'i', 'in', 'is', 'it', 'its',
             'many', 'me', 'my', 'none', 'of', 'on', 'or', 'our', 'she', 'some', 'the', 'their',
             'them', 'there', 'they', 'that', 'this', 'us', 'was', 'what', 'when', 'where',
             'which', 'who', 'why', 'will', 'with', 'you', 'your']

#stopwords= [x for x in stopwords('english')]




def get_file_data(files):

    result = []   # Result will store tokens of all the files
    doc_id = []
    header = {}
    for i in range(len(files)):
        f = open(str(sys.argv[1])+"/"+files[i], "r")
        #f = open("../Cranfield"+"/"+files[i], "r")
        #files = sorted(os.listdir("../Cranfield/"))
        #txt = re.sub(r'[,-]', " ", text)  
        #txt1 = re.sub(r'[^\w\s]', '', txt)  
        #res = re.sub(r'[^A-Za-z]', " ", txt1)  
        #res1 = res.lower()
        text = f.read()

        soup = BeautifulSoup(text,"html")
        title = soup.find_all('title')[0].string
        header.update({i+1 : title.replace("\n", " ").strip()})
        
        soup = BeautifulSoup(text,"html")
        data = soup.find_all('docno')
        doc_id.append(int(data[0].string))

        #soup = BeautifulSoup(text,"html") 
        #txt1 = re.sub(r'[^\w\s]', '', txt)  
        #res = re.sub(r'[^A-Za-z]', " ", txt1)  
        data = soup.findAll('text')   

        text = data[0].string      

        extract = []
        
        for x in text.split("\n"):
            extract.extend([i.replace(".","").replace(":","").replace("/","").replace("'","").replace(";","").replace("(","").replace(")","").replace("*","").replace("+","")
        .replace("1","").replace("2","").replace("3","").replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("9","").replace("0","").replace("+","").replace("=","")
        .strip(" ").lower() for i in x.replace("-"," ").replace(","," ").split(" ")])

        result.append([x for x in extract if x!=""])    # Append all the file tokens ignoring all the empty strings in the list

        
        
    return result, doc_id, header




def generate_dict(result, stopwords):

    posting = {}

    for x in result:
        for i in x:
            if i not in stopwords:
                if i not in posting.keys():
                    posting[i] = {"posting_list": {}, "term_freq": 0, "document_freq" : 0 }

    return OrderedDict(sorted(posting.items()))



def posting_files(result, posting, doc_id, stopwords, doc):	

    for i in range(len(result)):
        for x in result[i]:
            if x not in stopwords:
                posting[x]["posting_list"].update({ doc_id[i] : { "term_freq": result[i].count(x), "most_common_term_freq" : result[i].count(doc[i+1]["most_common"]) , "document_length" : doc[i+1]["total_terms"], "most_common" : doc[i+1]["most_common"] }})

    for x in posting.keys():
        doc_freq = len(posting[x]["posting_list"].keys())
        total_count = 0
        for i in posting[x]["posting_list"].keys():
            total_count += posting[x]["posting_list"][i]["term_freq"]
        posting[x]["term_freq"] = total_count
        posting[x]["document_freq"] = doc_freq

    return OrderedDict(sorted(posting.items()))



def document(result,stopwords):
    doc = {}
    for y in range(len(result)):
        most_common, num_most_common = Counter([a for a in result[y] if a not in stopwords]).most_common(1)[0]
        doc.update({ y+1 : {"total_terms": len(result[y]), "most_common": most_common, "num_most_common" : num_most_common, "document_length" : len(result[y]) }})

    return doc



def uncompressed_posting_file(posting, file_name):
    
    f = open(file_name, "w+")
    f.write("Term_id, Term, Term Frequency, Document Frequency, Posting List(Doc_id, term_freq, doc_len, most_common) \n")
    count = 1
    for x in posting.keys():
        s = str(count) + " "+  x + ", " + str(posting[x]["term_freq"]) + ", " + str(posting[x]["document_freq"]) + ", "
        p = ""
        count += 1
        for k in posting[x]["posting_list"]:
            p += str(k) + ": " + str(posting[x]["posting_list"][k]["term_freq"]) +", " + str(posting[x]["posting_list"][k]["document_length"]) + ", " +str(posting[x]["posting_list"][k]["most_common"])  + " --> "
        s += p[:-4]
        f.write(s + "\n")





def process(result, doc_id, stopwords, file_name, f):

    doc = document(result,stopwords)

    posting = generate_dict(result, stopwords)

    posting = posting_files(result, posting, doc_id, stopwords, doc)

    if f == "lemma":

        pass#uncompressed_posting_file(posting, file_name+".uncompress")

    return posting, doc




files = sorted(os.listdir(str(sys.argv[1])+"/"))
#files = sorted(os.listdir("../Cranfield/"))
token_result, doc_id, header = get_file_data(files)

result2 = token_result.copy()




def get_lemas(result2):
    wordnet_lemmatizer = WordNetLemmatizer()
    k = []
    for x in range(len(result2)):
        count = 0
        l = []
        for a in range(len(result2[x])):
            l.append(wordnet_lemmatizer.lemmatize(result2[x][a]))
        k.append(l)	
        count += 1

    return k




lemma_result = get_lemas(token_result)

posting_dict, doc = process(lemma_result, doc_id,stopwords, "Index_Version1", "lemma")



def get_documentfreq_query(questions_dict):
    df_query = {}
    for x in questions_dict.keys():
        d = {}
        
        data = Counter(questions_dict[x])
        for value in questions_dict[x]:
            count = 0
            for p in questions_dict.values():
                if value in p:
                    count += 1
            
            tf = data[value]
            d.update({value : {"document_freq" : count,
                               "tf" : tf,
                               "collectionsize": len(questions_dict),
                               "document_length" : len(questions_dict[x]),
                               "max_term_freq": data.most_common()[0][1]}})
        df_query[x] = d                
    return df_query







def get_weights(questions_dict, posting_dict, lemma_result, doc, df_query):

    collectionsize = 1400
    
    p = lambda x :  len(x)
    avgdoclen = sum([p(x) for x in token_result]) / collectionsize
    
    query_avgdoclen = sum([p(x) for x in questions_dict.values()]) / 20
    
    ranks = {}
    
    query_vector = {}
    
    for k in questions_dict.keys():    
        d = {"weight1": {}, "weight2": {}}
        
        query_vector.update({k : {}}) 
        temp = {"weight1" : {}, "weight2" : {}}   
        
        for x in questions_dict[k]: 
            if x in posting_dict.keys():
                
                tf = df_query[k][x]["tf"]
                df = df_query[k][x]["document_freqf"]
                #df = 1
                maxtf = df_query[k][x]["max_term_freq"]
                doclen =  df_query[k][x]["document_length"]
                cs = df_query[k][x]["collectionsize"]
                w1_q = (0.4 + 0.6 * math.log10(tf + 0.5) / math.log10(maxtf + 1.0)) * (math.log10(cs / df) / math.log10(cs))
                w2_q = (0.4 + 0.6 * (tf / (tf + 0.5 + 1.5 * (doclen / query_avgdoclen))) * math.log10(cs / df)/ math.log10(cs))
                
                temp["weight1"].update({x : w1_q/doclen })
                temp["weight2"].update({x : w2_q/doclen })
                
                """
                
                
                
                for term, tf in dictLemma.items():
                    docFreq = str(len(tf))
                    file.write(term+":\t")
                    file.write(docFreq+"\t")
                    file.write(str(tf))
                    file.write("\n")       
                    #tf_lem[index]=defaultdict(int)
                    #or w in lem:
                    #  tf_lem[i][w] += 1

               for w in set(lem):
                   if w not in ps_lem.keys():
                       ps_lem[w]={}
                       ps_lem[w][index] = []

               ps_lem[w][index]= tf_lem[index][w]
               df_lem[w]+=1
                """
                for doc_no in posting_dict[x]["posting_list"].keys():
                    if doc_no not in d["weight1"].keys():
                        d["weight1"].update({doc_no: 0})
                        d["weight2"].update({doc_no: 0})
                    tf = posting_dict[x]["term_freq"]
                    df = posting_dict[x]["document_freq"]
                    maxtf = posting_dict[x]["posting_list"][doc_no]["most_common_term_freq"]
                    doclen = doc[doc_no]["document_length"]
                    
                    w1 = (0.4 + 0.6 * math.log10(tf + 0.5) / math.log10(maxtf + 1.0)) * (math.log10(collectionsize / df) / math.log10(collectionsize)) 
                    w2 = (0.4 + 0.6 * (tf / (tf + 0.5 + 1.5 * (doclen / avgdoclen))) * math.log10(collectionsize / df)/ math.log10(collectionsize))

                    weight1 = (w1 * w1_q) / doclen
                    weight2 = (w2 * w2_q) / doclen
                    
                    d["weight1"][doc_no] += weight1
                    d["weight2"][doc_no] += weight2
                    
                    
        ranks.update({k : d})
        query_vector[k].update({"weight1": temp["weight1"], "weight2": temp["weight2"]})
        
    return ranks, query_vector  
                    



questions_list = get_questions_queries("hw3.queries")


questions_dict = get_query_tokens(questions_list ,stopwords)


documentfreq_query = get_documentfreq_query(questions_dict)


rank, query_vector = get_weights(questions_dict, posting_dict, lemma_result, doc, documentfreq_query)




for z in rank.keys():
    
 
    x = rank[z]["weight1"]
    y = sorted(x.items(), key=lambda kv: kv[1])[-5: ][:: -1]
    print("Query No: %d" %z)
    
   
    print("\nQuery Vector for weight equals 1: ")
    pprint.pprint(sorted(query_vector[z]["weight1"].items()))
    
    
    print("\nQuery Vector for weight equals 2: ")
    pprint.pprint(sorted(query_vector[z]["weight2"].items()))
    
    
    print("\nRanks ", "Document Number ", " Scores", " Haedlines")
    count = 0
    for k in y:
        count += 1
        print(count, "   ", k[0], "     ", k[1], " ", header[k[0]])
    
    print("\n")
    

    
    x = rank[z]["weight2"]
    y = sorted(x.items(), key=lambda kv: kv[1])[-5: ][:: -1]
    print("Rank ", "Doc No ", " Score", "                 Haedlines")
    count = 0
    for k in y:
        count += 1
        print(count, "   ", k[0], "     ", k[1], " ", header[k[0]])
    
    
    print("="*40)
    print("\n")

"""
print("\nDocument iD with the largest document length in collection: %s" % maxdoclendocid)

print("Size of uncompressed index1 is: ",os.path.getsize("Index_v1_uncompressed.bin"))
print("Size of uncompressed index2 is: ",os.path.getsize("Index_v2_uncompressed.bin"))
print("Size of compressed index1 is: ",os.path.getsize("Index_v1_compressed.bin"))
print("Size of compressed index2 is: ",os.path.getsize("Index_v2_compressed.bin"))

print("Time to build uncompressed index1 is: ",end1-start1)
print("Time to build uncompressed index2 is: ",end2-start2)
print("Time to build compressed index1 is: ",end3-start3)
print("Time to build compressed index2 is: ",end4-start4)



"""