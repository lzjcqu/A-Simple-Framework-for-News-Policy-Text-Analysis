一个简单的政策和新闻文本爬取以及分析框架

目前实现的功能有：
谷歌新闻按月度爬取，基于GNE提取正文
国务院政策文件库政策文本爬取

单个文本的分词（基于HANLP）以及去停用（基于jieba和哈工大停用词库）

main.py: 政策文本list获取
full_text: 政策文本全文获取

monthlynews.py: 按月度获取谷歌新闻

preprocessing： 预处理（分词+去停用）

news_full_text_high_performance:  并发获取新闻正文

基于外挂词库(搜狗财经词库+爬取能源常用词)的jieba分词

基于Word2Vec模型的能源政策词典扩充
