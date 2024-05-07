import requests
from bs4 import BeautifulSoup
import json
import os
import pandas as pd


ROOT_URL = "https://arxiv-sanity-lite.com/?page_number=%d"


def crawl_arxiv_sanity_lite():
    all_pages = [ ]
    for i in range(1, 2001):
        url = ROOT_URL % i
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        # Your string
        print("Page:", i, url,  len(soup.text))
        string_data = soup.find_all('script')[1].text.split('\n')[1][13:-1]

        # Convert the string to list of dictionaries
        data_list = json.loads(string_data)

        # Print the list of dictionaries
        all_pages.append(data_list)
        # if i % 50 == 0:
        #     with open(f'./tmp/arxiv05_page_{i}.json', 'w') as fw:
        #         json.dump(all_pages, fw)
    fn = './tmp/arxiv05_page_2000_final.json',
    os.makedirs(os.path.basename(fn), exist_ok=False)
    with open(fn, 'w') as fw:
        json.dump(all_pages, fw)
        
    return all_pages

def convert_data_to_pd(all_pages):
    
    # data = json.load(open('./tmp/arxiv05_page_2000_final.json', 'r'))

    data_csv = {
        'authors' : [],
        'id': [],
        'summary': [],
        'tags': [],
        'thumb_url': [],
        'time': [],
        'title': [],
        'utags': [],
        'weight': [],
        
    }
    for papers in all_pages:
        for pp in papers:
            for k, v in pp.items():
                data_csv[k].append(v)

    df_data = pd.DataFrame(data_csv)
    df_data.to_csv('./arxiv05.csv')

    return df_data

all_pages = crawl_arxiv_sanity_lite()

df_data = convert_data_to_pd(all_pages)


