# -*- coding: utf-8 -*-
# This file contains predefined information which needs to be imported by other modules
# Created Apr. 19, 2017 by Frederic
from termcolor import colored, cprint


# Function: get_row_code
# Used to get row code for each row in separate files in raw_data
# Usage:
# Example: get_row_code(1)
def get_row_code(row_num):
    if row_num == 1:
        return 'BFCA2900002E48B1B20AD34D4E4E50C8'
    elif row_num == 2:
        return '11DD7A497F57416EA11C4D01AD1DA66A'
    elif row_num == 3:
        return 'A777C6C778AB462BB742C6640D58E0DD'
    elif row_num == 4:
        return '1AC61925F56341B494CBA5AEA3C4AC3B'
    elif row_num == 5:
        return 'ADD7F6354105427EBA9EE72883DAF69F'
    else:
        return '921723A66500482189BDEF39E4C87D61'


# Function: get_semester_code_for_db
# For tables like ec_students or ec_classes, each semesters will have their own
# tables to reduce server pressure while querying. For example, the student table for second semester during 2016 and
#  2017 will be "ec_students_16_17_2". This function transforms semester codes like "2016-2017-2" to table name type
# like "16_17_2"
# Usage:
# Example: get_semester_code_for_db("2016-2017-2")
def get_semester_code_for_db(xq):
    if xq == '':
        import settings
        return get_semester_code_for_db(settings.GLOBAL_semester)
    else:
        import re
        splited = re.split('-', xq)
        return str(splited[0][2:4] + "_" + splited[1][2:4] + "_" + splited[2])


# Function: get_day_for_class
# Used to transform day like "周一" to digital form "1"
# Usage:
# Example: get_day_for_class("周一")
def get_day_for_class(chinese):
    if chinese == '周一':
        return '1'
    elif chinese == '周二':
        return '2'
    elif chinese == '周三':
        return '3'
    elif chinese == '周四':
        return '4'
    elif chinese == '周五':
        return '5'
    elif chinese == '周六':
        return '6'
    else:
        return '7'


# Function: get_time_for_class
# Used to transform time like "1-2" to form "1"
# Usage:
# Example: get_time_for_class("1-2")
#    Parameter is expected to be "1-2", "3-4", "5-6", "7-8", "9-10", "11-12"
def get_time_for_class(text):
    if text == '1-2':
        return '1'
    elif text == '3-4':
        return '2'
    elif text == '5-6':
        return '3'
    elif text == '7-8':
        return '4'
    elif text == '9-10':
        return '5'
    else:
        return '6'


# Function: get_faculty_name
def get_faculty_name(code):
    if code == '01':
        return '地球科学与信息物理学院'
    elif code == '02':
        return '资源与安全工程学院'
    elif code == '03':
        return '资源加工与生物工程学院'
    elif code == '04':# Not sure
        return '地球科学与信息物理学院'
    elif code == '05':
        return '冶金与环境学院'
    elif code == '06':
        return '材料科学与工程学院'
    elif code == '07':
        return '粉末冶金研究院'
    elif code == '08':
        return '机电工程学院'
    elif code == '09':
        return '信息科学与工程学院'
    elif code == '10':
        return '能源科学与工程学院'
    elif code == '11':
        return '交通运输工程学院'
    elif code == '12':
        return '土木工程学院'
    elif code == '13':
        return '数学与统计学院'
    elif code == '14':
        return '物理与电子学院'
    elif code == '15':
        return '化学化工学院'
    elif code == '16':
        return '商学院'
    elif code == '17':
        return '文学与新闻传播学院'
    elif code == '18':
        return '外国语学院'
    elif code == '19':
        return '建筑与艺术学院'
    elif code == '20':
        return '法学院'
    elif code == '21':
        return '马克思主义学院'
    elif code == '22':
        return '湘雅医学院'
    elif code == '23':
        return '基础医学院'
    elif code == '24':
        return '药学院'
    elif code == '25':
        return '湘雅护理学院'
    elif code == '26':
        return '公共卫生学院'
    elif code == '27':
        return '口腔医学院'
    elif code == '28':
        return '生命科学学院'
    elif code == '37':
        return '生命科学学院'
    elif code == '39':
        return '软件学院'
    elif code == '42':
        return '航空航天学院'
    elif code == '43':
        return '公共管理学院'
    elif code == '66':
        return '体育教研部'
    elif code == '93':
        return '国际合作与交流处'
    else: # international students and so on
        return '其他'


# Function: print_formatted_info
# Used to print debug info
# Usage:
# 1. print_formatted_info([list, dict and so on data types])
#    Won't show "---DEBUG---" flags
# 2. print_formatted_info([list, dict and so on data types],True)
#    Will show "---DEBUG---" flags
def print_formatted_info(info, show_debug_tip=False, info_about="DEBUG"):
    if show_debug_tip:
        cprint("-----" + info_about + "-----", "blue")
    if isinstance(info, dict):
        for (k, v) in info.items():
            print("%s =" % k, v)
    elif isinstance(info, str):
        cprint(info, attrs=["bold"])
    else:
        for each_info in info:
            print(each_info)
    if show_debug_tip:
        cprint("----" + info_about + " ENDS----", "blue")


# Function: create_tables
# Used to create tables for a semester
def create_tables():
    import mysql.connector
    import settings
    conn = mysql.connector.connect(**settings.MYSQL_CONFIG)
    cursor = conn.cursor()
    try:
        for line in open('everyclass.sql', 'r'):
            cursor.execute(line)
    except mysql.connector.errors.DatabaseError as e:
        cprint("Mysql Exception %d: %s" % (e.args[0], e.args[1]), "red")
    conn.commit()
    conn.close()


# Function: input_accepted
# Used to check if input is accepted when predefined.py is executed
def input_accepted(order):
    if order == "1":
        print("This function will execute SQL sentences in 'everyclass.sql'\n"
              "If you want to create table for a new semester you need to edit semester code in 'everyclass.sql' first.")
        cprint("Input Y if you want to create table for a semester", attrs=["bold"])
        sure = input()
        if sure == "Y" or sure == "y":
            create_tables()
            exit()
    else:
        return 0


if __name__ == "__main__":
    order = 0
    while not input_accepted(order):
        cprint("EveryClass tools:", "green", attrs=["bold"])
        print("1: Create table for a new semester")
        order = input()
