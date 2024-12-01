from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import pandas as pd
import sys

# 设置控制台编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# 初始化WebDriver
driver = webdriver.Edge()

# 打开目标URL

driver.get(
#   'https://www.google.com/search?q=%E5%85%89%E4%BC%8F%E4%BA%A7%E4%B8%9A&sca_esv=5140e803a5dc7c59&biw=1592&bih=930&sxsrf=ADLYWIIwsODlL3zWkQdQTdqmLgVfYsKjkg%3A1732950725424&source=lnt&tbs=cdr%3A1%2Ccd_min%3A2%2F1%2F2023%2Ccd_max%3A2%2F21%2F2023&tbm=nws'
    'https://www.google.com/search?q=%E5%85%89%E4%BC%8F%E4%BA%A7%E4%B8%9A&sca_esv=5140e803a5dc7c59&biw=1592&bih=930&sxsrf=ADLYWIIqQx9CRwPYM3VCZNP4zXZXAxkDEg%3A1732950944212&source=lnt&tbs=cdr%3A1%2Ccd_min%3A2%2F1%2F2023%2Ccd_max%3A2%2F28%2F2023&tbm=nws'
)
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


# 保存数据
data = pd.DataFrame(datalist, columns=['标题','来源','发布时间','概要','URL'])
data.to_csv('D://2023年2月光伏产业新闻.csv', index=False, encoding='utf_8_sig')

# 关闭浏览器
driver.quit()