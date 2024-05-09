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

conf_list = {
    'neurips': ['https://neurips.cc/virtual/%s/papers.html?filter=titles', 2006, 2025],
    'icml':  ['https://icml.cc/virtual/%s/papers.html?filter=titles', 2017, 2025],
    'iclr':  ['https://iclr.cc/virtual/%s/papers.html?filter=titles', 2018, 2025],
}

data_all = {}

def get_data_conf(conf_name):
    print(f"Process conf: {conf_name}")
    data_conf = {}
    conf_pattern = conf_list[conf_name]
    for year in range(conf_pattern[1], conf_pattern[2], 1):
        conf_url = conf_pattern[0] % year
        data = requests.get(conf_url)
        data.encoding = data.apparent_encoding
        soup = BeautifulSoup(data.text, 'html.parser')
        papers = soup.find_all('li')
        cnt = 0
        data_year = []
        for id, item in enumerate(papers):
            
            alink = item.find('a')
            if f'/virtual/{year}/poster' in alink['href']:
                cnt += 1
                data_year.append({'url': f'https://iclr.cc{alink["href"]}', 'title': alink.text})
        print(year, cnt)

        if cnt > 0:
            data_conf[f'{year}'] = data_year
    data_all[conf_name] = data_conf
for k in conf_list.keys():
    get_data_conf(k)


time_format = f'{datetime.now().strftime("%y%m%d")}'
with open(f'./tmp/neurips_icml_iclr_{time_format}.json', 'w') as fw:
    json.dump(data_all, fw, indent=2)

