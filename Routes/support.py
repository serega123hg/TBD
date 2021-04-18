from flask.blueprints import Blueprint
from flask import render_template
from flask import request
import cx_Oracle
import os  


wd1 = {}

lib_dir= r"D:\\Documents\\sqldeveloper-19.2.1.247.2212-no-jre\\instantclient-basic-windows.x64-19.10.0.0.0dbru\\instantclient_19_10"
os.environ["PATH"] = lib_dir + ";" + os.environ["PATH"]
dsn = cx_Oracle.makedsn(host='localhost', port=1521, sid='xe')


support = Blueprint('support', __name__,
                template_folder='templates',
                static_folder='static')


@support.route('/support')
def index4():
    
    return render_template('support.html')




@support.route('/support/all')
def idx1():
    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    mycursor = conn.cursor()

    mycursor.execute('select * from APPL ORDER BY Ride_Time')
    result = mycursor.fetchall()


    conn.close

    return render_template('support.html', rezall=result)


@support.route('/support/inwork', methods=['POST', 'GET'])
def idx2():
    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    mycursor = conn.cursor()
    mycursor.execute('select * from APPLINWORK ORDER BY Ride_Time')
    result = mycursor.fetchall()

    conn.close

    if request.method == 'POST':
        if (request.form.get('applid')):
            applid = request.form.get('applid')
        conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
        mycursor = conn.cursor()
        mycursor.execute('UPDATE APPLICATIONS SET Closed = 1 WHERE ApplID = ' + str(applid))
        mycursor.execute('COMMIT')
        mycursor.execute('select * from APPLINWORK ORDER BY Ride_Time')
        result = mycursor.fetchall()
        conn.close
        return render_template('support.html', rezinwork=result)

    return render_template('support.html', rezinwork=result)


@support.route('/support/create', methods=['POST', 'GET'])
def idx3():
    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    mycursor = conn.cursor()
    mycursor.execute('select WORKERS.FIO, WORKERS.WorkerID from WORKERS JOIN POSITIONS ON WORKERS.fk_pos = POSITIONS.PosID WHERE POSITIONS.Pos_Name = \'Support\'')
    workers = mycursor.fetchall()
    wrkrs = []
    for elem in workers:
        wd1[elem[0]] = elem[1]
        wrkrs.append(elem[0])

    conn.close

    if request.method == 'POST':
        if request.form.get('fk_worker'):
            fields = []
            fields1 = []
            if request.form.get('fk_worker'):
                fk_worker = request.form.get('fk_worker')
                fk_worker = str(wd1[fk_worker])
                fields.append(fk_worker)
                fields1.append('fk_worker')

            if request.form.get('Client_Name'):
                Name = request.form.get('Client_Name')
                Name = '\''+str(Name)+'\''
            
            if request.form.get('Client_Last_Name'):
                Last_Name = request.form.get('Client_Last_Name')
                Last_Name = '\''+str(Last_Name)+'\''

            if request.form.get('Client_Phone'):
                Phone = request.form.get('Client_Phone')
                Phone = '\''+str(Phone)+'\''


            if request.form.get('Ride_time'):
                Ride_Date = request.form.get('Ride_time')
                #Ride_Date = '\''+str(Ride_Date)+'\''
            
            if request.form.get('Ride_time1'):
                Ride_time = request.form.get('Ride_time1')
                #Ride_time = '\''+str(Ride_time)+'\''

            td =  'TO_DATE(\''+str(Ride_Date) + ' ' + str(Ride_time) + ':00\', \'YYYY-MM-DD HH24:MI:SS\')'


            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute('select CLIENTS.ClientID from CLIENTS where Name = '+ str(Name) + ' AND Last_Name = ' +str(Last_Name)  + ' AND Phone = ' + str(Phone))
            rz = mycursor.fetchall()
            cl = str(rz[0][0])
            fields.append(str(rz[0][0]))
            fields1.append('fk_client')

            mycursor.execute('select RideID, (('+ td +' - Ride_time) * 24 * 60) from RIDE where fk_client = '+ cl)
            #mycursor.execute('select RideID, min(ABS('+ td +' - Ride_time) * 24 * 60) from RIDE where fk_client = '+ cl + ' GROUP BY RideID')
            rz = mycursor.fetchall()
            tmpid = []
            tmprazn = []
            for elem in rz:
                tmpid.append(elem[0])
                tmprazn.append(elem[1])

            fk_ride = str(tmpid[tmprazn.index(min(tmprazn))])

            fields.append(fk_ride)
            fields1.append('fk_ride')
            #fk_ride = str(rz[0][0])

            if request.form.get('Description'):
                Description = request.form.get('Description')
                fields.append('\''+str(Description)+'\'')
                fields1.append('Description')
            
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

            #conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            #mycursor = conn.cursor()

            mycursor.execute('INSERT INTO APPLICATIONS (ApplID, ' + mystr1 + ', Closed) VALUES (ApplID.NextVal, ' + mystr + ', 0)')
            mycursor.execute('COMMIT')
            mycursor.execute('select WORKERS.FIO, POSITIONS.PosID from WORKERS JOIN POSITIONS ON WORKERS.fk_pos = POSITIONS.PosID WHERE POSITIONS.Pos_Name = \'Support\'')
            workers = mycursor.fetchall()
            wrkrs = []
            for elem in workers:
                wd1[elem[0]] = elem[1]
                wrkrs.append(elem[0])
            conn.close
            return render_template('support.html', message1 = 'Запись добавлена', workers = wrkrs, rezcreate=1)

    return render_template('support.html', workers = wrkrs, rezcreate=1)

