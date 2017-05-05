import mysql.connector
import json
import os
import re
from config import load_config
from predefine import get_day_chinese, get_time_chinese, faculty_lookup, is_chinese, print_formatted_info
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, escape, send_from_directory

app = Flask(__name__)
os.environ['MODE'] = 'DEVELOPMENT'
app.config.from_object(load_config())


class NoClassException(ValueError):
    pass


class NoStudentException(ValueError):
    pass


# 获取用于数据表命名的学期，输入2016-2017-2，输出16_17_2
def get_semester_code_for_db(xq):
    if xq == '':
        return get_semester_code_for_db(app.config['SEMESTER'])
    else:
        import re
        splited = re.split('-', xq)
        return str(splited[0][2:4] + "_" + splited[1][2:4] + "_" + splited[2])


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


# 查询学生所在班级
def class_lookup(student_id):
    re_split_result = re.findall(r'\d{4}', student_id)[1]
    if 10 < int(re_split_result[0:2]) < 20:  # 正则提取后切片切出来的班级一般是正确的，但有的学生学号并不是标准格式，因此这里对班级的前两位做一个年份判断(2010<年份<2020)
        return re_split_result
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
    mysql_query = "SELECT name,classes FROM ec_students_" + get_semester_code_for_db(
        app.config['SEMESTER']) + " WHERE xh=%s"
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
                          get_semester_code_for_db(app.config['SEMESTER']) + " WHERE id=%s"
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
    mysql_query = "SELECT students,clsname,day,time,teacher FROM ec_classes_" + get_semester_code_for_db(
        app.config['SEMESTER']) + " WHERE id=%s"
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
            mysql_query = "SELECT name FROM ec_students_" + get_semester_code_for_db(
                app.config['SEMESTER']) + " WHERE xh=%s"
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


# 帮助
@app.route('/guide')
def guide():
    return render_template('guide.html')


# 用于查询本人课表
@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.values.get('id'):  # 带有 id 参数（可为姓名或学号）
        id_or_name = request.values.get('id')
        if is_chinese(id_or_name[0:1]) and is_chinese(id_or_name[-1:]):  # 首末均为中文
            db = get_db()
            cursor = db.cursor()
            mysql_query = "SELECT name,xh FROM ec_students_" + get_semester_code_for_db(
                app.config['SEMESTER']) + " WHERE name=%s"
            cursor.execute(mysql_query, (id_or_name,))
            result = cursor.fetchall()
            if cursor.rowcount > 1:  # 查询到多个同名，进入选择界面
                students_list = list()
                for each_student in result:
                    students_list.append([each_student[0], each_student[1], faculty_lookup(each_student[1]),
                                          major_lookup(each_student[1]), class_lookup(each_student[1])])
                return render_template("query_same_name.html", count=cursor.rowcount, student_info=students_list)
            elif cursor.rowcount == 1:  # 仅能查询到一个人，则赋值学号
                student_id = result[0][1]
            else:
                flash("没有这个名字的学生哦")
                return redirect(url_for('main'))
        else:  # id 为学号
            student_id = request.values.get('id')
        session['stu_id'] = student_id
    elif session['stu_id']:
        student_id = session['stu_id']
    else:
        return redirect(url_for('main'))
    try:
        student_name, student_classes = get_classes_for_student(student_id)
    except NoStudentException:
        flash('对不起，没有在数据库中找到你哦。学号是不是输错了？你刚刚输入的是%s' % escape(student_id))
        return redirect(url_for('main'))
    else:
        # 空闲周末判断，考虑到大多数人周末都是没有课程的
        empty_wkend = True
        for cls_time in range(1, 7):
            for cls_day in range(6, 8):
                if (cls_day, cls_time) in student_classes:
                    empty_wkend = False
        # 空闲课程判断，考虑到大多数人11-12节都是没有课程的
        empty_6 = True
        for cls_day in range(1, 8):
            if (cls_day, 6) in student_classes:
                empty_6 = False
        empty_5 = True
        for cls_day in range(1, 8):
            if (cls_day, 5) in student_classes:
                empty_5 = False
        return render_template('query.html', name=student_name, stu_id=student_id, classes=student_classes,
                               empty_wkend=empty_wkend, empty_6=empty_6, empty_5=empty_5)


# 导出日历交换格式文件
@app.route('/calendar')
def generate_ics():
    if request.values.get('id'):
        session['stu_id'] = request.values.get('id')
    if session['stu_id']:
        from generate_ics import generate_ics
        student_name, student_classes = get_classes_for_student(session['stu_id'])
        generate_ics(session['stu_id'], student_name, student_classes)
        return render_template('ics.html', student_id=session['stu_id'])
    else:
        return redirect(url_for('main'))


@app.route('/<student_id>.ics')
def get_ics(student_id):
    return send_from_directory("ics", student_id + ".ics")


# 同学名单
@app.route('/classmates')
def get_classmates():
    try:
        class_name, class_day, class_time, class_teacher, students_info = get_students_in_class(
            request.values.get('class_id', None))
    except NoClassException as e:
        flash('没有这门课程:%s' % (e,))
        return redirect(url_for('main'))
    except NoStudentException:
        flash('这门课程没有学生')
        return redirect(url_for('main'))
    else:
        return render_template('classmate.html', class_name=class_name, class_day=get_day_chinese(class_day),
                               class_time=get_time_chinese(class_time), class_teacher=class_teacher,
                               students=students_info)


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
    app.add_url_rule('/android-chrome-192x192.png',
                     redirect_to=url_for('static', filename='android-chrome-192x192.png'))
    app.add_url_rule('/android-chrome-512x512.png',
                     redirect_to=url_for('static', filename='android-chrome-512x512.png'))
    app.add_url_rule('/apple-touch-icon.png', redirect_to=url_for('static', filename='/images/apple-touch-icon.png'))
    app.add_url_rule('/browserconfig.xml', redirect_to=url_for('static', filename='browserconfig.xml'))
    app.add_url_rule('/favicon-16x16.png', redirect_to=url_for('static', filename='/images/favicon-16x16.png'))
    app.add_url_rule('/favicon-32x32.png', redirect_to=url_for('static', filename='/images/favicon-32x32.png'))
    app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='/images/favicon.ico'))
    app.add_url_rule('/manifest.json', redirect_to=url_for('static', filename='manifest.json'))
    app.add_url_rule('/mstile-150x150.png', redirect_to=url_for('static', filename='/images/mstile-150x150.png'))
    app.add_url_rule('/safari-pinned-tab.svg', redirect_to=url_for('static', filename='/images/safari-pinned-tab.svg'))
    app.add_url_rule('/android-chrome-192x192.png',
                     redirect_to=url_for('static', filename='/images/android-chrome-192x192.png'))
    app.add_url_rule('/android-chrome-512x512.png',
                     redirect_to=url_for('static', filename='/images/android-chrome-512x512.png'))
