import csv
import os
import re

from nltk.corpus import stopwords
from collections import Counter
import jieba.analyse
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# 下载中文停用词字典
nltk.download('stopwords')


# nltk.download('stopwords-chinese')


def preprocess_text(text):
    # 移除特殊字符  
    text = re.sub(r'[^\w\s]', '', text)
    # 移除停用词
    stop_words = set(stopwords.words('chinese'))
    # 使用nltk的word_tokenize方法进行切词
    text = [word for word in jieba.cut(text) if word not in stop_words]
    return text


def tokenize_and_count(text):
    # 预处理文本  
    tokens = preprocess_text(text)
    # 使用Counter进行词频统计  
    word_count = Counter(tokens)
    return word_count


def cut_word():
    # 获取当前路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 使用函数
    files = os.listdir(current_dir + "/out")
    for pre_file in files:
        # 读取csv文件
        file_path = os.path.join("./out/", pre_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = [row for row in reader]

        # 对数据进行预处理和词频统计
        text = '\n'.join([row[0] for row in data])  # 假设数据在第一列
        word_freq = tokenize_and_count(text)
        sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

        # 写入CSV文件
        with open(f'./cut/cut_{pre_file}', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Word', 'Frequency'])  # 写入表头
            # 写入排序后的词频数据
            for word, freq in sorted_word_freq:
                writer.writerow([word, freq])


if __name__ == '__main__':
    # nltk.download('stopwords')
    cut_word()
