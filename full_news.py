import logging
import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from gne import GeneralNewsExtractor
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# 配置日志
logging.basicConfig(
    filename='script.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class NewsExtractor:
    def __init__(self, save_dir='D:/google_news_data_full_text'):
        self.save_dir = save_dir
        self.extractor = GeneralNewsExtractor()
        self.setup_directory()
        self.setup_browser()

    def setup_directory(self):
        """设置保存目录"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            logging.info(f"创建目录: {self.save_dir}")

    def setup_browser(self):
        """配置和初始化Edge浏览器"""
        try:
            edge_options = Options()
            edge_options.add_argument('--headless')  # 无头模式
            edge_options.add_argument('--disable-gpu')
            edge_options.add_argument('--no-sandbox')
            edge_options.add_argument('--disable-dev-shm-usage')
            edge_options.add_argument('--window-size=1920,1080')
            edge_options.add_argument(
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

            service = Service(EdgeChromiumDriverManager().install())
            self.driver = webdriver.Edge(service=service, options=edge_options)
            self.driver.set_page_load_timeout(30)
            logging.info("浏览器初始化成功")
        except Exception as e:
            logging.error(f"浏览器初始化失败: {e}")
            raise

    def clean_filename(self, filename):
        """清理文件名中的非法字符"""
        invalid_chars = r'\\/:*?"<>|'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

    def get_page_content(self, url, retries=3, delay=5):
        """获取页面内容，包含重试机制"""
        for attempt in range(retries):
            try:
                self.driver.get(url)
                # 等待页面加载完成
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                # 增加随机延迟，避免被反爬
                time.sleep(delay)
                return self.driver.page_source
            except TimeoutException:
                logging.warning(f"第 {attempt + 1} 次尝试超时: {url}")
                if attempt == retries - 1:
                    raise
            except WebDriverException as e:
                logging.warning(f"第 {attempt + 1} 次尝试失败: {url}, 错误: {e}")
                if attempt == retries - 1:
                    raise
                time.sleep(delay * (attempt + 1))  # 递增延迟

    def save_content(self, content, index, title):
        """保存提取的内容到文件"""
        try:
            if pd.isna(title) or title.strip() == '':
                filename = f'{index + 1}_无标题.txt'
            else:
                clean_title = self.clean_filename(title)
                filename = f'{index + 1}_{clean_title}.txt'
                if len(filename) > 255:
                    filename = filename[:255]

            counter = 0
            while True:
                if counter == 0:
                    full_path = os.path.join(self.save_dir, filename)
                else:
                    name, ext = os.path.splitext(filename)
                    full_path = os.path.join(self.save_dir, f'{name}_{counter}{ext}')
                if not os.path.exists(full_path):
                    break
                counter += 1

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logging.info(f'成功保存第 {index + 1} 条新闻: {filename}')
            return True
        except Exception as e:
            logging.error(f'保存文件失败 {filename}: {e}')
            return False

    def process_urls(self, csv_path):
        """处理CSV文件中的所有URL"""
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
            urls = df['URL'].tolist()
            titles = df['标题'].tolist()

            success_count = 0
            fail_count = 0

            for index, (url, title) in enumerate(zip(urls, titles)):
                try:
                    logging.info(f'正在处理第 {index + 1}/{len(urls)} 条新闻: {url}')

                    html = self.get_page_content(url)
                    result = self.extractor.extract(html, with_body_html=False)
                    content = result.get('content', '')

                    if not content.strip():
                        logging.warning(f'第 {index + 1} 条新闻内容为空: {url}')
                        fail_count += 1
                        continue

                    if self.save_content(content, index, title):
                        success_count += 1
                    else:
                        fail_count += 1

                except Exception as e:
                    logging.error(f'处理第 {index + 1} 条新闻失败: {url}, 错误: {e}')
                    fail_count += 1
                    continue

            logging.info(f'处理完成: 成功 {success_count} 条, 失败 {fail_count} 条')

        except Exception as e:
            logging.error(f'处理CSV文件失败: {e}')
        finally:
            self.cleanup()

    def cleanup(self):
        """清理资源"""
        try:
            self.driver.quit()
            logging.info("浏览器资源已释放")
        except Exception as e:
            logging.error(f"释放浏览器资源失败: {e}")


def main():
    csv_path = 'D:/google_news_data/叶片 风/2023/Apr_news.csv'
    extractor = NewsExtractor()
    extractor.process_urls(csv_path)


if __name__ == '__main__':
    main()