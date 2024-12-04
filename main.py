from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd
import sys

# 设置控制台编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# 初始化WebDriver
driver = webdriver.Edge()

# 打开目标URL
driver.get('https://sousuo.www.gov.cn/zcwjk/policyDocumentLibrary?q=%E7%94%9F%E6%80%81&t=zhengcelibrary&orpro=')

# 设置显式等待
wait = WebDriverWait(driver, 10)

# 初始化数据列表
data_list = []

# 找到总页数
pagination_div = driver.find_element(By.CLASS_NAME, 'pagination')
pages_text = pagination_div.find_element(By.XPATH, ".//span[contains(text(), '共') and contains(text(), '页')]").text
total_pages = int(re.search(r'\d+', pages_text).group())

# 初始化当前页数
current_page = 1

while current_page <= total_pages:
    print(f'正在爬取第 {current_page} 页')

    # 等待政策项容器加载
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dys_middle_result_content_item')))

    # 找到所有政策项的容器
    items = driver.find_elements(By.CLASS_NAME, 'dys_middle_result_content_item')

    for item in items:
        try:
            # 提取标题和URL
            a_tag = item.find_element(By.TAG_NAME, 'a')
            title = a_tag.find_element(By.CLASS_NAME, 'dysMiddleResultConItemTitle').text
            url = a_tag.get_attribute('href')

            # 提取概要
            summary = item.find_element(By.CLASS_NAME, 'dysMiddleResultConItemMemo').text

            # 提取类型和发布时间
            type_time_p = item.find_element(By.CLASS_NAME, 'dysMiddleResultConItemRelevant.clearfix1')
            spans = type_time_p.find_elements(By.TAG_NAME, 'span')
            policy_type = spans[0].text if len(spans) >= 1 else ''
            publish_time = spans[1].text if len(spans) >= 2 else ''

            # 存储数据
            data_list.append({
                '标题': title,
                '类型': policy_type,
                '发布时间': publish_time,
                '概要': summary,
                'URL': url
            })
            print(f'成功爬取 {title}')
        except Exception as e:
            print(f'Error extracting item: {e}')

    # 点击下一页按钮
    if current_page < total_pages:
        try:
            next_button = driver.find_element(By.CLASS_NAME, 'btn-next')
            next_button.click()
            # 等待页面加载
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dys_middle_result_content_item')))
            current_page += 1
        except NoSuchElementException:
            break  # 没有找到下一页按钮，退出循环
    else:
        break

# 创建DataFrame并保存数据
data = pd.DataFrame(data_list, columns=['标题', '类型', '发布时间', '概要', 'URL'])
data.to_csv('D://生态政策按标题.csv', index=False, encoding='utf_8_sig')

# 关闭浏览器
driver.quit()