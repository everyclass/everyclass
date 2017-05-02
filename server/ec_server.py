import mysql.connector
import json
import time
from termcolor import cprint
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)
app.config.update(dict(
    MYSQL_CONFIG={
        'user': 'everyclass_user',
        'password': 'everyclass_pwd',
        'host': '127.0.0.1',
        'port': '3306',
        'database': 'everyclass',
        'raise_on_warnings': True,
    },
    DEBUG=True,
    SECRET_KEY='development key',
    SEMESTER='2016-2017-2',
    DATA_LAST_UPDATE_TIME='Apr. 29, 2017'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


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


# 调试输出函数
def print_formatted_info(info, show_debug_tip=False, info_about="DEBUG"):
    if show_debug_tip:
        cprint("-----" + info_about + "-----", "blue", attrs=['bold'])
    if isinstance(info, dict):
        for (k, v) in info.items():
            print("%s =" % k, v)
    elif isinstance(info, str):
        cprint(info, attrs=["bold"])
    else:
        for each_info in info:
            print(each_info)
    if show_debug_tip:
        cprint("----" + info_about + " ENDS----", "blue", attrs=['bold'])


def faculty_lookup(student_id):
    code = student_id[0:2]
    if code == '01':
        return '地球科学与信息物理学院'
    elif code == '02':
        return '资源与安全工程学院'
    elif code == '03':
        return '资源加工与生物工程学院'
    elif code == '04':  # Not sure
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
    else:  # international students and so on
        return '其他'


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


# 获得一个学生的全部课程，学生存在则返回学号、姓名、课程 dict（键值为 day、time 组成的 tuple），否则引出 exception
def get_classes_for_student(student_id):
    db = get_db()
    cursor = db.cursor()
    mysql_query = "SELECT * FROM ec_students_" + get_semester_code_for_db(app.config['SEMESTER']) + " WHERE xh=%s"
    cursor.execute(mysql_query, (student_id,))
    result = cursor.fetchall()
    if not result:
        cursor.close()
        raise NoStudentException
    else:
        student_name = result[0][1]
        student_classes_list = json.loads(result[0][3])
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
        return student_id, student_name, student_classes


# 获得一门课程的全部学生，若有学生，返回学生列表（包含姓名、学号、学院、专业、班级），否则引出 exception
def get_students_in_class(class_id):
    db = get_db()
    cursor = db.cursor()
    mysql_query = "SELECT students FROM ec_classess_" + get_semester_code_for_db(
        app.config['SEMESTER']) + " WHERE id=%s"
    cursor.execute(mysql_query, (class_id,))
    result = cursor.fetchall()
    if not result:
        cursor.close()
        raise NoClassException
    else:
        students = json.loads(result[0][0])
        students_info = list()
        if not students:
            cursor.close()
            raise NoStudentException
        for each_student in students:
            mysql_query = "SELECT name,xh FROM ec_students_" + get_semester_code_for_db(
                app.config['SEMESTER']) + " WHERE xh=%s"
            cursor.execute(mysql_query, (each_student,))
            result = cursor.fetchall()
            # 信息包含姓名、学号、学院、专业、班级
            students_info.append([result[0][0], result[0][1], faculty_lookup(each_student)])
        cursor.close()
        return students_info


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


# 关于
@app.route('/guide')
def about():
    return render_template('about.html')

# 用于查询本人课表
@app.route('/query', methods=['POST'])
def query():
    try:
        student_id, student_name, student_classes = get_classes_for_student(request.form['id'])
    except NoStudentException:
        flash('对不起，没有在数据库中找到你哦。学号是不是输错了？你刚刚输入的是%s' % request.form['id'])
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


@app.route('/calendar')
def generate_ics():
    from generate_ics import generate_ics
    return render_template('ics.html', ics=generate_ics(request.form['id']))


# 同学名单
@app.route('/classmates')
def get_classmates():
    try:
        students_info = get_students_in_class(request.form['class_id'])
    except NoClassException:
        flash('没有这门课程')
        return redirect(url_for('main'))
    except NoStudentException:
        flash('这门课程没有学生')
        return redirect(url_for('main'))
    else:
        return render_template('classmate.html', students=students_info)


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
