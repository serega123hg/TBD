from flask.blueprints import Blueprint
from flask import render_template
from flask import request
import cx_Oracle
import os  
import datetime 

pl = {}

lib_dir= r"D:\\Documents\\sqldeveloper-19.2.1.247.2212-no-jre\\instantclient-basic-windows.x64-19.10.0.0.0dbru\\instantclient_19_10"
os.environ["PATH"] = lib_dir + ";" + os.environ["PATH"]
dsn = cx_Oracle.makedsn(host='localhost', port=1521, sid='xe')


callcenter = Blueprint('callcenter', __name__,
                template_folder='templates',
                static_folder='static')


@callcenter.route('/callcenter', methods=['POST', 'GET'])
def index5():
    global pl

    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    mycursor = conn.cursor()
    mycursor.execute('select PlanID, Name from Plans')
    result1 = mycursor.fetchall()
    for k in result1:
        pl[k[1]] = k[0]  
    conn.close

    if request.method == 'POST':
        if (request.form.get('calltaxi')):
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            fields = []
            fields1 = []
            if request.form.get('Client_Last_Name'):
                Client_Last_Name1 = request.form.get('Client_Last_Name')
                Client_Last_Name = '\''+str(Client_Last_Name1)+'\''
            if request.form.get('Client_Name'):
                Client_Name1 = request.form.get('Client_Name')
                Client_Name = '\''+str(Client_Name1)+'\''
            if request.form.get('Client_Phone'):
                Client_Phone1 = request.form.get('Client_Phone')
                Client_Phone = '\''+str(Client_Phone1)+'\''

            parms = [Client_Name1, Client_Last_Name1, Client_Phone1]
            mycursor.callproc('CheckClient', parms)
            #mycursor.execute('EXECUTE CheckClient(' + Client_Name + ', ' + Client_Last_Name + ', ' + Client_Phone + ')')
            mycursor.execute('SELECT clientid FROM CLIENTS WHERE Name = ' + Client_Name + ' AND Last_Name=' + Client_Last_Name + ' AND Phone = '+ Client_Phone)
            temp = mycursor.fetchall()
            fk_client = str(temp[0][0])
            fields.append(fk_client)
            fields1.append('fk_client')

            if request.form.get('plan'):
                plan = request.form.get('plan')
                fk_plan = str(pl[plan])
                fields.append(fk_plan)
                fields1.append('fk_plan')
            
            if request.form.get('gofrom'):
                Departue = request.form.get('gofrom')
                Departue = '\''+str(Departue)+'\''
                fields.append(Departue)
                fields1.append('Av_Departue')
            if request.form.get('goto'):
                Destination = request.form.get('goto')
                Destination = '\''+str(Destination)+'\''
                fields.append(Destination)
                fields1.append('Av_Destination')
            # if request.form.get('rasst'):
            #     Distance = request.form.get('rasst')
            #     Distance = '\''+str(Distance)+'\''
            #     fields.append(Distance)
            #     fields1.append('Distance')

            if (request.form.get('Meeting')):
                fields.append('1')
                fields1.append("Meeting")
            else:
                fields.append('0')
                fields1.append("Meeting")
            if (request.form.get('Child_Chair')):
                fields.append('1')
                fields1.append("Child_Chair")
            else:
                fields.append('0')
                fields1.append("Child_Chair")
            if (request.form.get('Animal')):
                fields.append('1')
                fields1.append("Animal")
            else:
                fields.append('0')
                fields1.append("Animal")


            mystr = ''
            mystr1 = ''
            for elem in fields:
                mystr += elem + ', '
            mystr = mystr[:-1]
            mystr = mystr[:-1]

            for element in fields1:
                mystr1 += element + ', '
            mystr1 = mystr1[:-1]
            mystr1 = mystr1[:-1]


            mycursor.execute('INSERT INTO AVRIDE (AvID, ' + mystr1+ ') VALUES (AvrideID.NextVal, ' + mystr + ')')
            mycursor.execute('COMMIT')


            conn.close
            return render_template('callcenter.html', plans = pl, mes = 'Поездка создана')

        
    return render_template('callcenter.html', plans = pl)