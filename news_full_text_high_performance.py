import asyncio
import aiohttp
import logging
import os
import pandas as pd
from gne import GeneralNewsExtractor
from asyncio import Semaphore
from tenacity import retry, stop_after_attempt, wait_exponential

# 配置日志
logging.basicConfig(filename='script.log', level=logging.INFO)

# 初始化提取器
extractor = GeneralNewsExtractor()
save_dir = 'D:/google_news_data_full_text'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 信号量，限制并发请求数量
sem = Semaphore(10)

# 读取CSV文件
df = pd.read_csv('D:/google_news_data/叶片 风/2023/Apr_news.csv', encoding='utf-8')
urls = df['URL'].tolist()
titles = df['标题'].tolist()


# 清洁文件名
def clean_filename(filename):
    invalid_chars = r'\\/:*?"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def process_url(session, index, url, title):
    async with sem:
        try:
            html = await fetch(session, url)
            result = extractor.extract(html, with_body_html=False)
            content = result.get('content', '')

            if pd.isna(title) or title.strip() == '':
                filename = f'{index + 1}_无标题.txt'
            else:
                clean_title = clean_filename(title)
                filename = f'{index + 1}_{clean_title}.txt'
                if len(filename) > 255:
                    filename = filename[:255]

            counter = 0
            while True:
                if counter == 0:
                    full_path = os.path.join(save_dir, filename)
                else:
                    name, ext = os.path.splitext(filename)
                    full_path = os.path.join(save_dir, f'{name}_{counter}{ext}')
                if not os.path.exists(full_path):
                    break
                counter += 1

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logging.info(f'第 {index + 1} 条新闻已保存。')
        except aiohttp.ClientError as e:
            logging.error(f'请求失败: {e}')
        except IOError as e:
            logging.error(f'文件操作失败: {e}')
        except Exception as e:
            logging.error(f'其他错误: {e}')


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [process_url(session, index, url, title) for index, (url, title) in enumerate(zip(urls, titles))]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
