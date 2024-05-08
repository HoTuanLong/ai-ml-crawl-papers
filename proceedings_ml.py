import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime


journal_pattern = {
    'pmlr': ['https://proceedings.mlr.press/v%s/', [1, 240], ['R0', 'R1', 'R2', 'R3', 'R4', 'R5']],
    'jmlr': ['https://www.jmlr.org/papers/v%s/', [1, 25]],
    'dmlr': ['https://data.mlr.press/volumes/%s.html', [1, 1]],
    'tmlr': ['https://jmlr.org/tmlr/papers/'],
    'mloss': ['https://www.jmlr.org/mloss/'],
}

all_papers = {}

tmlr_url='https://jmlr.org/tmlr/papers/'
data = requests.get(tmlr_url)
data.encoding = data.apparent_encoding
soup = BeautifulSoup(data.text, 'html.parser')

item_nocertificate = soup.find_all('li', {'class': 'item nocertificate'})
print(f"Number of papers in TMLR: {len(item_nocertificate)}")
tmlr_papers = []
for idp, item in enumerate(item_nocertificate):
    # print(item)
    paper = {}
    paper['title'], paper['url'] = item.find('h4').text, item.find('h4').find('a')['href']
    paper['author'], paper['time_pub'] = item.find('p').find('i').text, item.find('p').get_text(strip=True).split('[')[0].split(', ')[-1]
    hrefs = item.find('p').find_all('a')
    for href in hrefs:
        if 'bib' in href.text:            
            paper[href.text] = f"https://jmlr.org{href['href']}"
        else:
            paper[href.text] = href['href']
    # print(idp, paper)
    tmlr_papers.append(paper)
print(f"Total number in tmlr: {len(tmlr_papers)}")
all_papers['tmlr'] = tmlr_papers


dmlr_papers = []
dmlr_pattern = journal_pattern['dmlr']
for volume in range(dmlr_pattern[1][0], dmlr_pattern[1][1] + 1):
    dmlr_url = f'https://data.mlr.press/volumes/{volume:02d}.html'
    data = requests.get(dmlr_url)
    data.encoding = data.apparent_encoding
    soup = BeautifulSoup(data.text, 'html.parser')
    post_content = soup.find('div', {'class': 'post-content'})
    dl_soup = post_content.find_all('dl')
    print(f"Number of paper in volume {volume} url: {dmlr_url} : {len(dl_soup)}")

    for id_pp, pp_infor in enumerate(dl_soup):
        paper = {}
        paper['title'], paper['author'] = pp_infor.find('dt').get_text(strip=True), pp_infor.find('dd').get_text(strip=True).replace(',', ', ')
        paper['abstract'] = pp_infor.find('details').find('p').text
        hrefs = pp_infor.find_all('a')
        for href in hrefs:
            if '[' not in href.text:
                continue
            if 'bib' in href.text:            
                paper[href.text[1:-1].lower()] = f"https://data.mlr.press/{href['href']}"
            else:
                paper[href.text[1:-1].lower()] = href['href']
        dmlr_papers.append(paper)
print(f"Total number in dmlr: {len(dmlr_papers)}")
all_papers['dmlr'] = dmlr_papers


jmlr_papers = []
jmlr_pattern = journal_pattern['jmlr']
for volume in range(jmlr_pattern[1][0], jmlr_pattern[1][1] + 1):
    jmlr_url = f'https://www.jmlr.org/papers/v{volume}'
    data = requests.get(jmlr_url)
    data.encoding = data.apparent_encoding
    soup = BeautifulSoup(data.text, 'html.parser')
    print(f"Process to url volume: {jmlr_url}")
    if volume < 5:
        paper_list = soup.find_all('tr')
    else:
        paper_list = soup.find_all('dl')
        
    print(f"Number of paper in this volume {volume} : {len(paper_list)} ")
    for idp, item in enumerate(paper_list):
        # print(item)
        paper = {}
        paper['title'] = item.find('dt').text.split('\n')[0]
        dd_soup = item.find('dd')
        paper['author'], paper['time_pub'] = dd_soup.find('b').find('i').text, paper_list[0].find('dd').get_text(strip=True).split('[')[0].split('\n')[-1]
        hrefs = dd_soup.find_all('a')
        for href in hrefs:
            if 'abs' in href.text:            
                paper[href.text[1:-1].lower()] = f"{jmlr_url}/{href['href']}"
            else:
                paper[href.text[1:-1].lower()] = href['href']
        # print(idp, paper)
        jmlr_papers.append(paper)
print(f"Total number in jmlr: {len(jmlr_papers)}")
all_papers['jmlr'] = jmlr_papers


pmlr_papers = []
pmlr_pattern = journal_pattern['pmlr']
for volume in range(pmlr_pattern[1][0], pmlr_pattern[1][1] + 1):
    pmlr_url = f'https://proceedings.mlr.press/v{volume}'
    
    data = requests.get(pmlr_url)
    data.encoding = data.apparent_encoding
    soup = BeautifulSoup(data.text, 'html.parser')
    if 'File not found' in soup.text:
        print(f"*****Skip this url volume: {pmlr_url}")
        continue
    
    print(f"Process to url volume: {pmlr_url}")
        
    proceedings_name = soup.find('h2').text
    print(f"The name of volume: {proceedings_name}")
    paper_list = soup.find_all('div', {'class': 'paper'})
    print(f"Number of paper in volume {volume}: {len(paper_list)}")
    
    for idp, item in enumerate(paper_list):
        paper = {}
        
        paper['title'] = item.find('p', {'class': 'title'}).text
        paper['author'] = item.find('span', {'class': 'authors'}).text.replace('\xa0', ' ')
        paper['info'] = item.find('span', {'class': 'info'}).text
        paper['proceedings'] = proceedings_name
        hrefs = item.find('p', {'class': 'links'}).find_all('a')

        for href in hrefs:
            if 'pdf' in href.text.lower():            
                paper['pdf'] = href['href']
            else:
                paper[href.text.lower()] = href['href']
        # print(idp, paper)
        pmlr_papers.append(paper)
        
print(f"Total number in pmlr: {len(pmlr_papers)}")    
all_papers['pmlr'] = pmlr_papers


mloss_papers = []
data = requests.get('https://www.jmlr.org/mloss/')
data.encoding = data.apparent_encoding
soup = BeautifulSoup(data.text, 'html.parser')

paper_list = soup.find_all('dl')

print(f"Number of paper in mloss track : {len(paper_list)} ")
for idp, item in enumerate(paper_list):
    # print(item)
    paper = {}
    paper['title'] = item.find('dt').text.split('\n')[0]
    dd_soup = item.find('dd')
    paper['author'], paper['time_pub'] = dd_soup.find('b').find('i').text, paper_list[0].find('dd').get_text(strip=True).split('[')[0].split('; ')[-1]
    hrefs = dd_soup.find_all('a')
    for href in hrefs:
        if 'abs' in href.text or 'pdf' in href.text or 'bib' in href.text:
            paper[href.text] = f"https://www.jmlr.org{href['href']}"
        else:
            paper[href.text] = href['href']

all_papers['mloss'] = mloss_papers


time_format = f'{datetime.now().strftime("%y%m%d")}'
fn_write = f'./tmp/prml_jmlr_dmlr_tmlr_mloss_{time_format}.json'
with open(fn_write, 'w') as fw:
    json.dump(all_papers, fw, indent=2)    
print(f"Done write to file: {fn_write}")