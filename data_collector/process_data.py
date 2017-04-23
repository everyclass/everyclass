# This module processes data from raw_data directory and save them to database
# Created Mar. 26, 2017 by Frederic
import os
from bs4 import BeautifulSoup
import hashlib
import json
import mysql.connector
import settings
from predefined import get_row_code
from predefined import get_semester_code_for_db


def process_data(xq):
    class_info = {}
    class_list = []
    students_set = set([])
    names_json = open("stu_data.json")
    names = json.load(names_json)
    conn = mysql.connector.connect(**settings.MYSQL_CONFIG)
    cursor = conn.cursor()
    for stu in names:
        print('Processing student: [%s]%s(id=%s)' % (stu['xh'], stu['xm'], stu['xs0101id']))
        file_addr = os.path.join('raw_data', stu['xs0101id'])
        file = open(file_addr + '.html', 'r')
        soup = BeautifulSoup(file, 'html.parser')
        query = 'select * from ec_students_%s where xh=%s'
        if settings.DEBUG:
            print(query)
        cursor.execute(query, (get_semester_code_for_db(xq), stu['xh']))
        if not cursor.fetchall():
            print('[ADD STUDENT]')
            for class_time in range(1, 8):
                for row_number in range(1, 7):
                    query_selector = 'div[id="' + get_row_code(row_number) + '-' + str(
                        class_time) + '-2"] a'
                    for i in soup.select(query_selector):  # i 为 a 元素
                        class_info['clsname'] = i.contents[0]
                        class_info['teacher'] = 'None' if not i.select('font[title="老师"]') else \
                            i.select('font[title="老师"]')[0].string
                        class_info['duration'] = 'None' if not i.select('font[title="周次"]') else \
                            i.select('font[title="周次"]')[0].string
                        class_info['week'] = 'None' if not i.select('font[title="单双周"]') else \
                            i.select('font[title="单双周"]')[0].string
                        class_info['location'] = 'None' if not i.select('font[title="上课地点教室"]') else \
                            i.select('font[title="上课地点教室"]')[0].string
                        class_str = str(class_info['clsname']) + str(class_info['teacher']) + str(
                            class_info['duration']) + str(class_info['week']) + str(class_info['location']) + str(
                            class_time) + str(row_number)
                        md5 = hashlib.md5()
                        md5.update(class_str.encode('utf-8'))
                        class_info['hash'] = md5.hexdigest()
                        class_list.append(md5.hexdigest())
                        query = "select * from ec_classes_%s where id=%s"
                        if settings.DEBUG:
                            print(query)
                        cursor.execute(query, (get_semester_code_for_db(xq), md5.hexdigest()))
                        class_fetch_result = cursor.fetchall()
                        if not class_fetch_result:
                            print('[ADD CLASS]', end='')
                            students_set.clear()
                            students_set.add(stu['xh'])
                            query = "insert into ec_classes_%s (clsname, day, time, teacher, duration, week, location, students, id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            if settings.DEBUG:
                                print(query)
                            cursor.execute(query, (
                                get_semester_code_for_db(xq), str(class_info['clsname']), class_time, row_number,
                                str(class_info['teacher']),
                                str(class_info['duration']), str(class_info['week']), str(class_info['location']),
                                json.dumps(students_set),
                                md5.hexdigest()))
                        else:
                            print('[APPEND STUDENT]', end='')
                            students_set.clear()
                            students_set = json.loads(class_fetch_result[0][7])
                            # For unknown reason, education management system in CSU may show your same classes twice,
                            # hence you need to check whether this happens
                            if stu['xh'] not in students_set:
                                students_set.add(stu['xh'])
                                query = "update ec_classes_%s set students=%s where id=%s"
                                if settings.DEBUG:
                                    print(query)
                                cursor.execute(query, (
                                    get_semester_code_for_db(xq), json.dumps(students_set), md5.hexdigest()))
                        del md5
                        print(class_info)
                        class_info.clear()
            query = "insert into ec_students_%s (xs0101id, name, xh, classes) values (%s, %s, %s, %s)"
            if settings.DEBUG:
                print('Classlist(%s): %s' % (len(class_list), class_list))
            class_list.clear()
            if settings.DEBUG: print(query)
            cursor.execute(query, (
                get_semester_code_for_db(xq), stu['xs0101id'], stu['xm'], stu['xh'], json.dumps(class_list)))
            conn.commit()
        else:
            print('[PASS] STUDENT ALREADY EXISTS')
        print('\n')
    cursor.close()
    conn.close()


if __name__ == '__main__':
    xq = input('Input a semester(2016-2017-2 by default):')
    process_data(xq)
