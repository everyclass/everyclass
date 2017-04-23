# This module retrieves separate English class tables from server and process information
# Created Apr. 20, 2017 by Frederic
import requests
import json
import mysql.connector
import settings
import predefined
import hashlib
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


def process_english_students(xq):
    url = settings.ENGLISH_CLASS_NAMEROLL_URL
    s = requests.session()
    print("Fetching students information...")
    data = {
        'pageNo': 1,
    }
    req = s.get(url, headers=header_info, params=data)  # You must use GET method instead of POST here
    json_string = req.content.decode(encoding='utf-8')
    json_string = re_quote_compiled.sub('"', json_string)
    if settings.DEBUG:
        print(json_string)
    json_content = json.loads(json_string)
    num_page = json_content[0][0]
    num_total = json_content[0][1]
    page = json_content[0][2]

    # todo write code here. Process each students


def retrieve_english_classes(xq):
    url = settings.ENGLISH_CLASS_URL
    s = requests.session()
    conn = mysql.connector.connect(**settings.MYSQL_CONFIG)
    cursor = conn.cursor()
    print('Fetching class information...')
    req = s.post(url, headers=header_info)
    json_string = req.content.decode('utf-8')
    json_string = re_quote_compiled.sub('"', json_string)
    if settings.DEBUG:
        predefined.print_formatted_info("json_string:" + json_string, True)
        print("-----\n\n")
    json_content = json.loads(json_string)
    for each_class in json_content:
        if each_class[2] != 1:  # Exclude first invalid line
            this_clsname = "英语约课" + each_class[4]
            this_day = predefined.get_day_for_class(each_class[4][1:3])
            this_time = predefined.get_time_for_class(each_class[4][4:7])
            this_teacher = each_class[3]
            if each_class[2][0] == '双':
                this_duration = "4-16"
                this_week = "双周"
            else:
                this_duration = "3-15"
                this_week = "单周"
            this_location = each_class[5]
            md5 = hashlib.md5()
            class_str = str(each_class[2]) + str(each_class[3]) + str(each_class[4]) + str(each_class[5])
            md5.update(class_str.encode('utf-8'))
            this_id = md5.hexdigest()
            del md5
            predefined.print_formatted_info(dict(Clsname=this_clsname, Day=this_day, Time=this_time,
                                                 Teacher=this_teacher, Duration=this_duration,
                                                 Week=this_week, ID=this_id))
            query = "select * from ec_classes_" + predefined.get_semester_code_for_db(xq) + " where id=%s"
            if settings.DEBUG:
                predefined.print_formatted_info(query)
            cursor.execute(query, (this_id,))
            class_fetch_result = cursor.fetchall()
            if not class_fetch_result:
                cprint('[Add class]', "blue", attrs=["bold"], end='')
                query = "insert into ec_classes_" + predefined.get_semester_code_for_db(
                    xq) + " (clsname, day, time, teacher, duration, week, location, students, id) "" \
                    ""values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                predefined.print_formatted_info("SQL: " + query)
                cursor.execute(query, (
                    this_clsname, this_day, this_time, this_teacher, this_duration,
                    this_week, this_location, json.dumps(list()), this_id))
                conn.commit()
            else:
                cprint("[Class already exists]", "green", attrs=["bold"])
            print("--\n")
    cursor.close()
    conn.close()


if __name__ == '__main__':
    semester = input('Input a semester(2016-2017-2 by default):')
    if not semester:
        semester = settings.GLOBAL_semester
    retrieve_english_classes(semester)
    # process_english_students(semester)
