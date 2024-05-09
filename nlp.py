import re
import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# https://2023.aclweb.org/downloads/acl2023-handbook-v3.pdf
['ACL', 'ACL Findings', 'EMNLP', 'EMNLP Findings', 'NAACL HLT', 'NAACL-HLT Findings', 'COLING']

data_all = {}

nlp_url = "https://aclanthology.org/events/"
data = requests.get(nlp_url)
data.encoding = data.apparent_encoding
soup = BeautifulSoup(data.text, 'html.parser')
events = soup.find_all('li')
cnt = 0
data_event = []
for ide, event in enumerate(events):
    alink = event.find('a')
    if f'/events/' in alink['href']:
        data_event.append({'url': f'https://aclanthology.org{alink["href"]}', 'info': alink.text})
print(f'Number of events: {len(data_event)}')


for ide, event in enumerate(data_event):
    data = requests.get(event['url'])
    data.encoding = data.apparent_encoding
    soup = BeautifulSoup(data.text, 'html.parser')
    papers = soup.find_all('p', {'class': 'd-sm-flex align-items-stretch'})
    print(f"Number of paper in event: {event['info']}: {len(papers)}")
    data_list = []
    for id, item in enumerate(papers):  
        strong = item.find('strong')
        alink = strong.find('a', {'class': 'align-middle'})
        paper = {'url': f'https://aclanthology.org{alink["href"]}', 'title': alink.text, 'info': event['info']}
        data_list.append(paper)
    data_all[event['info']] = data_list
    print(f"Done process to event {ide + 1}/ {len(data_event)} len: {len(data_list)}")


data_all['events'] = data_event

time_format = f'{datetime.now().strftime("%y%m%d")}'
with open(f'./tmp/all_nlp_{time_format}.json', 'w') as fw:
    json.dump(data_all, fw, indent=2)




