import requests
from bs4 import BeautifulSoup
import json
import os

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
    
all_pages = crawl_arxiv_sanity_lite()