"""
查询相关函数
"""
from flask import Blueprint

query_blueprint = Blueprint('query', __name__)
from flask import request, render_template, flash, redirect, url_for, session, escape
from flask import current_app as app
from commons import is_chinese, semester_to_tuple, semester_code, NoStudentException, NoClassException, \
    semester_to_string, class_lookup, get_day_chinese, get_time_chinese, faculty_lookup
from ec_server import semester, get_db, major_lookup, get_classes_for_student, \
    get_students_in_class


# 用于查询本人课表
@query_blueprint.route('/query', methods=['GET', 'POST'])
def query():
    if request.values.get('semester'):
        if semester_to_tuple(request.values.get('semester')) in app.config['AVAILABLE_SEMESTERS']:
            session['semester'] = semester_to_tuple(request.values.get('semester'))
    if request.values.get('id'):  # 带有 id 参数（可为姓名或学号）
        id_or_name = request.values.get('id')
        if is_chinese(id_or_name[0:1]) and is_chinese(id_or_name[-1:]):  # 首末均为中文
            db = get_db()
            cursor = db.cursor()
            mysql_query = "SELECT name,xh FROM ec_students_" + semester_code(semester()) + " WHERE name=%s"
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
        # 学期选择器
        available_semesters = []
        for each_semester in app.config['AVAILABLE_SEMESTERS']:
            if semester() == each_semester:
                available_semesters.append([semester_to_string(each_semester), True])
            else:
                available_semesters.append([semester_to_string(each_semester), False])
        return render_template('query.html', name=[student_name,faculty_lookup(student_id),major_lookup(student_id),class_lookup(student_id)], stu_id=student_id, classes=student_classes,
                               empty_wkend=empty_wkend, empty_6=empty_6, empty_5=empty_5,
                               available_semesters=available_semesters)


# 同学名单
@query_blueprint.route('/classmates')
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
                               students=students_info, student_count=len(students_info))
