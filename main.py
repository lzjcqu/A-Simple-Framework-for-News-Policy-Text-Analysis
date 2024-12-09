import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd
import sys


sys.stdout.reconfigure(encoding='utf-8')

edge_options = webdriver.EdgeOptions()
edge_options.use_chromium = True
# 屏蔽inforbar
edge_options.add_experimental_option('useAutomationExtension', False)
edge_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])

edge_options.add_argument('headless')
edge_options.add_argument('disable-gpu')



# 初始化WebDriver
driver = webdriver.Edge(options= edge_options)

# 打开目标URL
#driver.get('https://qiye.qizhidao.com/company/1bb4faadd8dffa4c148fa7b7555d4b60.html')
"""
try:
    # Navigate to the target URL
    url = 'https://qiye.qizhidao.com/company/1bb4faadd8dffa4c148fa7b7555d4b60.html'
    driver.get(url)

    # Wait until the element is visible
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '//div[@class="flex" and @data-v-6ec29510]/p[@class="key" and normalize-space(text())="经营范围"]/following-sibling::p[@class="value f-1"]'))
    )

    # Get and print the text of the经营范围
    operation_scope = element.text
    print("经营范围:", operation_scope)

except Exception as e:
    print("An error occurred:", e)
finally:
    # Quit the WebDriver
    driver.quit()
"""



driver.get('https://qiye.qizhidao.com/search-company?key=%E9%9D%96%E6%B1%9F%E6%96%B0%E5%8D%8E%E4%B9%A6%E5%BA%97%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&businessSource=PC%E6%9F%A5%E4%BC%81%E4%B8%9A%E9%A6%96%E9%A1%B5&pageTitle=PC%E6%9F%A5%E4%BC%81%E4%B8%9A%E9%A6%96%E9%A1%B5&searchMode=%E5%8E%86%E5%8F%B2%E6%90%9C%E7%B4%A2&searchTab=1')
time.sleep(60)
"""
try:
    # 定位到第一个搜索结果的<a>标签
    link_element = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="靖江新华书店有限责任公司"]/parent::a')))

    # 获取href属性并打印
    link_url = link_element.get_attribute('href')
    print(link_url)

except Exception as e:
    print("未找到目标链接:", e)
"""
