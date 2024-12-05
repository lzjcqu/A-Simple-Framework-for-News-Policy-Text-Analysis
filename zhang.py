import random
import time
import pandas as pd
import sys
import os
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


keywords3 = [
    #'风力发电',
    #'风电',
    '风能',
    '风机',
    '塔筒 风',
    '齿轮箱 风',
    '风塔',
    '叶片 风'
]
years = range(2018, 2024)

# 生成每个月份的数据
months = [
    {'name': 'Jan', 'month_num': '1', 'start_day': '1', 'end_day': '31'},
    {'name': 'Feb', 'month_num': '2', 'start_day': '1', 'end_day': '28'},
    {'name': 'Mar', 'month_num': '3', 'start_day': '1', 'end_day': '31'},
    {'name': 'Apr', 'month_num': '4', 'start_day': '1', 'end_day': '30'},
    {'name': 'May', 'month_num': '5', 'start_day': '1', 'end_day': '31'},
    {'name': 'Jun', 'month_num': '6', 'start_day': '1', 'end_day': '30'},
    {'name': 'Jul', 'month_num': '7', 'start_day': '1', 'end_day': '31'},
    {'name': 'Aug', 'month_num': '8', 'start_day': '1', 'end_day': '31'},
    {'name': 'Sep', 'month_num': '9', 'start_day': '1', 'end_day': '30'},
    {'name': 'Oct', 'month_num': '10', 'start_day': '1', 'end_day': '31'},
    {'name': 'Nov', 'month_num': '11', 'start_day': '1', 'end_day': '30'},
    {'name': 'Dec', 'month_num': '12', 'start_day': '1', 'end_day': '31'}
]

# 设置输出文件夹
output_folder = 'D:/google_news_data'

# 设置控制台编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

DO = 0

for keyword in keywords3:
    time.sleep(60)
    # 创建关键字文件夹
    keyword_folder = os.path.join(output_folder, keyword)
    if not os.path.exists(keyword_folder):
        os.makedirs(keyword_folder)

    # 遍历每个年份
    for year in years:
        time.sleep(60)
        year_folder = os.path.join(keyword_folder, str(year))
        if not os.path.exists(year_folder):
            os.makedirs(year_folder)

        # 遍历每个月份
        for month in months:

            time.sleep(30)
            driver = webdriver.Edge()
            # 设置查询字符串
            query = keyword
            encoded_query = urllib.parse.quote(query)
            # 构建URL
            url = f'https://www.google.com/search?q={encoded_query}&tbs=cdr:1,cd_min:{month["month_num"]}/{month["start_day"]}/{year},cd_max:{month["month_num"]}/{month["end_day"]}/{year}&tbm=nws'
            driver.get(url)
            # 设置显式等待
            wait = WebDriverWait(driver, 10)

            # 初始化数据列表
            datalist = []
            news = 0
            page = 0
            max_news = 4950
            while True:
                page = page + 1
                print(f'关键字: {keyword}, 年份: {year}, 月份: {month["name"]}, 页码: {page}')
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
            # 保存数据到CSV
            file_name = os.path.join(year_folder, f'{month["name"]}_news.csv')
            data = pd.DataFrame(datalist, columns=['标题', '来源', '发布时间', '概要', 'URL'])
            data.to_csv(file_name, index=False, encoding='utf_8_sig')
            print(f'{month["name"]}数据已保存到 {file_name}')
            # 关闭浏览器
            driver.quit()


print("K3Done!")