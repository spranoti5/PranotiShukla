# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 15:36:39 2017
@author: spran
"""

import requests
import csv
from collections import Counter
from operator import itemgetter
import itertools
import copy

#declaring the lists and a dictionary
tuple_list=[]
main_list=[]
freq_list=[]
final_list=[]
dict_freq = {}

#assigning the URLs
url_train="http://kevincrook.com/utd/market_basket_training.txt"
url_test="http://kevincrook.com/utd/market_basket_test.txt"

r = requests.get(url_train)
s = requests.get(url_test)

#assigning the file names
train_filename = "market_basket_training.txt"
test_filename = "market_basket_test.txt"

#getting the files in local directory
trf = open(train_filename,"wb")
trf.write(r.content)
trf.close()
tef = open(test_filename,"wb")
tef.write(s.content)
tef.close()

#create dictionary for training data
def create_traindata_dictionary():
    with open(train_filename, "rt", encoding="utf8") as f:
        for line in csv.reader(f):
            tuple_list.append(line[1::])
        count = Counter(tuple(x) for x in iter(tuple_list))
        for key,val in count.items():
            dict_freq[key] = val

#create product recommendations
def create_recommendation():
    #using the test file in read mode
    with open(test_filename, "rt", encoding="utf8") as f:
        for line in csv.reader(f):
            main_list=[]
            #accessing the dictionary
            for key, value in dict_freq.items():
                #checking if the length of tuple and list is equal
                if len(key)==len(line):
                    if all(x in key for x in line[1::]):
                        #getting the set difference
                        reco_prod = set(key) - set(line[1::])
                        freq_list=[line[0],reco_prod.pop(),value]
                        main_list.append(freq_list)
                        final_copy=copy.deepcopy(main_list)
            #if the product in not found in the training dat set
            if not main_list:
                chunks = list(itertools.combinations(line[1::], len(line)-2))
                chunk_list= [list(elem) for elem in chunks]
                temp_list=[]
                for line1 in chunk_list:
                    main_list=[]
                    #accessing the dictionary
                    for key, value in dict_freq.items():
                        #checking if the length of tuple and list is equal
                        if len(key)==len(line1)+1:
                            if all(x in key for x in line1):
                                #getting the set difference
                                reco_prod = set(key) - set(line1)
                                freq_list=[line[0],reco_prod.pop(),value]
                                main_list.append(freq_list)
                                temp_list.append(freq_list)
                                final_copy=copy.deepcopy(main_list)
                    #if the product in not found in the training dat set
                    if not temp_list:
                        chunks_n = list(itertools.combinations(line1, len(line1)-1))
                        chunk_list_n= [list(ele) for ele in chunks_n]
                        for line2 in chunk_list_n:
                            for key, value in dict_freq.items():
                                #checking if the length of tuple and list is equal
                                if len(key)==len(line2)+1:
                                    if all(x in key for x in line2):
                                        #getting the set difference
                                        reco_prod = set(key) - set(line2)
                                        freq_list=[line[0],reco_prod.pop(),value]
                                        main_list.append(freq_list)
                                        final_copy=copy.deepcopy(main_list)
            #sorting the list based on the frequencies
            main_list = sorted(final_copy, key=itemgetter(2), reverse=True)
            final_list.append(main_list[0])
        
#calling the functions
create_traindata_dictionary()
create_recommendation()

#delete the unwanted column
for li in final_list:
    del li[-1]
#write data to new file created                
with open("market_basket_recommendations.txt", "w+") as f:
    writer = csv.writer(f)
    writer.writerows(final_list)
