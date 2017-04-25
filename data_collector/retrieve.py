# This module retrieves class tables from server and save them to raw_data directory
# Created Mar. 15, 2017 by Frederic
import requests
import json
import settings

header_info = {
    "User-Agent": settings.USER_AGENT,
    "Referer": "http://csujwc.its.csu.edu.cn/jiaowu/pkgl/llsykb/llsykb_find_xs0101.jsp?xnxq01id=2016-2017-2&init=1&isview=0",
    'Host': 'csujwc.its.csu.edu.cn',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://csujwc.its.csu.edu.cn',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Content-Length': '103',
    'Cookie': settings.COOKIE_JW,
}


def retrieve_classtable():
    file = open("stu_data.json")
    stu_data = json.load(file)
    url = 'http://csujwc.its.csu.edu.cn/jiaowu/pkgl/llsykb/llsykb_kb.jsp'
    data = {
        'type': 'xs0101',
        'isview': '0',
        'xnxq01id': settings.GLOBAL_semester,
        'xs0101id': 'xs0101id',
        'xs': u'xs',
        'sfFD': '1'
    }
    s = requests.session()
    for i in stu_data:
        data['xs0101id'] = i['xs0101id']
        data['xs'] = i['xm']
        print('Trying to fetch data for %s...' % data['xs0101id'])
        req1 = s.post(url, headers=header_info, data=data)
        local_filename = 'raw_new/' + data['xs0101id'] + '.html'
        with open(local_filename, 'wb') as f:
            f.write(req1.content)
        print(req1)


if __name__ == '__main__':
    retrieve_classtable()