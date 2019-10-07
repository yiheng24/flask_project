import os
import hashlib
import datetime
import functools

from flask import render_template
from flask import redirect, session
from flask_restful import Resource

from models import *
from main import app
# from main import csrf
from models import Picture
from main import api
from main import STATICFILES_DIR






def set_password(password):
    npw = hashlib.md5()
    npw.update(password.encode())
    result = npw.hexdigest()
    return result


def login_valid(fun):
    @functools.wraps(fun)
    def inner(*args, **kwargs):
        username = request.cookies.get('username')
        id = request.cookies.get('id', '0')
        user = User.query.get(int(id))
        session_username = session.get('username')
        if user:
            if username == session_username and user.user_name == username:
                return fun(*args, **kwargs)
            else:
                return redirect('/login/')
        else:
            return redirect('/login/')

    return inner


class Calendar:
    def __init__(self):
        self.result = []

        big_month = [1, 3, 5, 7, 8, 10, 12]
        small_month = [4, 6, 9, 11]

        now = datetime.datetime.now()
        month = now.month

        first_date = datetime.datetime(now.year, now.month, 1, 0, 0)

        if month in big_month:
            day_range = range(1, 32)
        elif month in small_month:
            day_range = range(1, 31)
        else:
            if not self.leep_year(now.year):
                day_range = range(1, 29)
            else:
                day_range = range(1, 30)
        day_range = list(day_range)

        first_week = first_date.weekday()

        line1 = ['empty' for e in range(first_week)]

        for d in range(7 - first_week):
            flag = 0
            if day_range[0] > now.day:
                flag = 2
            elif day_range[0] == now.day:
                flag = 1
            line1.append({'day': str(day_range.pop(0)), 'course': 'python', 'flag': flag})
        self.result.append(line1)

        while day_range:
            line = []
            for i in range(7):
                if len(line) < 7 and day_range:
                    flag = 0
                    if day_range[0] > now.day:
                        flag = 2
                    elif day_range[0] == now.day:
                        flag = 1
                    line.append(
                        {'day': str(day_range.pop(0)), 'course': 'python', 'flag': flag}
                    )
                else:
                    line.append('empty')
            self.result.append(line)

    def calendar_month(self):
        return self.result

    def leep_year(self, year):
        return (year % 400 == 0) or (year % 4 == 0 and year % 100 == 0)

    def print_result(self):
        print('星期一  星期二  星期三  星期四  星期五  星期六  星期日')
        for line in self.result:
            for day in line:
                print(day, end='  ')
            print()


@app.route('/base/')
def base():
    return render_template('base.html')


@app.route('/login/', methods=['GET', 'POST'])
# @csrf.exempt
def login():
    error = ''
    if request.method == 'POST':
        form_data = request.form
        email = form_data.get('email')
        password = form_data.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            db_password = user.password
            if set_password(password) == db_password:
                response = redirect('/index/')
                response.set_cookie('username', user.user_name)
                response.set_cookie('email', user.email)
                response.set_cookie('id', str(user.id))
                session['username'] = user.user_name
                return response
            else:
                error = '密码错误'
        else:
            error = '用户名错误'

    return render_template('login.html', error=error)


@app.route('/logout/')
def logout():
    response = redirect('/login/')
    response.delete_cookie('username')
    response.delete_cookie('email')
    response.delete_cookie('id')
    del session['username']
    return response


#

@app.route('/index/')
@login_valid
# @csrf.exempt
def index():
    return render_template('index.html')


@app.route('/userinfo/')
def userinfo():
    calendar_month = Calendar().calendar_month()
    return render_template('userinfo.html', **locals())


from flask import request
from models import User


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User()
        user.user_name = username
        user.email = email
        user.password = set_password(password)
        user.save()

    return render_template('register.html')


@app.route('/leave/', methods=['get', 'post'])
@login_valid
# @csrf.exempt
def leave():
    if request.method == 'POST':
        data = request.form
        request_user = data.get('request_user')
        request_type = data.get('select')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        phone = data.get('phone')
        request_reason = data.get('request_reason')

        leave = Leave()
        leave.request_id = request.cookies.get('id')
        leave.request_name = request_user
        leave.request_type = request_type
        leave.request_start_time = start_time
        leave.request_end_time = end_time
        leave.request_phone = phone
        leave.request_reason = request_reason
        leave.request_status = '0'
        leave.save()
    return render_template('leave.html')


