from flask.blueprints import Blueprint
from flask import render_template
import os  
#from models.lecturer import Lecturer
import datetime
import cx_Oracle
from flask import request
import sys
# from datetime import datetime
# from models.subject import Subject
# from models.interval import Interval
# from models.group import Group
# from models.schedule import Schedule


index1 = Blueprint('index1', __name__,
                template_folder='templates',
                static_folder='static')


@index1.route('/')
def index():
    lib_dir= r"D:\\Documents\\sqldeveloper-19.2.1.247.2212-no-jre\\instantclient-basic-windows.x64-19.10.0.0.0dbru\\instantclient_19_10"
    os.environ["PATH"] = lib_dir + ";" + os.environ["PATH"]
    #cx_Oracle.init_oracle_client(lib_dir= r"D:\\Documents\\sqldeveloper-19.2.1.247.2212-no-jre\\instantclient-basic-windows.x64-19.10.0.0.0dbru\\instantclient_19_10")
    #conn = cx_Oracle.connect('KURS/KOLOBOK@localhost:1521/service')
    dsn = cx_Oracle.makedsn(host='localhost', port=1521, sid='xe')
    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    #dsn = cx_Oracle.makedsn(host='localhost', port=1521, sid='xe')
    # dsn = cx_Oracle.makedsn(
    # 'localhost', 
    # '1521', 
    # service_name='orcl'
    # )
    # conn = cx_Oracle.connect(
    # user='KURS', 
    # password='KOLOBOK', 
    # dsn=dsn
    # )
    mycursor = conn.cursor()
    mycursor.execute('select  tt.code, tt.discount from promo tt')
 
    # парсим полученный результат в список кортежей
    result = mycursor.fetchall()
 
    # бежим по записям и выполняем любые действия 
    for  (myfield1, myfield2) in result:
            #выводим на экран значения полей 
            print(str(myfield1) + '|' + str(myfield2))

    # после выполнения всех нужных нам действий закрываем соединение с базой 
    conn.close
    # first = datetime.datetime.strptime("09.11.2020", "%d.%m.%Y")
    # today = datetime.date.today()
    # now = datetime.datetime.now()
    # #now2 = now.strftime("%d-%m-%Y")
    # razn = ((now - first).days)

    # if (razn // 7) % 2 == 0:
    #     todned = "Нечетная"
    # else:
    #     todned = "Четная"
    # days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    # trv = ['9:30 - 11:05','11:20 - 12:55','13:10 - 14:45','15:25 - 17:00']
    # cur_group = "БФИ1801"
    # group_id = db.session.query(Group.id).filter(Group.name==cur_group).first()[0]
    # schedule = db.session.query(Schedule).filter(Schedule.group_id==group_id)
    # #group_id = db.session.query(Group.id).filter(Group.name==group).first()[0]
    return render_template('index.html')

# @lecturers.route('/',methods=['post', 'get'])
# def chooseGroup():
#     if request.method == 'POST':
#         cur_group = request.form.get('cur_group')

    
#     first = datetime.datetime.strptime("09.11.2020", "%d.%m.%Y")
#     today = datetime.date.today()
#     now = datetime.datetime.now()
#     #now2 = now.strftime("%d-%m-%Y")
#     razn = ((now - first).days)

#     if (razn // 7) % 2 == 0:
#         todned = "Нечетная"
#     else:
#         todned = "Четная"
#     days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
#     trv = ['9:30 - 11:05','11:20 - 12:55','13:10 - 14:45','15:25 - 17:00']
#     message = ''
#     group_id = db.session.query(Group.id).filter(Group.name==cur_group).first()[0]
#     schedule = db.session.query(Schedule).filter(Schedule.group_id==group_id)


#     return render_template('index.html', curdate = today.strftime('%d-%m-%Y'), cur_group=cur_group, todned = todned, days = days, trvs = trv, lecturers=Lecturer.query.all(),subjects=Subject.query.all(),intervals=Interval.query.all(),group_names=Group.query.all(),schedules=schedule)