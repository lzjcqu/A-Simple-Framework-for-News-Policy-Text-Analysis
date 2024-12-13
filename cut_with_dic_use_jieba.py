import os
import re
from typing import List, Set
import jieba


class TextPreprocessor:
    def __init__(self, stopwords_path: str, custom_dicts: List[str] = None):
        """
        初始化文本预处理器

        :param stopwords_path: 停用词文件路径
        :param custom_dicts: 自定义词典路径列表（可选）
        """
        # 加载自定义词典
        if custom_dicts:
            for dict_path in custom_dicts:
                jieba.load_userdict(dict_path)

        # 添加一些特定领域的专用词
        jieba.add_word('工业和信息化部')

        # 读取停用词表
        self.stopwords = self._load_stopwords(stopwords_path)

    def _load_stopwords(self, stopwords_path: str) -> Set[str]:
        """
        加载停用词文件

        :param stopwords_path: 停用词文件路径
        :return: 停用词集合
        """
        try:
            with open(stopwords_path, 'r', encoding='utf-8') as f:
                return set(line.strip() for line in f)
        except FileNotFoundError:
            print(f"警告：停用词文件 {stopwords_path} 未找到")
            return set()

    def preprocess_text(self, text: str) -> List[str]:
        """
        对文本进行预处理：去除空格、清洗文本、分词、去停用词

        :param text: 输入文本
        :return: 处理后的词语列表
        """
        # 去除空格
        content_no_spaces = text.replace(' ', '')

        # 清洗文本，只保留中文、数字和字母
        content_clean = re.sub(r'[^\u4e00-\u9fff0-9a-zA-Z]', '', content_no_spaces)

        # 分词
        tokens = jieba.lcut(content_clean)

        # 过滤停用词
        filtered_tokens = [word for word in tokens if word not in self.stopwords]

        return filtered_tokens

    def process_file(self, file_path: str) -> List[str]:
        """
        处理单个文件

        :param file_path: 文件路径
        :return: 处理后的词语列表
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return self.preprocess_text(content)
        except FileNotFoundError:
            print(f"文件未找到：{file_path}")
            return []
        except Exception as e:
            print(f"处理文件 {file_path} 时发生错误：{e}")
            return []

    def process_directory(self, directory_path: str, output_dir: str, file_extension: str = '.txt') -> dict:
        """
        遍历处理目录下的所有文件，并将结果写入输出目录

        :param directory_path: 输入目录路径
        :param output_dir: 输出目录路径
        :param file_extension: 要处理的文件扩展名，默认为 .txt
        :return: 文件名到处理结果的字典
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        results = {}
        for filename in os.listdir(directory_path):
            if filename.endswith(file_extension):
                file_path = os.path.join(directory_path, filename)
                file_tokens = self.process_file(file_path)
                results[filename] = file_tokens
                # 写入文件
                output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_processed.txt")
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(file_tokens))
        return results


def main():
    # 配置参数
    STOPWORDS_PATH = r'D:\中文停用词表.txt'
    CUSTOM_DICTS = [
        r'D:\词库最终.txt',
    ]
    INPUT_DIRECTORY = r'D:\energypolicytextfile'
    OUTPUT_DIRECTORY = r'D:\processed_texts_cut_jieba'

    # 创建预处理器实例
    preprocessor = TextPreprocessor(
        stopwords_path=STOPWORDS_PATH,
        custom_dicts=CUSTOM_DICTS
    )

    # 处理整个目录并存储结果
    results = preprocessor.process_directory(INPUT_DIRECTORY, OUTPUT_DIRECTORY)

    # 打印每个文件的处理结果
    for filename, tokens in results.items():
        print(f"文件：{filename}")
        print(f"处理后的词语数量：{len(tokens)}")
        # 可选：打印前10个词语
        print("前10个词语：", tokens[:10])
        print("-" * 50)


if __name__ == "__main__":
    main()