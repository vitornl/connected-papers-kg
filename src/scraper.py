import os

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def parse_related_work(driver, url, paper_id, paper_name):
    
    driver.get(url)
    current_url = driver.current_url

    related_work_type = current_url.split('/')[-1]
    
    table = driver.find_element(by=By.XPATH, value='html/body/div/div/div[2]/div[3]/div[2]/div/div/table')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'tr')))

    for row in table.find_elements(by=By.TAG_NAME, value='tr'):
        row_content_elements = row.find_elements(by=By.CLASS_NAME, value='td-formatter')
        row_content_values = [element.text for element in row_content_elements]

        with open(f'{SCRAPED_DP}/{related_work_type}/{paper_id}.txt', 'a') as f:
            f.write('\t'.join(row_content_values) + '\n')

def parse_paper_details(driver, url):

    driver.get(url)
    current_url = driver.current_url

    table = driver.find_element(by=By.XPATH, value='html/body/div/div/div[2]/div[3]/div[2]/div/div/table')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'tr')))

    for row in table.find_elements(by=By.TAG_NAME, value='tr'):

        try:                
            row_activator = row.find_elements(by=By.TAG_NAME, value='span')[0]
            row_activator.click()
        except:
            continue
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(row_activator)).click()

        paper_abstract = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[2]/div[3]/div[3]')
        
        authors_div = paper_abstract.find_elements(by=By.CLASS_NAME, value='metadata')[0]
        plus_authors = authors_div.find_elements(by=By.CLASS_NAME, value='plus-authors')
        if len(plus_authors) > 0:
            plus_authors[0].click()

        try:
            paper_name = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[2]/div[3]/div[3]/div/div[2]/div[1]/div/a').text
            authors = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[2]/div[3]/div[3]/div/div[2]/div[2]/div/div').text
            metadata_publication = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[2]/div[3]/div[3]/div/div[2]/div[3]').text
            citations = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[2]/div[3]/div[3]/div/div[2]/div[4]/div[1]').text                
            url = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[2]/div[3]/div[3]/div/div[2]/div[5]/a[1]').get_attribute('href')
            abstract = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[2]/div[3]/div[3]/div/div[2]/div[6]').text
        except:
            continue
        else:
                                
            paper_id = url.split('/')[-3]

            with open(f'{SCRAPED_DP}/details/{paper_id}.txt', 'w') as f:
                f.write(f'{paper_name}\n{authors}\n{metadata_publication}\n{citations}\n{url}\n{abstract}')

def parse_page(url):
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get(url)
    current_url = driver.current_url

    paper_id = current_url.split('/')[-3]
    paper_name = current_url.split('/')[-2]

    if current_url.endswith('/graph'):

        with open(f'{SCRAPED_DP}/papers_id_map.txt', 'a') as f:
            f.write(f'{paper_id}\t{paper_name}\n')

        related_works_urls = [
            current_url.replace('/graph', '/prior'),
            current_url.replace('/graph', '/derivative')
        ]

        for url in related_works_urls:
            parse_related_work(driver, url, paper_id, paper_name)
            parse_paper_details(driver, url)

def main():

        urls = [
            'https://www.connectedpapers.com/main/14f0ee2594c550de7fb5e590b322bcb1bcec8061',
            # 'https://www.connectedpapers.com/main/00358a3f17821476d93461192b9229fe7d92bb3f',
            # 'https://www.connectedpapers.com/main/cb2d9b2f171da67f7b47ac3e0eb935a0de223354',
            # 'https://www.connectedpapers.com/main/d9f5ec342df97e060b527a8bc18ae4e97401f246',
            # 'https://www.connectedpapers.com/main/75c8466a0c1c3b9fe595efc83671984ef95bd679',
            # 'https://www.connectedpapers.com/main/861cf64943e90074cd25eada6e4c3912aef17eb0',
            # 'https://www.connectedpapers.com/main/a8ae2d8232db04d88cf622e5fabd11da3163aa8f',
            # 'https://www.connectedpapers.com/main/7b2ab7a828a6ae5cadffe79b1b3aa8bfbe3ae577',
            # 'https://www.connectedpapers.com/main/123139463809b5acf98b95d4c8e958be334a32b5',
            # 'https://www.connectedpapers.com/main/a7d5d88967a64a380ffc8e2d7c8b4e6e09dfe1bd',
            # 'https://www.connectedpapers.com/main/9b165b8abab60c01cd1eaabf58fd427f0e9ec97d',
            # 'https://www.connectedpapers.com/main/08ede1cbadd5c631f93c0f952ac7ca99605d8a21',
            # 'https://www.connectedpapers.com/main/9e707dd89bba25a3dd22c96f43bd72b9b3ab94bb',
            # 'https://www.connectedpapers.com/main/2a5a8db41940990dc8fe8e7717ed85ba043204e1'
        ]

        for url in urls:
            parse_page(url)

if __name__ == '__main__':


    ROOTWD = Path(os.path.dirname(os.path.realpath(__file__))).parent

    DATAPATH = f'{ROOTWD}/data'
    DRIVER = f'{DATAPATH}/geckodriver'
    SCRAPED_DP = f'{DATAPATH}/scraped/test'

    os.makedirs(SCRAPED_DP, exist_ok=True)
    os.makedirs(f'{SCRAPED_DP}/details', exist_ok=True)
    os.makedirs(f'{SCRAPED_DP}/derivative', exist_ok=True)
    os.makedirs(f'{SCRAPED_DP}/prior', exist_ok=True)
    
    main()