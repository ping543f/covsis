# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 23:34:29 2020

@author: mdsae
"""

import json
import os


writelog = open("file_processing_log.txt","a+", encoding = "utf-8")

def convertjson2txt(path, filename):
    file_name = filename
    file_path = path
    with open(file_path+file_name) as f:
      data = json.load(f)
    
    print("Processing File:",file_name)
    writelog.write(file_name+"\n")
    # print(data)
    # print(json.dumps(data,indent =4))
    writef = open('converted/'+file_name+".txt","a+", encoding = "utf-8")

    writef.write(data['metadata']['title']+"\n")
    
    if(file_path=="pdf_json/"):
        for i in data['abstract']:
            writef.write(i['text']+"\n")
    
        for i in data['body_text']:
            # writef.write(i['section']+"\n")
            writef.write(i['text']+"\n")
    else:
        for i in data['body_text']:
            # writef.write(i['section']+"\n")
            writef.write(i['text']+"\n")
            
    writef.close()



path = 'pdf_json/'
files = []
# r = root, d = directories, f = files
for r,d, f in os.walk(path):
    for file in f:
        if '.json' in file:
            files.append(file)

for file in files:
    convertjson2txt(path, file)


path2 = 'pmc_json/'
files2 = []
# r = root, d = directories, f = files
for r,d, f in os.walk(path2):
    for file in f:
        if '.json' in file:
            files2.append(file)

for file in files2:
    convertjson2txt(path2, file)
    


writelog.close()