一个简单的政策和新闻文本爬取以及分析框架

目前实现的功能有：
谷歌新闻按月度爬取，基于GNE提取正文
国务院政策文件库政策文本爬取

单个文本的分词（基于HANLP）以及去停用（基于jieba和哈工大停用词库）
多文本预处理(两种方法：一种基于HanLP，不外挂词典；一种基于jieba，外挂词典)
基于Word2Vec模型的能源政策词典扩充（基于维基百科中文数据和爬取到的政策语料，训练了一个Word2Vec模型）

main.py: 政策文本list获取
full_text: 政策文本全文获取

monthlynews.py: 按月度获取谷歌新闻

preprocessing： 预处理（分词+去停用）

news_full_text_high_performance:  并发获取新闻正文

cut_jieba.py :基于外挂词库(搜狗财经词库+爬取能源常用词)的jieba分词 

word2wec_train(test).py: Word2Vec模型的训练与测试，如果要在本地运行，首先要使用此项目：https://github.com/lzhenboy/word2vec-Chinese
完成中文维基百科的预处理（不包括分词），然后使用perprocessing对维基百科语料分词。之后将两种语料合并后训练即可。

NEXT：基于pre-trained-model的embeddings
      语句级情感分析
      篇章级情感分析（embeddings+FNN（RF，SVM））


Reference：
https://github.com/lzhenboy/word2vec-Chinese


