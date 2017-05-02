# Find relationships between student number prefix and the faculty he/she is in from English class system and save
# them to table ec_stu_id_prefix
import requests
import json
import mysql.connector
import settings
import predefined
import re
from termcolor import cprint

re_quote_compiled = re.compile("'")

class_dict = {}
header_info = {
    "User-Agent": settings.USER_AGENT,
    "Referer": "http://122.207.65.163/agent161/",
    'Host': '122.207.65.163',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'Cookie': settings.COOKIE_ENG,
}


def stu_id_prefix():
    url = settings.ENGLISH_CLASS_NAMEROLL_URL
    s = requests.session()
    conn = mysql.connector.connect(**settings.MYSQL_CONFIG)
    cursor = conn.cursor()
    print("Fetching students information...")
    data = dict(pageNo=1)
    req = s.get(url, headers=header_info, params=data)  # You must use GET method instead of POST here
    json_string = req.content.decode(encoding='utf-8')
    json_string = re_quote_compiled.sub('"', json_string)
    json_content = json.loads(json_string)
    if settings.DEBUG:
        print("json_string:\n" + json_string)
    pages_count = json_content[0][0]
    records_count = json_content[0][1]
    this_page = json_content[0][2]
    if settings.DEBUG:
        predefined.print_formatted_info(class_dict, True, 'Class_dict')
    cprint("Fetched %s records in %s pages" % (records_count, pages_count), color='magenta')
    while this_page <= pages_count:
        cprint("Now processing page %s:" % this_page, color='cyan')
        data = dict(pageNo=this_page)
        req = s.get(url, headers=header_info, params=data)
        json_string = req.content.decode(encoding='utf-8')
        json_string = re_quote_compiled.sub('"', json_string)
        json_content = json.loads(json_string)
        for each_people in json_content:
            if not isinstance(each_people[2], int):
                print(each_people)
                re_profess_compiled = re.compile(r'[0-9]{4,4}')
                print("Now processing [%s]%s" % (each_people[6][0:4], re_profess_compiled.split(each_people[4])[0]))
                # Query in ec_stu_id_prefix table
                query = "SELECT name FROM ec_stu_id_prefix WHERE prefixes=%s"
                cursor.execute(query, (each_people[6][0:4],))
                fetch_result = cursor.fetchall()
                if not fetch_result:
                    cprint('[Add]', end='', color='blue', attrs=['bold'])
                    query = "INSERT INTO ec_stu_id_prefix (prefixes, name) values (%s, %s)"
                    cursor.execute(query, (each_people[6][0:4], re_profess_compiled.split(each_people[4])[0]))
                    conn.commit()
                else:
                    # For unknown reason, there are different majors having same prefixes, therefore you need to handle
                    # this situation.
                    cprint("[Prefix already in table]", color='green', attrs=['bold'], end='')
                    print(fetch_result[0][0])
                    if re_profess_compiled.split(each_people[4])[0] not in fetch_result[0][0]:
                        query = "UPDATE ec_stu_id_prefix SET name=%s WHERE prefixes=%s"
                        cursor.execute(query, (
                            fetch_result[0][0] + ';' + re_profess_compiled.split(each_people[4])[0],
                            each_people[6][0:4]))
                        conn.commit()

            print("\n")
        this_page += 1
    cursor.close()
    conn.close()
    cprint("Finished!", color='green', attrs=['blink', 'bold'])


if __name__ == '__main__':
    stu_id_prefix()
