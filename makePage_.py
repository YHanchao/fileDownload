# 重置的生成网页的脚本

import os
import json
import time
import pandas as pd

icons = {
    'pdf':
    'https://yan-blog.oss-cn-beijing.aliyuncs.com/images/file/images/pdf.png',
    'mp4':
    'https://yan-blog.oss-cn-beijing.aliyuncs.com/images/file/images/mp4.png'
}

def changeNum(num):
    if num < 10:
        return '0{}'.format(num)
    return num

def makeHTML(info):
    string = '''
    <div class="file">
        <div class="fileType">
            <img class="img" src="{}" alt="">
        </div>
        <div class="fileInfo">
            <div class="file-name">
                <i class="fas fa-file-alt"></i>&nbsp;&nbsp;{}
            </div>
            <div class="file-desc">
                <i class="fas fa-calendar-day"></i>&nbsp;&nbsp;创建时间：{}年 {}月 {}日<br/>
            </div>
            <div class="file-href">
            <a href="{}">
                <button type="button" class="button">下载</button>
            </a>
        </div>
        </div>
        
    </div>
    '''.format(icons[info['type']], info['name'], info['year'], changeNum(info['month']), changeNum(info['day']), info['link'])
    return string

def row_to_dict(row):
    name, type = row['file_name'].split('.')
    fileCtime = time.localtime(row['time_strap'])
    year, month, day = fileCtime[0], fileCtime[1], fileCtime[2]
    res = {
        'name': name,
        'type': type,
        'time_strap': row['time_strap'],
        'link': row['link'],
        'year': year,
        'month': month,
        'day': day
    }
    return res

if __name__ == '__main__':
    df = pd.read_csv('links.csv', encoding='utf-8')
    df = df.sort_values(by='time_strap', ascending=False)

    head = ''
    tail = ''
    content = ''

    # 遍历行
    for index, row in df.iterrows():
        content += makeHTML(row_to_dict(row))

    with open('base.html', 'r', encoding='utf-8') as baseFile:
        baseHTML = baseFile.read()
        post = baseHTML.find('insert')
        head = baseHTML[:post]
        tail = baseHTML[post + len('insert'):]

    with open('index.html', 'w', encoding='utf-8') as finalFile:
        finalFile.write(head + content + tail)