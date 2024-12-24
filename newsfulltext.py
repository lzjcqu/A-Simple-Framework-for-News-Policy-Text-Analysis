from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import pandas as pd
import sys
from gne import GeneralNewsExtractor
import os

sys.stdout.reconfigure(encoding='utf-8')

def clean_filename(filename):
    invalid_chars = '\\/:*?"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

# 读取CSV文件
df = pd.read_csv('D:/merged_data_for_SA_model.csv', encoding='utf-8')
urls = df['URL'].tolist()
titles = df['标题'].tolist()

# 添加新列'正文'，初始化为空字符串
df['正文'] = ''

for index, (url, title) in enumerate(zip(urls, titles)):
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        html = response.text
        extractor = GeneralNewsExtractor()
        result = extractor.extract(html, with_body_html=False)
        content = result.get('content', '')
        print(content)

        # 将提取的内容保存到DataFrame的新列中
        df.at[index, '正文'] = content

        print(f'第 {index + 1} 条新闻已提取。')
    except Exception as e:
        print(f'第 {index + 1} 条新闻提取失败，原因：{e}')
        df.at[index, '正文'] = '提取失败'

# 保存DataFrame到新的CSV文件
df.to_csv('D:/merged_data_for_SA_model_full.csv', encoding='utf-8-sig', index=False)
print('所有新闻提取完毕，并保存到CSV文件中。')

