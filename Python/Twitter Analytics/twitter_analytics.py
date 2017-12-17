# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 12:33:58 2017

@author: spran
"""
import requests
import json
import operator
import csv

#declaration of variables, dictionary and lists
tweet_cnt=0 
lang_dict = {}
lang_list=[] 
tweet_list=[]

#accessing the json file 
json_file = requests.get("http://kevincrook.com/utd/tweets.json")

#downloading the json file in the local directory
data = json_file.json()
with open('data.json', 'w') as f:
    json.dump(data, f)
    
#calculating the tweet languages and their frequencies            
def calculate_tweet_lang_freq():
    #opening the file in utf-8 format
    with open('data.json', 'r',encoding='utf-8') as f:
        data = json.load(f)
        for d in data:
            for key, val in d.items():
                #checking if the object in json file is lang
                if 'lang' in key: 
                    #checking if the lang is already added to the dictionary
                    if val in lang_dict.keys():
                        for k, v in lang_dict.items():
                            if val==k:
                                #increasing the count of frequency
                                lang_dict[k] +=1 
                    #if language does not exist in the dictionary
                    else:
                        #adding the language into the dictionary
                        temp1 = val
                        #setting the frequency of each language to 1 initially
                        lang_dict[temp1]=1
    return lang_dict
    
    
#opening the file in utf-8 format       
with open('data.json', 'r',encoding='utf-8') as f:
    data = json.load(f)
    #get the number of events
    events = len(data)
    #counting the number of tweets in each of the event
    for d in data:
        for key, val in d.items():
            #checking if the object is text object
            if 'text'==key: 
                #incrementing the tweet count for each text object found
                tweet_cnt += 1

#getting the dictionary of tweet languages and their frequencies
lang_freq = calculate_tweet_lang_freq()  
 
#sorting the dictionary based on frequency count              
sorted_x = sorted(lang_freq.items(), key=operator.itemgetter(1), reverse=True)

for x in sorted_x:
    lang_list.append(list(x))

#editing the lang abbr length to 2 letters
for li in lang_list:
    li[0]=li[0][:2]


# For storing the tweets texts                                        
with open('data.json', 'r',encoding='utf-8') as f:
    data = json.load(f)
    for d in data:
        for key, val in d.items():
            if 'text'== key: 
                #storing the tweet text
                tweet_list.append(val)
                
#creating the twitter_analytics.txt output file
with open("twitter_analytics.txt", "w+",encoding='utf-8') as f:
    #event count
    f.write(str(events)+"\n")
    #tweet count
    f.write(str(tweet_cnt)+"\n")
    #lang with highest freq first
    writer = csv.writer(f)
    writer.writerows(lang_list) 

#creating the tweets.txt output file
with open("tweets.txt", "w+",encoding='utf-8') as f:
    for line in tweet_list[:-1]:
        f.write(line + "\n")  
    for line in tweet_list[-1:]:
        f.write(line)
