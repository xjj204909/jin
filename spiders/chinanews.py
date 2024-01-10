import csv
import json
import random
import re
import threading
import time
from configparser import ConfigParser
import requests
from bs4 import BeautifulSoup

# 读取页数
def read_page(item):
    # 修改配置选项的值
    lock = threading.Lock()
    with lock:
        config = ConfigParser()
        config.read('config/conf.ini')
        return int(config.get('spider', item))

# 写入配置
def write_page(item):
    # 修改配置选项的值
    lock = threading.Lock()
    with lock:
        config = ConfigParser()
        config.read('config/conf.ini')
        page = int(config.get('spider', item))
        config.set('spider', item, str(page + 1))
        # 写入配置文件
        with open('config/conf.ini', 'w') as configfile:
            config.write(configfile)
        return page + 1


class ChinanewsSpider:

    # 国际 https://channel.chinanews.com.cn/cns/cjs2/gj.shtml?pager=0
    # 体育 https://channel.chinanews.com.cn/cns/cjs2/ty.shtml?pager=0
    # 文娱 https://channel.chinanews.com.cn/cns/cjs2/cul.shtml?pager=0
    # 社会 https://channel.chinanews.com.cn/cns/cjs/sh.shtml?pager=0
    # 反腐 https://channel.chinanews.com.cn/cns/cl/fz-ffcl.shtml?pager=0
    # 军事 https://channel.chinanews.com.cn/cns/cl/gn-js.shtml?pager=0
    # 金融 https://channel.chinanews.com.cn/cns/cl/cj-fortune.shtml?pager=0
    # 科技 https://channel.chinanews.com.cn/cns/cl/cj-it.shtml?pager=0
    # 地产 https://channel.chinanews.com.cn/cns/cl/cj-house.shtml?pager=0
    # 汽车 https://channel.chinanews.com.cn/cns/cl/cj-auto.shtml?pager=0
    def start_requests(self):
        urls = ['https://channel.chinanews.com.cn/cns/cjs2/gj.shtml',
                'https://channel.chinanews.com.cn/cns/cjs2/ty.shtml',
                'https://channel.chinanews.com.cn/cns/cjs2/cul.shtml',
                'https://channel.chinanews.com.cn/cns/cjs/sh.shtml',
                'https://channel.chinanews.com.cn/cns/cl/fz-ffcl.shtml',
                'https://channel.chinanews.com.cn/cns/cl/gn-js.shtml',
                'https://channel.chinanews.com.cn/cns/cl/cj-fortune.shtml',
                'https://channel.chinanews.com.cn/cns/cl/cj-it.shtml',
                'https://channel.chinanews.com.cn/cns/cl/cj-house.shtml',
                'https://channel.chinanews.com.cn/cns/cl/cj-auto.shtml']
        names = ['国际', '体育', '文娱', '社会', '反腐', '军事', '金融', '科技', '地产', '汽车']
        # 获取任务需要抓取的页数
        page_no = read_page("page_no")
        # 获取任务需要开始抓取的链接
        item_no = read_page("item_no")
        for url in urls[item_no:]:
            self.name = names[item_no]
            for i in range(page_no, 20):
                # 拼接链接
                sp_url = f"{url}?pagenum=500&pager={i}"
                print(f"sp_url:  {sp_url}")
                time.sleep(random.randint(1, 3))
                # 请求
                response = requests.get(url=sp_url)
                try:
                    # 解析响应
                    text = response.text
                    docs = []
                    if item_no < 4:
                        # 正则匹配获取json串
                        match = re.search(r"(?<={).*(?=})", text)
                        if match:
                            # 提取匹配的内容
                            text = match.group(0)
                            text = '{' + text + '}'
                            json_data = json.loads(text)
                            docs = json_data['docs']
                    else:
                        # 另外一种页面格式 解析
                        soup = BeautifulSoup(text, 'html.parser')
                        script_tags = soup.find_all('script')

                        for script_tag in script_tags:
                            script_content = script_tag.string
                            if script_content:
                                # 正则匹配获取json串
                                match = re.search(r"(?<=\[).*(?=\])", script_content)
                                if match:
                                    # 提取匹配的内容
                                    text = match.group(0)
                                    text = '[' + text + ']'
                                    json_data = json.loads(text)
                                    docs = json_data
                                    break
                    for doc in docs:
                        title = doc['title'].strip()
                        content = doc['content'].strip()
                        href = doc['url'].strip()
                        with open(f'out/{self.name}_2.csv', mode='a', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            writer.writerow([title, content, href])
                except Exception as e:
                    print("error:" + response.text)
                    raise
                #write_page("page_no")
                print(f"item:{item_no}---page_no:{i}")
            item_no = write_page("item_no")


if __name__ == '__main__':
    chinanews = ChinanewsSpider()
    # 请求抓取任务
    chinanews.start_requests()
