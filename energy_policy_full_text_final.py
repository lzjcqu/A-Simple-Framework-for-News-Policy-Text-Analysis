import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import os
from gne import GeneralNewsExtractor
from PyPDF2 import PdfReader
import win32com.client


def change_word_to_txt(word_path, save_path):
    word = win32com.client.Dispatch('Word.Application')
    doc = word.Documents.Open(word_path)
    doc.SaveAs(save_path, 2)
    doc.Close()
    word.Quit()


save_dir = 'D:/energypolicytext'

# 读取CSV文件
df = pd.read_csv('D://能源政策.csv', encoding='utf-8')
urls = df['URL'].tolist()
titles = df['标题'].tolist()

for index, (url, title) in enumerate(zip(urls, titles)):
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        html = response.text
        extractor = GeneralNewsExtractor()
        result = extractor.extract(html, with_body_html=False)
        content = result.get('content', '')

        if '附件' in content:
            print("有附件")
            driver = webdriver.Edge()
            driver.get(url)
            attachments_pdf = driver.find_elements(By.XPATH, "//div[@id='UCAP-CONTENT']//a[contains(@href, '.pdf')]")
            attachments_doc = driver.find_elements(By.XPATH, "//div[@id='UCAP-CONTENT']//a[contains(@href, '.doc')]")
            attachments_docx = driver.find_elements(By.XPATH, "//div[@id='UCAP-CONTENT']//a[contains(@href, '.docx')]")
            # Combine all attachments into a single list
            attachments = attachments_pdf + attachments_doc + attachments_docx
            # Initialize a counter for附件序号
            attachment_counter = 1
            for attachment in attachments:
                link = attachment.get_attribute('href')
                print(f"附件链接：{link}")
                # Determine the file extension
                extension = os.path.splitext(link)[1]
                if not extension:
                    # If extension not found, assume based on the list it came from
                    if attachment in attachments_pdf:
                        extension = '.pdf'
                    elif attachment in attachments_doc:
                        extension = '.doc'
                    elif attachment in attachments_docx:
                        extension = '.docx'
                    else:
                        extension = '.unknown'
                # Construct the filename
                filename = f"energypolicy_{index + 1}_附件{attachment_counter}{extension}"
                filepath = os.path.join(save_dir, filename)
                try:
                    response = requests.get(link, stream=True)
                    response.raise_for_status()
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"下载完成: {filepath}")
                except requests.exceptions.HTTPError as errh:
                    print(f"HTTP Error: {errh}")
                except requests.exceptions.ConnectionError as errc:
                    print(f"Error Connecting: {errc}")
                except requests.exceptions.Timeout as errt:
                    print(f"Timeout Error: {errt}")
                except requests.exceptions.RequestException as err:
                    print(f"Error: {err}")
                attachment_counter += 1
            driver.quit()




        filename_txt = f'energypolicy_{index + 1}.txt'

        full_path = os.path.join(save_dir, filename_txt)

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'第 {index + 1} 条政策已保存。')
    except Exception as e:
        print(f'第 {index + 1} 条政策提取失败，原因：{e}')