@app.route('/leave_msg/<int:page>/')
@login_valid
# @csrf.exempt
def leave_msg(page):
    # page=int(page)
    leaves = Leave.query.all()
    pager = Pager(leaves, 2)
    page_data = pager.page_data(page)
    # print(page_data)
    # print(leaves)
    # print(pager.page_range)
    return render_template('leave_msg.html', **locals())


from flask import jsonify


@app.route('/cancel/', methods=['get', 'post'])
# @csrf.exempt
def cancel():
    # id = request.args.get('id')
    id = request.form.get('id')
    leave = Leave.query.get(int(id))
    leave.delete()
    return jsonify({'data': '数据移除成功'})


class Pager:
    def __init__(self, data, page_size):
        self.data = data
        self.page_size = page_size
        self.is_start = False
        self.is_end = False
        self.page_count = len(data)
        self.previous_page = 0
        self.next_page = 0
        self.page_number = self.page_count / page_size
        if self.page_number == int(self.page_number):
            self.page_number = int(self.page_number)
        else:
            self.page_number = int(self.page_number) + 1
        self.page_range = range(1, self.page_number + 1)

    # @csrf.exempt
    def page_data(self, page):
        self.next_page = int(page) + 1
        self.previous_page = int(page) - 1
        if page <= self.page_range[-1]:
            page_start = (page - 1) * self.page_size
            page_end = page * self.page_size
            data = self.data[page_start: page_end]
            if page == 1:
                self.is_start = True
            else:
                self.is_start = False
            if page == self.page_range[-1]:
                self.is_end = True
            else:
                self.is_end = False
        else:
            data = ['没有要查询的数据']

        return data


from forms import TaskFrom


@app.route('/add_task/', methods=['get', 'post'])
# @csrf.exempt
def add_task():
    errors = ''
    task = TaskFrom()
    if request.method == 'POST':
        if task.validate_on_submit():
            form_data = task.data
        else:
            errors_list = list(task.errors.keys())
            errors = task.errors
            print(errors)
    return render_template('add_task.html', **locals())

@app.route('/picture/',methods=['get','post'])
def picture():
    p={'picture':'img/photo.jpg'}
    if request.method == 'POST':
        file=request.files.get('photo')
        file_name=file.filename
        file_path='img/%s'%file_name
        save_path=os.path.join(STATICFILES_DIR,file_path)
        file.save(save_path)
        p=Picture()
        p.picture=file_path
        p.save()
    return render_template('picture.html',**locals())

@api.resource('/Api/leave/')
class LeaveApi(Resource):
    def __init__(self):
        super(LeaveApi,self).__init__()
        self.result={
            'version':'1.0',
            'data':''
        }

    def set_data(self,leave):
        result_data={
            'request_name': leave.request_name,
            'request_type': leave.request_type,
            'request_start_time': leave.request_start_time,
            'request_end_time': leave.request_end_time,
            'request_reason': leave.request_reason,
            'request_phone': leave.request_phone,
        }
        return result_data

    def get(self):
        data=request.args
        id=data.get('id')
        if id:
            leave=Leave.query.get(int(id))
            result_data=self.set_data(leave)
        else:
            leaves=Leave.query.all()
            result_data=[]
            for leave in leaves:
                result_data.append(self.set_data(leave))
        self.result['data']=result_data
        return self.result

    def post(self):
        data=request.form

        request_id=data.get('request_id')
        request_name=data.get('request_name')
        request_type=data.get('request_type')
        request_start_time=data.get('request_start_time')
        request_end_time=data.get('request_end_time')
        request_reason=data.get('request_reason')
        request_phone=data.get('request_phone')

        leave=Leave()
        leave.request_id=request_id
        leave.request_name=request_name
        leave.request_type=request_type
        leave.request_start_time=request_start_time
        leave.request_end_time=request_end_time
        leave.request_phone=request_phone
        leave.request_reason=request_reason
        leave.request_status=0
        leave.save()

        self.result['data']=self.set_data(leave)
        return self.result


    def put(self):
        data=request.form
        id = data.get('id')
        leave = Leave.query.get(int(id))
        for key,value in data.items():
            if key != 'id':
                setattr(leave,key,value)
        leave.save()
        self.result['data']=self.set_data(leave)
        return self.result

    def delete(self):
        data=request.form
        id=data.get('id')
        leave=Leave.query.get(int(id))
        leave.delete()
        self.result['data']='id:%s的数据删除成功'%id

        return self.result