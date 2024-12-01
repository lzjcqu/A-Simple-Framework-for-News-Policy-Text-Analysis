#text_218
import os
import re
import jieba
from hanlp_restful import HanLPClient
HanLP = HanLPClient('https://www.hanlp.com/api', auth=None, language='zh')
#from paddlenlp import Taskflow
#import tensorflow as tf
#from minlptokenizer.tokenizer import MiNLPTokenizer


# 指定文件路径
file_path = r'D:\energypolicytext\energypolicy_218.txt'  # 修改为你的文件路径

with open('D:\中文停用词表.txt', 'r', encoding='utf-8') as f:
    stopwords = set([line.strip() for line in f.readlines()])

# 读取文件内容
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# 去掉所有空格
content_no_spaces = content.replace(' ', '')

# 定义标点符号的正则表达式，匹配非中文字符、非数字、非字母
pattern = r'[^\u4e00-\u9fff0-9a-zA-Z]'

# 去掉所有标点符号
content_clean = re.sub(pattern, '', content_no_spaces)



cut_content = HanLP(content_clean, tasks='tok/coarse').to_dict()

words_list = [word for word in cut_content['tok/coarse'][0] if word]

# 将词语写入文件，每个词语占一行
with open('words.txt', 'w', encoding='utf-8') as f:
    for word in words_list:
        f.write(word + '\n')





