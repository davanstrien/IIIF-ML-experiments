#!/usr/bin/env python3 -u

import sys
import xml.etree.ElementTree as ET
from urllib.request import urlopen
import urllib.request
import urllib
import json
import os.path
import pandas as pd

def download(concept):
    term_description = concept.find("DESCRIPTOR")
    term_id = concept.find("TNR")
    if term_id is not None:
        term_id = term_id.text
    if term_description is not None:
        term_description = term_description.text

        output_filename = 'data/{}.json'.format(term_id)

        if os.path.isfile(output_filename): 
            with open(output_filename) as json_file:
                data = json.load(json_file)
        else:
            url = "http://www.loc.gov/pictures/search/?fi=subject&{}&op=PHRASE&va=exact&fo=json".format(urllib.parse.urlencode({ 'q': term_description}))
            req = urllib.request.Request(
                url, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            print (url)
            response = None
            try:
                response = urlopen(req, timeout=10)
            except urllib.error.HTTPError as error:
                print ('{}: {}'.format(error.code, error.reason))
                print ('Response: {}'.format(response))
                raise error
                
            data = json.loads(response.read())
            with open(output_filename, 'w') as outfile:
                json.dump(data, outfile)

        
        print ('{}|{}|{}'.format(term_id, term_description, data["search"]["hits"]))            
        form=False
        if concept.find('TTCForm') is not None:
            form = True

        available = 0
        internal = 0
        if 'facets' in data and len(data['facets']) == 1 and 'filters' in data['facets'][0]:
            for facet in data['facets'][0]['filters']:
                if facet['title'] == "Larger image available anywhere":
                    available = facet['count']
                elif  facet['title'] == "Larger image available only at the Library of Congress":
                    internal = facet['count']
            
        return { 'id': term_id, 'desc': term_description, 'hits': data["search"]["hits"], 'format': form, 'available': available, 'internal': internal}
    else:
        print ('Skipping {} due to no descriptor'.format(term_id)) 

def printTableHeader():
    print ('Id|Term|Public Images | Total Images')
    print('--|--|--|--|')

def printRow(row):
    print ("{}|[{}](http://www.loc.gov/pictures/search/?fi=subject&{}&op=PHRASE&va=exact)|{:,}| {:,}".format(row["id"],row["desc"],urllib.parse.urlencode({ 'q': row["desc"]}),row["available"],row["hits"]))

def images(row, df):
    filename = 'data/{}.json'.format(row['id'])

    # ["id", "desc","term", "url"]
    with open(filename) as json_file:
        data = json.load(json_file)
        for result in data['results']:
            if 'tile.loc.gov' in result['image']['full']:
                df = df.append({
                    'id': row['id'],
                    'desc':result['title'],
                    'term':row['desc'],
                    'source': result['links']['item'],
                    'url': result['image']['full']
                }, ignore_index=True)
    return df            

if __name__ == "__main__":
    tree = ET.parse('tgm1-2021-05-07.xml')
    root = tree.getroot()

    cacheFile = 'cache.pkl'
    if os.path.isfile(cacheFile): 
        df = pd.read_pickle(cacheFile)
    else:
        df = pd.DataFrame(columns=["id", "desc", "hits", 'format', "available", "internal"])
        for concept in root:
            result = download(concept)
            if result:
                df = df.append(result, ignore_index=True)
        df.to_pickle(cacheFile)
    sum_count = 20
    print ('## Formats:')
    printTableHeader()
    for row in df[df["format"]==True].sort_values(by="available", ascending=False).head(sum_count).iterrows():
        printRow(row[1])

    print ('## Subjects:')
    printTableHeader()
    for row in df[df["format"]==False].sort_values(by="available", ascending=False).head(sum_count).iterrows():
        printRow(row[1])

    print ('## Hugs:')    
    printTableHeader()
    printRow(df[df['id'] == 'tgm005206'].to_dict('records')[0])

    if len(sys.argv) > 1:
        formatSample = pd.DataFrame(columns=["id", "desc","term","source", "url"])
        for row in df[df["format"]==True].sort_values(by="available", ascending=False).head(sum_count).iterrows():
            formatSample = images(row[1], formatSample)
        print(formatSample.groupby("term").size())    
        formatSample.to_csv('image_by_formats.csv')

        subjectSample = pd.DataFrame(columns=["id", "desc","term","source", "url"])
        for row in df[df["format"]==False].sort_values(by="available", ascending=False).head(sum_count).iterrows():
            subjectSample = images(row[1], subjectSample)

        subjectSample = images(df[df['id'] == 'tgm005206'].to_dict('records')[0], subjectSample)
        print(subjectSample.groupby("term").size())    
        subjectSample.to_csv('image_by_subject.csv')
