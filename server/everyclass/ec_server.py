import json
import os
import re

import mysql.connector
from flask import Flask, session, g, redirect, url_for, render_template, send_from_directory

from cal import cal_blueprint
from commons import semester_code, NoClassException, NoStudentException, class_lookup, faculty_lookup
from config import load_config
from query import query_blueprint

app = Flask(__name__, static_folder='static', static_url_path='')
os.environ['MODE'] = 'DEVELOPMENT'
app.config.from_object(load_config())


# 获取当前学期，当 url 中没有显式表明 semester 时，不设置 session，而是在这里设置默认值
def semester():
    if session.get('semester', None) and session.get('semester') in app.config['AVAILABLE_SEMESTERS']:
        return session['semester']
    else:
        return app.config['DEFAULT_SEMESTER']


# 查询专业信息
def major_lookup(student_id):
    code = re.findall(r'\d{4}', student_id)[0]
    db = get_db()
    cursor = db.cursor()
    mysql_query = "SELECT name FROM ec_stu_id_prefix WHERE prefix=%s"
    cursor.execute(mysql_query, (code,))
    result = cursor.fetchall()
    if result:
        return result[0][0]
    else:
        return "未知"


# 初始化数据库连接
def connect_db():
    conn = mysql.connector.connect(**app.config['MYSQL_CONFIG'])
    return conn


# 获得数据库连接
def get_db():
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = connect_db()
    return g.mysql_db


# 结束时关闭数据库连接
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'mysql_db'):
        g.mysql_db.close()


# 获得一个学生的全部课程，学生存在则返回姓名、课程 dict（键值为 day、time 组成的 tuple），否则引出 exception
def get_classes_for_student(student_id):
    db = get_db()
    cursor = db.cursor()
    mysql_query = "SELECT name,classes FROM ec_students_" + semester_code(semester()) + " WHERE xh=%s"
    cursor.execute(mysql_query, (student_id,))
    result = cursor.fetchall()
    if not result:
        cursor.close()
        raise NoStudentException
    else:
        student_name = result[0][0]
        student_classes_list = json.loads(result[0][1])
        student_classes = dict()
        for classes in student_classes_list:
            mysql_query = "SELECT clsname,day,time,teacher,duration,week,location,id FROM ec_classes_" + \
                          semester_code(semester()) + " WHERE id=%s"
            cursor.execute(mysql_query, (classes,))
            result = cursor.fetchall()
            if (result[0][1], result[0][2]) not in student_classes:
                student_classes[(result[0][1], result[0][2])] = list()
            student_classes[(result[0][1], result[0][2])].append(dict(name=result[0][0], teacher=result[0][3],
                                                                      duration=result[0][4],
                                                                      week=result[0][5], location=result[0][6],
                                                                      id=result[0][7]))
        cursor.close()
        return student_name, student_classes


# 获得一门课程的全部学生，若有学生，返回课程名称、课程时间（day、time）、任课教师、学生列表（包含姓名、学号、学院、专业、班级），否则引出 exception
def get_students_in_class(class_id):
    db = get_db()
    cursor = db.cursor()
    mysql_query = "SELECT students,clsname,day,time,teacher FROM ec_classes_" + semester_code(
        semester()) + " WHERE id=%s"
    cursor.execute(mysql_query, (class_id,))
    result = cursor.fetchall()
    if not result:
        cursor.close()
        raise NoClassException(class_id)
    else:
        students = json.loads(result[0][0])
        students_info = list()
        class_name = result[0][1]
        class_day = result[0][2]
        class_time = result[0][3]
        class_teacher = result[0][4]
        if not students:
            cursor.close()
            raise NoStudentException
        for each_student in students:
            mysql_query = "SELECT name FROM ec_students_" + semester_code(semester()) + " WHERE xh=%s"
            cursor.execute(mysql_query, (each_student,))
            result = cursor.fetchall()
            # 信息包含姓名、学号、学院、专业、班级
            students_info.append(
                [result[0][0], each_student, faculty_lookup(each_student), major_lookup(each_student),
                 class_lookup(each_student)])
        cursor.close()
        return class_name, class_day, class_time, class_teacher, students_info


# 首页
@app.route('/')
def main():
    return render_template('index.html')


# 帮助
@app.route('/faq')
def faq():
    return render_template('faq.html')


# 关于
@app.route('/about')
def about():
    return render_template('about.html')


# 帮助
@app.route('/guide')
def guide():
    return render_template('guide.html')


app.register_blueprint(cal_blueprint)
app.register_blueprint(query_blueprint)


@app.route('/<student_id>-<semester>.ics')
def get_ics(student_id, semester):
    return send_from_directory("ics", student_id + "-" + semester + ".ics")


# 404跳转回首页
@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('main'))


# 405跳转回首页
@app.errorhandler(405)
def method_not_allowed(error):
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run()
