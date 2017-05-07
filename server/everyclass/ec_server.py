from flask import Flask, g, redirect, url_for, render_template, send_from_directory

from everyclass.cal import cal_blueprint
from everyclass.config import load_config
from everyclass.query import query_blueprint

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object(load_config())


# 结束时关闭数据库连接
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'mysql_db'):
        g.mysql_db.close()


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
