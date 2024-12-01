from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
#from webdriver_manager.microsoft import EdgeChromiumDriverManager
#from selenium.webdriver.common.proxy import Proxy, ProxyType
import random
import time
import pandas as pd
import sys
import os
import urllib.parse

months = [
    #{'name': 'March', 'start_date': '3/1/2022', 'end_date': '3/31/2022'},
    {'name': 'April', 'start_date': '4/1/2022', 'end_date': '4/30/2022'},
    {'name': 'May', 'start_date': '5/1/2022', 'end_date': '5/31/2022'},
    #{'name': 'June', 'start_date': '6/1/2023', 'end_date': '6/30/2023'},
    #{'name': 'July', 'start_date': '7/1/2023', 'end_date': '7/31/2023'},
    #{'name': 'August', 'start_date': '8/1/2023', 'end_date': '8/31/2023'},
    #{'name': 'September', 'start_date': '9/1/2023', 'end_date': '9/30/2023'},
    #{'name': 'October', 'start_date': '10/1/2023', 'end_date': '10/31/2023'},
    #{'name': 'November', 'start_date': '11/1/2023', 'end_date': '11/30/2023'},
    #{'name': 'December', 'start_date': '12/1/2023', 'end_date': '12/31/2023'}
]

output_folder = 'D:/2022_March_to_December_light_volts_google_news_list'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# 设置控制台编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')




DO = 0

for month in months:
    if DO:
        time.sleep(30)
    driver = webdriver.Edge()
    query = '光伏产业'
    encoded_query = urllib.parse.quote(query)
    url = f'https://www.google.com/search?q={encoded_query}&tbs=cdr:1,cd_min:{month["start_date"]},cd_max:{month["end_date"]}&tbm=nws'

    driver.get(url)

    # 设置显式等待
    wait = WebDriverWait(driver, 10)

    # 初始化DataFrame
    datalist = []
    news = 0
    page = 0
    max_news = 4950
    while True:
        page = page + 1
        print(page)
        try:
            # 等待政策项容器加载
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'SoaBEf')))

            # 找到所有政策项的容器
            items = driver.find_elements(By.CLASS_NAME, 'SoaBEf')

            for item in items:
                try:
                    news = news + 1
                    # URL, title
                    a_tag = item.find_element(By.TAG_NAME, 'a')
                    url = a_tag.get_attribute('href')
                    print(url)

                    # Use CSS selector for multiple classes and search within 'item'
                    data_class_pre = item.find_element(By.CSS_SELECTOR, '.lSfe4c.r5bEn.aI5QMe')
                    data_class = data_class_pre.find_element(By.CLASS_NAME, 'SoAPf')

                    # Extract summary
                    summary_class = data_class.find_element(By.CLASS_NAME, 'GI74Re.nDgy9d')
                    summary = summary_class.text
                    print(summary)

                    # Extract source and title
                    source_and_title_class = data_class.find_element(By.CLASS_NAME, 'MgUUmf.NUnG9d')
                    source = source_and_title_class.find_element(By.TAG_NAME, 'span').text
                    print(source)
                    title = data_class.find_element(By.CLASS_NAME, 'n0jPhd.ynAwRc.MBeuO.nDgy9d').text
                    print(title)

                    time_class = data_class.find_element(By.CLASS_NAME, 'OSrXXb.rbYSKb.LfVVr')
                    pub_time = time_class.find_element(By.TAG_NAME, 'span').text
                    print(pub_time)

                    # 存储数据
                    datalist.append({
                        '标题': title,
                        '来源': source,
                        '发布时间': pub_time,
                        '概要': summary,
                        'URL': url
                    })
                    print(f'成功爬取第 {news} 条新闻: {title}')
                except Exception as e:
                    print(f'Error extracting item: {e}')

            #     # 找到并点击翻页链接
            #     try:
            #         next_button = driver.find_element(By.ID, "pnnext")
            #         next_button.click()
            #         # 等待下一页加载
            #         time.sleep(3)
            #         wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'SoaBEf')))
            #     except news == 4950:
            #         print("没有更多页面了")
            #         break
            # except Exception as e:
            #     print(f'Error during pagination: {e}')
            #     break
            # 如果已经达到预定新闻数量，跳出循环
            if news >= max_news:
                break

                # 找到并点击翻页链接
            try:
                next_button = driver.find_element(By.ID, "pnnext")
                next_button.click()
                # 等待下一页加载
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'SoaBEf')))
            except NoSuchElementException:
                print("没有更多页面了")
                break
        except (TimeoutException, NoSuchElementException) as e:
            print(f'翻页时出错: {e}')
            break

        # Save data to CSV
        file_name = f'{output_folder}/{month["name"]}_news.csv'
        data = pd.DataFrame(datalist, columns=['标题', '来源', '发布时间', '概要', 'URL'])
        data.to_csv(file_name, index=False, encoding='utf_8_sig')
        print(f'{month["name"]}数据已保存到 {file_name}')

    # 关闭浏览器
    driver.quit()


print("Done!")

