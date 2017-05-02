# 检查ec_stu_id_prefix表中的前缀还有哪些是未知的

import mysql.connector
import settings
from predefined import get_semester_code_for_db

conn = mysql.connector.connect(**settings.MYSQL_CONFIG)
cursor = conn.cursor()
query = 'SELECT xh FROM ec_students_' + get_semester_code_for_db(settings.GLOBAL_semester)
cursor.execute(query)
students = cursor.fetchall()
unknown_prefixes = set()
for each_student in students:
    if len(each_student[0]) == 10 and each_student[0].isdigit():
        query = 'SELECT prefix FROM ec_stu_id_prefix WHERE prefix=%s'
        cursor.execute(query, (each_student[0][0:4],))
        if not cursor.fetchall():
            if each_student[0][0:4] not in unknown_prefixes:
                unknown_prefixes.add(each_student[0][0:4])
                print(each_student[0][0:4])
print('total:%s' % len(unknown_prefixes))
cursor.close()
conn.close()
