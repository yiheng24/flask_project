import datetime
from flask import render_template
from main import app
from models import Course

class Calendar:
    def __init__(self):
        self.result=[]

        big_month=[1,3,5,7,8,10,12]
        small_month=[4,6,9,11]

        now=datetime.datetime.now()
        month=now.month

        first_date=datetime.datetime(now.year,now.month,1,0,0)

        if month in big_month:
            day_range=range(1,32)
        elif month in small_month:
            day_range=range(1,31)
        else:
            if not self.leep_year(now.year):
                day_range=range(1,29)
            else:
                day_range=range(1,30)
        day_range=list(day_range)

        first_week=first_date.weekday()

        line1=['empty' for e in range(first_week)]

        for d in range(7-first_week):
            flag=0
            if day_range[0]>now.day:
                flag=2
            elif day_range[0]==now.day:
                flag=1
            line1.append({'day':str(day_range.pop(0)),'course':'python','flag':flag})
        self.result.append(line1)



        while day_range:
            line=[]
            for i in range(7):
                if len(line)<7 and day_range:
                    flag=0
                    if day_range[0]>now.day:
                        flag=2
                    elif day_range[0]==now.day:
                        flag=1
                    line.append(
                        {'day':str(day_range.pop(0)),'course':'python','flag':flag}
                    )
                else:
                    line.append('empty')
            self.result.append(line)

    def calendar_month(self):
        return self.result

    def leep_year(self,year):
        return (year%400==0) or (year%4==0 and year%100==0)

    def print_result(self):
        print('星期一  星期二  星期三  星期四  星期五  星期六  星期日')
        for line in self.result:
            for day in line:
                print(day,end='  ')
            print()



@app.route('/base/')
def base():
    return render_template('base.html')

@app.route('/index/')
def index():
    # c=Course()
    # c.c_id='001'
    # c.c_name='python'
    # c.c_time=datetime.datetime.now()
    # c.save()
    # data=Course.query.all()
    return render_template('index.html',**locals())

@app.route('/userinfo/')
def userinfo():

    calendar_month = Calendar().calendar_month()
    return render_template('userinfo.html',**locals())

from flask import request
from models import User
@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method =='POST':
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User()
        user.user_name=username
        user.email=email
        user.password=password
        user.save()

    return render_template('register.html')


if __name__=='__main__':
    Calendar().print_result()