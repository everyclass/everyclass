# 对学生的课程去重
import mysql.connector
import settings
import json
from predefined import get_semester_code_for_db

conn = mysql.connector.connect(**settings.MYSQL_CONFIG)
cursor = conn.cursor()
query = 'SELECT xh,classes FROM ec_students_' + get_semester_code_for_db('2016-2017-2')
cursor.execute(query)
result = cursor.fetchall()
for each_student in result:
    classes = list(set(json.loads(each_student[1])))
    classes.sort(key=json.loads(each_student[1]).index)
    query = 'UPDATE ec_students_' + get_semester_code_for_db('2016-2017-2') + ' SET classes=%s WHERE xh=%s'
    cursor.execute(query, (json.dumps(classes), each_student[0]))
conn.commit()
cursor.close()
conn.close()
