import os
import time
import json
import requests
from bs4 import BeautifulSoup
import hashlib

# TODO edit this file


def process_english_class():
    class_info = []
    # todo edit here
    md5 = hashlib.md5()
    file = open('test_response.html', 'r')
    soup = BeautifulSoup(file, 'html.parser')
    for class_time in range(1, 7):
        for row_number in range(1, 8):
            query_selector = 'div[id="' + get_row_code(row_number) + '-' + str(class_time) + '-2"] a'  # 拼接soup选择条件
            for i in soup.select(query_selector):
                class_info.append(i.contents[0])
                for j in i.select('font'):
                    class_info.append(j.string)
                if len(class_info) == 4:
                    class_info.append('None')
                class_str = class_info[0] + class_info[1] + str(class_time) + str(row_number)
                md5.update(class_str.encode('utf-8'))
                class_info.append(md5.hexdigest())
                print(class_info)
                class_info.clear()


if __name__ == '__main__':
    process_english_class()
