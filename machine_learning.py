import re
import os
import json
import requests
from bs4 import BeautifulSoup


conf_pattern = {
    'nips': ['https://papers.nips.cc/paper_files/paper/%s', [1987, 2023, 1]],

}

def crawl_data(conf_name):
    conf_data = conf_pattern[conf_name]
    url_pattern, years = conf_data
    all_papers = []
    for year in years:
        cvpr_url = url_pattern % year
        print(f"Crawl to url: {cvpr_url}")
        req = requests.get(cvpr_url)
        soup = BeautifulSoup(req.text, 'html.parser')
        papers = soup.find_all('dt', {'class': 'ptitle'})
        dd_soup = soup.find_all('dd')
        start_id = 0
        if len(papers) * 2 != len(dd_soup):
            start_id = 1
        for id_pp, paper in enumerate(papers):
            paper_dict = {}
            paper_dict['html'] = f"https://openaccess.thecvf.com/{paper.find('a')['href']}"
            paper_dict['title'] = f"{paper.text}"
            dd0 = dd_soup[start_id + id_pp * 2]
            dd1 = dd_soup[start_id + id_pp * 2 + 1]
            paper_dict['author'] = dd0.text.strip().replace('\n\n\n\n', ' ')

            all_a_link = dd1.find_all('a')
            for id, alink in enumerate(all_a_link):
                if id == len(all_a_link) - 1:
                    paper_dict[alink.text] = dd1.find('div').text.replace('[bibtex]\n\n', '').replace('\n\n', '')
                else:
                    try:
                        paper_dict[alink.text] = f"https://openaccess.thecvf.com/{alink['href']}" 
                    except Exception as e:
                        print(alink)
            # print(id_pp, paper_dict)
            all_papers.append(paper_dict)
    fn = f'./tmp/{conf_name}.json'
    # os.makedirs(os.path.basename(fn), exist_ok=False)
    with open(fn, 'w') as fw:
        json.dump(all_papers, fw, indent=2)

# crawl_data('wacv')
# crawl_data('iccv')

def crawl_eccv():
    url = 'https://www.ecva.net/papers.php'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    all_papers = []
    papers = soup.find_all('dt', {'class': 'ptitle'})
    dd_soup = soup.find_all('dd')
    start_id = 0
    if len(papers) * 2 != len(dd_soup):
        start_id = 1
    for id_pp, paper in enumerate(papers):
        paper_dict = {}
        paper_dict['html'] = f"https://www.ecva.net/{paper.find('a')['href']}"
        paper_dict['title'] = f"{paper.find('a').text}".replace('\n', '')
        dd0 = dd_soup[start_id + id_pp * 2]
        dd1 = dd_soup[start_id + id_pp * 2 + 1]
        paper_dict['author'] = dd0.text.strip().replace('\n\n\n\n', ' ')

        all_a_link = dd1.find_all('a')
        for id, alink in enumerate(all_a_link):
            try:
                if 'https' in alink['href']:
                    paper_dict[alink.text] = f"{alink['href']}" 
                else:
                    paper_dict[alink.text] = f"https://www.ecva.net/{alink['href']}" 
            except Exception as e:
                print(alink)
        print(id_pp, paper_dict)
        all_papers.append(paper_dict)
    conf_name = 'eccv'
    fn = f'./tmp/{conf_name}.json'
    # os.makedirs(os.path.basename(fn), exist_ok=False)
    with open(fn, 'w') as fw:
        json.dump(all_papers, fw, indent=2)