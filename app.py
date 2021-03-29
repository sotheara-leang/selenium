import os
import time
from selenium import webdriver
from tqdm import tqdm

def google_translate(driver, sents):
    text_area = driver.find_element_by_css_selector('div.QFw9Te textarea')

    src_sents = '\n'.join(sents)
    text_area.clear()
    text_area.send_keys(src_sents)
    time.sleep(3)

    tar_sents = driver.find_element_by_css_selector('div.J0lOec').text.split('\n')
    return tar_sents


if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    
    driver = webdriver.Chrome('./chromedriver', options=option)
    driver.get('https://translate.google.com/?sl=km&tl=en&op=translate')

    data_dir = 'work/data'
    output_dir = 'work/result'

    for text_file in os.scandir(data_dir):
        if text_file.is_dir() or text_file.name.startswith('.') or text_file.name.startswith('_'):
            continue

        file_name = os.path.basename(text_file.path)

        with open(text_file.path, 'r', encoding='utf-8') as reader, open('%s/%s' % (output_dir, file_name), 'w', encoding='utf-8') as writer:
            sents = []
            for line in tqdm(reader):
                line = line.strip()
                sents.append(line)
                
                if len(sents) == 10 or line == '':
                    print('--> source sentences')
                    print(sents)
                    
                    tar_sents = google_translate(driver, sents)

                    print('--> target sentences')
                    print(tar_sents)
                    
                    for sent in tar_sents[:-1]:
                        sent = sent.strip()
                        writer.write('%s\n' % sent)

                    writer.flush()
                    
                    sents = []
