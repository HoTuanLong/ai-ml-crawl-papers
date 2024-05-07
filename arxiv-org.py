import requests
from bs4 import BeautifulSoup
import re
import json
import os

data_all = {}

def get_data_url(url='https://arxiv.org/list/cs.LG/2209?skip=2000&show=2000'):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    soup_span = soup.find_all("span", {"class": "list-identifier"})
    soup_dd = soup.find_all("dd")
    print(len(soup_span), len(soup_dd))
    
    for id, (ss, sd) in enumerate(zip(soup_span, soup_dd)):
        span_dd = sd.find_all('div')
        ddict = {}
        for iidd, sd in enumerate(span_dd[1:]):
            attb = sd.text.strip().replace('\n', ' ').replace('  ', ' ')
            attb = attb.split(": ", 1)
            try:
                ddict[attb[0]] = attb[1]
            except Exception as e:
                print(attb)
                
        ss_txt = ss.text.replace('[', '').replace(']','').replace(',', '')
        ss_txt = ss_txt.split(' ')
        ss0 = ss_txt[0].split(':')
        ddict[ss0[0]] = f'https://arxiv.org/abs/{ss0[1]}'
        for ssi in ss_txt[1:]:
            if ssi == 'other':
                ssi = 'format'         
            ddict[ssi] = f'https://arxiv.org/{ssi}/{ss0[1]}'
        global data_all
        data_all[ss0[1]] = ddict
    print(f"Process done url: {url} len acc: {len(data_all)}")
    
cats = ['stat.TH', 'cs.LG', 'cs.AI', 'cs.CV', 'eess.AS', 'eess.IV', 'eess.SP', 'cs.DC', 'cs.CL', 'math.ST', 'math.RT', 'math.SP', 'cs.SD', 'cs.IR', 'cs.IT', 'stat.AP']
for cat_name in cats:
    for year in range(1990, 2025, 1):
        fix_pattern = f'https://arxiv.org/list/{cat_name}/{str(year)[2:]}'
        req = requests.get(fix_pattern)
        soup = BeautifulSoup(req.text, 'html.parser')
        small_text = soup.find("small").text
        try:
            number_paper = int(re.search(r'\b\d+\b', small_text).group())
        except Exception as e:
            continue
        list_urls = []
        for ii in range((number_paper+1999)//2000):
            if ii == 0:
                list_urls.append(f'{fix_pattern}?show=2000')
            else:
                list_urls.append(f'{fix_pattern}?skip={ (ii) * 2000}&show=2000')
        print(fix_pattern, number_paper)
        print(list_urls)
        for url in list_urls:
            get_data_url(url)
    fn = f'./tmp/data_arxiv_{cat_name}.json'
    os.makedirs(os.path.basename(fn), exist_ok=False)
    
    with open(fn, 'w') as fw:
        json.dump(data_all, fw, indent=2)