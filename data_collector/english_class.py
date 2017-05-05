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
    students_list = []
    class_list = []
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
                cprint("Now processing [%s]%s in class %s" % (each_people[6], each_people[7], each_people[2]),
                       attrs=['bold'])
                if settings.DEBUG:
                    predefined.print_formatted_info((class_dict[each_people[2]]))
                # Query ec_classes table
                query = "SELECT students FROM ec_classes_" + predefined.get_semester_code_for_db(xq) + " WHERE id=%s"
                if settings.DEBUG:
                    predefined.print_formatted_info(query)
                cursor.execute(query, (class_dict[each_people[2]]['ID'],))
                class_fetch_result = cursor.fetchall()
                students_list.clear()
                students_list = json.loads(class_fetch_result[0][0])
                if each_people[6] not in students_list:
                    cprint('[Append student to class]', end='', color='blue', attrs=['bold'])
                    students_list.append(each_people[6])
                    query = "update ec_classes_" + predefined.get_semester_code_for_db(
                        xq) + " set students=%s where id=%s"
                    if settings.DEBUG:
                        predefined.print_formatted_info(query)
                    cursor.execute(query, (json.dumps(students_list), class_dict[each_people[2]]['ID']))
                    conn.commit()
                else:
                    cprint("[Student already in this class]", color='green', attrs=['bold'])
                # Query ec_students table
                query = "SELECT classes FROM ec_students_" + predefined.get_semester_code_for_db(xq) + " WHERE xh=%s"
                if settings.DEBUG:
                    predefined.print_formatted_info(query)
                cursor.execute(query, (each_people[6],))
                class_fetch_result = cursor.fetchall()
                class_list = json.loads(class_fetch_result[0][0])
                if class_dict[each_people[2]]['ID'] not in class_list:
                    class_list.append(class_dict[each_people[2]]['ID'])
                    query = "UPDATE ec_students_" + predefined.get_semester_code_for_db(
                        xq) + " SET classes=%s WHERE xh=%s"
                    cursor.execute(query, (json.dumps(class_list), each_people[6]))
                    conn.commit()
                else:
                    cprint("[Class already in this student's record]", color='green', attrs=['bold'])
            print("\n")
        this_page += 1
    cursor.close()
    conn.close()
    cprint("Finished!", color='green', attrs=['blink', 'bold'])


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
        if not isinstance(each_class[2], int):  # Exclude first invalid line
            this_clsname = "英语约课" + each_class[4]
            this_day = predefined.get_day_for_class(each_class[4][1:3])
            this_time = predefined.get_time_for_class(each_class[4][4:7])  # 这里切片实际上是有问题的，"9-10"会切成"9-1"，之前被坑过了
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
            class_dict[each_class[2]] = dict(Clsname=this_clsname, Day=this_day, Time=this_time,
                                             Teacher=this_teacher, Duration=this_duration,
                                             Week=this_week, ID=this_id)
            predefined.print_formatted_info(class_dict[each_class[2]])
            query = "select * from ec_classes_" + predefined.get_semester_code_for_db(xq) + " where id=%s"
            if settings.DEBUG:
                predefined.print_formatted_info(query)
            cursor.execute(query, (this_id,))
            class_fetch_result = cursor.fetchall()
            if not class_fetch_result:
                cprint('[Add class]', "blue", attrs=["bold"], end='')
                query = "INSERT INTO ec_classes_" + predefined.get_semester_code_for_db(
                    xq) + " (clsname, day, time, teacher, duration, week, location, students, id) "" \
                    ""VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
    process_english_students(semester)
