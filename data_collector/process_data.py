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
import predefined
from termcolor import cprint


def process_data(xq):
    class_info = {}
    class_list = []
    students_list = []
    names_json = open("stu_data.json")
    names = json.load(names_json)
    conn = mysql.connector.connect(**settings.MYSQL_CONFIG)
    cursor = conn.cursor()
    for stu in names:
        cprint('Processing student: [%s]%s' % (stu['xh'], stu['xm']), attrs=["bold"])
        file_addr = os.path.join('raw_data', stu['xs0101id'])
        file = open(file_addr + '.html', 'r')
        soup = BeautifulSoup(file, 'html.parser')
        query = 'SELECT * FROM ec_students_' + get_semester_code_for_db(xq) + ' WHERE xh=%s'
        if settings.DEBUG:
            predefined.print_formatted_info(query)
        cursor.execute(query, (stu['xh'],))
        if not cursor.fetchall():
            cprint('[ADD STUDENT]', attrs=['bold'])
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
                        query = "SELECT * FROM ec_classes_" + get_semester_code_for_db(xq) + " WHERE id=%s"
                        if settings.DEBUG:
                            predefined.print_formatted_info(query)
                        cursor.execute(query, (md5.hexdigest(),))
                        class_fetch_result = cursor.fetchall()
                        if not class_fetch_result:
                            cprint('[ADD CLASS]', end='', color="blue", attrs=['bold'])
                            students_list.clear()
                            students_list.append(stu['xh'])
                            query = "INSERT INTO ec_classes_" + get_semester_code_for_db(
                                xq) + "(clsname, day, time, teacher, duration, week, location, students, id) VALUES (" \
                                      "%s, %s, %s, %s, %s, %s, %s, %s, %s) "
                            if settings.DEBUG:
                                predefined.print_formatted_info(query)
                            cursor.execute(query, (
                                str(class_info['clsname']), class_time, row_number,
                                str(class_info['teacher']),
                                str(class_info['duration']), str(class_info['week']), str(class_info['location']),
                                json.dumps(students_list),
                                md5.hexdigest()))
                            conn.commit()
                        else:
                            students_list.clear()
                            students_list = json.loads(class_fetch_result[0][7])
                            # For unknown reason, education management system in CSU may show your same classes twice,
                            # hence you need to check whether this happens
                            if stu['xh'] not in students_list:
                                students_list.append(stu['xh'])
                                query = "UPDATE ec_classes_" + get_semester_code_for_db(
                                    xq) + " SET students=%s WHERE id=%s"
                                if settings.DEBUG:
                                    predefined.print_formatted_info(query)
                                cursor.execute(query, (json.dumps(students_list), md5.hexdigest()))
                                conn.commit()
                                cprint('[APPEND STUDENT]', end='', color='blue', attrs=['bold'])
                        del md5
                        print(class_info)
                        class_info.clear()
            query = "INSERT INTO ec_students_" + get_semester_code_for_db(
                xq) + " (xs0101id, name, xh, classes) VALUES (%s, %s, %s, %s)"
            # 对 class_list 去重
            class_list_final = list(set(class_list))
            class_list_final.sort(key=class_list.index)
            if settings.DEBUG:
                print('Class list(%s): %s' % (len(class_list_final), class_list_final))
                predefined.print_formatted_info(query)
            cursor.execute(query, (stu['xs0101id'], stu['xm'], stu['xh'], json.dumps(class_list_final)))
            conn.commit()
            class_list.clear()
            class_list_final.clear()
        else:
            cprint('[PASS] STUDENT ALREADY EXISTS', color='green', attrs=['bold'])
        print('\n')
    cursor.close()
    conn.close()
    cprint("Finished!", color='red')


if __name__ == '__main__':
    semester = input('Input a semester(2016-2017-2 by default):')
    if not semester:
        semester = settings.GLOBAL_semester
    process_data(semester)
