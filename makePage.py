import os
import json
import time

baseDir = 'files'
icons = {
    'pdf':
    'https://yan-blog.oss-cn-beijing.aliyuncs.com/images/file/images/pdf.png'
}

links = dict()
fileList = list()

with open('links.txt', 'r', encoding='utf-8') as linkFile:
    files = linkFile.read().split('\n')
    for f in files:
        ff = f.split(' ')
        links[ff[0]] = ff[1]

def changeNum(num):
    if num < 10:
        return '0{}'.format(num)
    return num

for file in os.listdir(baseDir):
    thisFile = baseDir + '\\' + file
    fileName = os.path.splitext(file)[0]
    fileType = os.path.splitext(thisFile)[-1]
    file_timeStrap = int(os.path.getctime(thisFile))
    fileCtime = time.localtime(file_timeStrap)
    year, month, day = fileCtime[0], fileCtime[1], fileCtime[2]

    fileList.append({
        'name': fileName,
        'type': fileType[1: ],
        'link': links[fileName + fileType],
        'time_strap': file_timeStrap,
        'year': year,
        'month': month,
        'day': day
    })

fileList.sort(key=lambda x: x['time_strap'], reverse=True)

json_data = json.dumps(fileList)
with open('data.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

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

with open('base.html', 'r', encoding='utf-8') as baseFile:
    baseHTML = baseFile.read()
    post = baseHTML.find('insert')
    content = baseHTML[:post]

    for info in fileList:
        content += makeHTML(info)

    content += baseHTML[post + len('insert'):]

    with open('index.html', 'w', encoding='utf-8') as finalFile:
        finalFile.write(content)
