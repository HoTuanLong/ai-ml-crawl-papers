import re
import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Natural Language Processing and Computational Linguistics: ['ACL', 'ACL Findings', 'EMNLP', 'EMNLP Findings', 'NAACL HLT', 'NAACL-HLT Findings', 'COLING']
# Computer Vision and Pattern Recognition: ['CVPR', 'ICCV', 'ECCV', 'WACV']
# Machine Learning and Learning Theory: ['ICML', 'ICLR', 'NeurIPS', 'COLT', 'UAI', 'AISTATS']
# Artificial Intelligence: ['AAAI', 'IJCAI']
# Data Mining and Information Retrieval: ['KDD', 'SIGIR', 'TheWebConf', 'WSDM', 'CIKM', 'ICDM', 'RecSys']
# Speech and Signal Processing: ['INTERSPEECH', 'ICASSP', '']
# Security and Privacy: ['PETS', 'S&P', 'USENIX', 'SaTML', 'NDSS', 'ACM CCS'] # https://people.engr.tamu.edu/guofei/sec_conf_stat.htm
# https://github.com/ZhengyuZhao/AI-Security-and-Privacy-Events

def get_data_iclr():
    data_iclr = {}
    for year in range(2018, 2025, 1):
        iclr_url = f'https://iclr.cc/virtual/{year}/papers.html?filter=titles'
        data = requests.get(iclr_url)
        data.encoding = data.apparent_encoding
        soup = BeautifulSoup(data.text, 'html.parser')
        papers = soup.find_all('li')
        cnt = 0
        data_year = []
        for id, item in enumerate(papers):
            
            alink = item.find('a')
            if f'/virtual/{year}/poster' in alink['href']:
                cnt += 1
                # print(cnt, alink['href'], alink.text, '/virtual/2022' in alink)
                data_year.append({'url': f'https://iclr.cc{alink["href"]}', 'title': alink.text})
        print(year, cnt)

        if cnt > 0:
            data_iclr[f'{year}'] = data_year

    time_format = f'{datetime.now().strftime("%y%m%d")}'
    with open(f'./tmp/iclr_{time_format}.json', 'w') as fw:
        json.dump(data_iclr, fw, indent=2)

