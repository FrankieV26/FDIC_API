#!/usr/bin/env python

import requests
import json
import pandas as pd
import numpy as np

def get_fdic():
    url = 'https://banks.data.fdic.gov/api/institutions'
    headers = {
        'fields': 'CERT,NAME,ADDRESS,CITY,STALP,ZIP,RSSDHCR,FED_RSSD,NAMEHCR',
        'limit':10000,
        'offset':0,
    }
    
    json_object_data = []
    total_rows = 1 #dummy figure until overwritten
    while total_rows > headers['offset']:
        response = requests.get(url,params=headers)
        json_object = json.loads(response.text)
        json_object_data += json_object['data']

        total_rows = int(json_object['meta']['total'])
        headers['offset'] += headers['limit']
    return json_object_data

def main():
    json_object_data = get_fdic()
    data = []
    for listing in json_object_data:
        data.append(listing['data'])
    df = pd.DataFrame(data)
    df['Mapping_Name'] = df.apply(lambda x:x['NAME'] if x['NAMEHCR'] is np.nan else x['NAMEHCR'],axis=1)
    #TODO export data to excel or database or return df

if __name__=="__main__":
    main()