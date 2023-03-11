# -*- coding: utf-8 -*-
"""Web Crawler.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1syuJbuIfGI_El_ifPZZrsibF7DVhw2gA
"""

import requests
from bs4 import BeautifulSoup
import os
import re
import nltk
import string
from urllib import request
from urllib.parse import urlparse
import json
from collections import Counter
import pickle
import sqlite3

nltk.download('punkt')
nltk.download('stopwords')

def get_urls(starter):
    dictUrl = {}
    r = requests.get(starter)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    urls = [starter]
    #dictUrl[]
    
    total = 0
    index = 0
    while total < 50:
        for link in soup.find_all(href=re.compile("^https://")):
            link_string = str(link.get('href'))
            link_data = requests.get(link_string).text
            link_soup = BeautifulSoup(link_data, 'html.parser')
            for script in link_soup(['script', 'style']):
                script.extract()
            link_text = link_soup.getText()

            if link_string not in urls and 'google' not in link_string and ('tea' in link_text or 'Tea' in link_text or 'theanine' in link_text):
                urls.append(link_string)

                file = open(str(total) + '.txt', 'w', encoding="utf-8")
                file.write(link_text)
                file.close()
                
                dictUrl[link_string] = str(total) + '.txt' 

                total += 1
            if total >= 50:
                break

        index += 1
        if len(urls) > index and total < 50:
            r = requests.get(urls[index])
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')
        else:
            break

    print(urls)
    return dictUrl #urls = list(dictUrl.keys())

#Given a list of URLs, scrapes all text off each page.
def scrape_text(urls):
    text_list = []
    for i, url in enumerate(urls):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        text = soup.get_text()
        text_list.append(text)
        
        # create directory for files if it does not exist
        directory = 'data'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # create file with scraped text
        with open(os.path.join(directory, f"{i}.txt"), 'w', encoding='utf-8') as f:
            f.write(text)

    return text_list

#Given a list of URLs, cleans up the text from each file by removing newlines and tabs, 
#and extracts sentences with NLTK's sentence tokenizer. Writes the sentences for each file to a new file.
def clean_text(dictUrl):
    dictCleanText = {}
    #for url in urls:
    for k, v in dictUrl.items():
        url = k        
        #filename = os.path.basename(url) + '.txt'
        filename = v
        sentenceFile = os.path.basename(url) + '_sentences.txt'
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                text = f.read()
                text = text.replace('\n', ' ').replace('\t', ' ')
                sentences = nltk.sent_tokenize(text)
                with open(sentenceFile , 'w') as f2:
                    f2.write('\n'.join(sentences))
                dictCleanText[k] = sentenceFile # entry only when no exception
            except Exception as e:
                # fornmatted as xml, etc 
                pass
    return dictCleanText

#Given a list of URLs, extracts 25  terms from the pages using an term frequency.
#lowercase everything, remove stopwords and punctuation. Prints the top 25-40 terms.
def get_top_terms(dictCleanText):
    all_terms = []
    regex = re.compile('[^a-zA-Z-]')
    #for url in urls:
    for k, v in dictCleanText.items():
        url = k
        file = v
        #print(file)
        #print(url) # https://matcha.com/en-ca/blogs/news/the-green-teas-highest-in-l-theanine-the-mood-boosting-amino-acid-that-fights-brain-fog-cognitive-decline-with-age
        
        #print(url.split('//')[-1])
        #with open(url.split('//')[-1] + '_sentences.txt', 'r') as f:
        with open(file, 'r') as f:
            text = f.read()
            text = text.lower()
            text = regex.sub(' ', text) # replace all non-alpha and non-dash characters with a space
            text = re.sub(r'\b\w{1}\b', '', text)
            terms = [word for word in nltk.word_tokenize(text) if word not in string.punctuation and word not in nltk.corpus.stopwords.words('english')]
            all_terms.extend(terms)
    
    term_counts = Counter(all_terms)
    top_terms = term_counts.most_common(40)
    for term, count in top_terms:
        print(f"{term}: {count}")

    return top_terms

#given a list of urls, a searchable knowledge base related to the 10 manual terms using a dictionary is built and pickled
def create_knowledge_base(dictCleanText):
    top_terms = ['tea', 'theanine', 'matcha', 'green tea', 'black tea', 'oolong tea', 'herbal tea', 'caffiene', 'health', 'flavors']
    conn = sqlite3.connect('knowledge_base.db')
    c = conn.cursor()
    
    # Create table for each term
    for term in top_terms:
        c.execute(f"CREATE TABLE IF NOT EXISTS {term} (fact TEXT)")
        
        # Insert facts into table
        #for url in urls:
        for k, v in dictCleanText.items():
            url = k
            file = v
            #ith open(url.split('//')[-1] + '_sentences.txt', 'r') as f:
            with open(file, 'r') as f:
                text = f.read()
                if term in text.lower():
                    c.execute(f"INSERT INTO {term} (fact) VALUES (?)", (text,))
    
    conn.commit()
    conn.close()
    
    # Pickle database schema
    with open('knowledge_base_schema.pickle', 'wb') as f:
        pickle.dump(top_terms, f)

#Given a term, queries the knowledge base SQLite database and returns a list of related facts.
def query_knowledge_base(term):    
    conn = sqlite3.connect('knowledge_base.db')
    c = conn.cursor()
    
    # Query database for facts related to the term
    c.execute(f"SELECT fact FROM {term}")
    results = c.fetchall()
    facts = [result[0] for result in results]
    
    conn.close()
    
    return facts

# Press the green button in the gutter to run the script.
def main():
    starter_url = 'https://matcha.com/blogs/news/the-green-teas-highest-in-l-theanine-the-mood-boosting-amino-acid-that-fights-brain-fog-cognitive-decline-with-age'
    #creates many local text files off of url
    dictUrl = get_urls(starter_url) 
    dictUrl.keys()
    #scrape and clean text
    text_list = scrape_text(dictUrl.keys())
    dictCleanText = clean_text(dictUrl)
    #get top terms, and save it into a dictionary
    top_terms = get_top_terms(dictCleanText)

    #create_knowledge_base(dictCleanText)

if __name__ == '__main__':
    main()