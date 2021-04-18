from flask.blueprints import Blueprint
from flask import render_template
from flask import request
import cx_Oracle
import os  
import datetime 

FIO = ''
result12 = ''
drid = ''
TS_model = ''
TS_number = ''
tarif = ''
myplan = ''
drivers = []
tss = []
tekride = ''
takethis = ''

lib_dir= r"D:\\Documents\\sqldeveloper-19.2.1.247.2212-no-jre\\instantclient-basic-windows.x64-19.10.0.0.0dbru\\instantclient_19_10"
os.environ["PATH"] = lib_dir + ";" + os.environ["PATH"]
dsn = cx_Oracle.makedsn(host='localhost', port=1521, sid='xe')


driver = Blueprint('driver', __name__,
                template_folder='templates',
                static_folder='static')


@driver.route('/driver', methods=['POST', 'GET'])
def index5():
    global FIO
    global drid 
    global TS_model 
    global TS_number 
    global result12 
    global tarif 
    global drivers 
    global tss
    global myplan
    global tekride
    global takethis
    # conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    # mycursor = conn.cursor()
    if request.method == 'POST':
        
        if (request.form.get('Phone')):
            Phone = request.form.get('Phone')
            Phone = '\''+str(Phone)+'\''
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute('select * from DRIVERS WHERE Phone = ' + Phone)
            temp = mycursor.fetchall()
            temp = temp[0]
            drid = str(temp[0])
            FIO = temp[1]
            Rating = temp[9]
            result12 = temp[9]
            if result12 == None:
                result12 == 'У вас ещё нет оценок'

            for zap in temp:
                drivers.append(zap)
            tsid1 = str(drivers[5])

            mycursor.execute('select TSID, AUTO_NUMBER, fk_model from AUTOPARK WHERE TSID =' + str(tsid1))
            result = mycursor.fetchall()
            for zap in result:
                for elem in zap:
                    tss.append(elem)
            TS_number = tss[1]
            TS_id = tss[0]
            auto_id = tss[2]
            mycursor.execute('select * from AUTO WHERE AutoID = ' + str(auto_id))
            result = mycursor.fetchall()
            TS_model = result[0][1]
            mycursor.execute('select * from AUTOPLANS WHERE fk_plan = ' + str(auto_id))
            result111 = mycursor.fetchall()
            fk_plan = result111[0][1]
            myplan = fk_plan

            mycursor.execute('select Name from PLANS WHERE PlanID =' + str(fk_plan))
            result = mycursor.fetchall()
            tarif = result[0][0]


            avrides=[]
            mycursor.execute('select * from AVRIDE WHERE fk_plan =' + str(fk_plan))
            result = mycursor.fetchall()
            stroka = ''
            for elem in result:
                stroka =  str(elem[0]) + ' От ' + str(elem[4]) + ' До ' + str(elem[5])
                if elem[7] == '1':
                    stroka += ' Перевозка животных'
                if elem[8] == '1':
                    stroka += ' Детское кресло'
                if elem[9] == '1':
                    stroka += ' Встреча с табличкой'
                avrides.append(stroka)

            conn.close
            return render_template('driver.html', cantake=1, tarif = tarif, FIO = FIO, flag = 1, TS_number = TS_number, TS_model = TS_model, Rating = result12, avrides=avrides)

        if (request.form.get('takeit')):
            if (request.form.get('takethis')):
                conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
                mycursor = conn.cursor()
                takethis1 = request.form.get('takethis')
                takethis = takethis1.split()[0]
                mycursor.execute('select * from AVRIDE WHERE AVID =' + str(takethis))
                result = mycursor.fetchall()
                thisride = result[0]
                fk_client = str(thisride[1])
                fk_plan = str(thisride[2])
                if thisride[3] != None:
                    fk_promo = str(thisride[3])
                else:
                    fk_promo = 'NULL'
                dep = '\'' + str(thisride[4]) + '\''
                des = '\'' +str(thisride[5]) + '\''
                #dis = thisride[6]
                an = str(thisride[7])
                ch = str(thisride[8])
                me = str(thisride[9])
                mycursor.execute('select Name, Phone from Clients WHERE ClientID =' + str(fk_client))
                result = mycursor.fetchall()
                result = result[0]
                clphone = '\'' + str(result[1]) + '\''
                clname = '\'' + str(result[0]) + '\''

                # new_rez = []
                # last_idx = -1
                # for i in mycursor.fetchall():
                #     new_rez.append(int(i[0]))
                #     if int(i[0]) > last_idx:
                #         last_idx = int(i[0])
                # last_idx += 1

                now = datetime.datetime.now() 
                mycursor.execute('INSERT INTO RIDE (RideID, fk_client, fk_driver, fk_promo, phone, Ride_Time, departue, destination, animal, child_chair, meeting, fk_plan, finished) VALUES (RideID.NextVal, ' + fk_client + ', ' + str(drid) + ', ' + fk_promo + ', ' + clphone + ', ' + 'TO_DATE(\'' + str(now.strftime('%Y-%m-%d %H:%M:%S')) +'\', \'YYYY-MM-DD HH24:MI:SS\'), ' + dep + ', ' + des + ', ' + an + ', ' + ch + ', ' + me + ', ' + fk_plan + ', 0)')
                #mycursor.execute('INSERT INTO RIDE (RideID, fk_client, fk_driver, fk_promo, phone, Ride_Time, departue, destination, animal, child_chair, meeting, fk_plan, finished) VALUES (RideID.NextVal, ' + fk_client + ', ' + str(drid) + ', ' + fk_promo + ', ' + clphone + ', ' + 'TO_DATE(\'' + str(now.strftime('%Y-%m-%d %H:%M:%S')) +'\', \'YYYY-MM-DD HH24:MI:SS\'), ' + dep + ', ' + des + ', ' + an + ', ' + ch + ', ' + me + ')')
                mycursor.execute('SELECT RIDEID FROM RIDE')
                mxidx = -1
                tmprez = mycursor.fetchall()
                for elem in tmprez:
                    if int(elem[0]) > mxidx:
                        mxidx = int(elem[0])
                tekride = mxidx
                mycursor.execute('COMMIT') 
                conn.close
                return render_template('driver.html',vezufrom = dep, vezuto=des, vezukogo = clname, vezukogophone = clphone, tarif = tarif, FIO = FIO, flag = 1, TS_number = TS_number, TS_model = TS_model, Rating = result12, vezu=1)
                #return render_template('driver.html',vezufrom = dep, vezuto=des, vezukogo = clname, vezukogophone = clphone, tarif = tarif, FIO = FIO, flag = 1, TS_number = TS_number, TS_model = TS_model, Rating = result12, vezu=1, message='INSERT INTO RIDE (RideID, fk_client, fk_driver, fk_promo, phone, Ride_Time, departue, destination, animal, child_chair, meeting, fk_plan, finished) VALUES (RideID.NextVal, ' + fk_client + ', ' + str(drid) + ', ' + fk_promo + ', ' + clphone + ', ' + 'TO_DATE(\'' + str(now.strftime('%Y-%m-%d %H:%M:%S')) +'\', \'YYYY-MM-DD HH24:MI:SS\'), ' + dep + ', ' + des + ', ' + an + ', ' + ch + ', ' + me + ', ' + fk_plan + ', 0)')

            #return render_template('client.html', message='INSERT INTO CARDS (CardID, ' + mystr1+ ') VALUES (CardID.NextVal, ' + mystr + ')')
        if (request.form.get('Distance')):
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            if (request.form.get('Distance')):
                Distance = request.form.get('Distance')
                Distance = str(Distance)
            
            if (request.form.get('Total')):
                Total = request.form.get('Total')
                Total = str(Total)

            mycursor.execute('UPDATE RIDE SET Distance = '+ Distance + ', Total = '+ Total + ', Finished=1 WHERE RideID = '+ str(tekride) )

            mycursor.execute('Delete from AVRIDE WHERE AVID =' + str(takethis))
            mycursor.execute('COMMIT')
            avrides=[]
            mycursor.execute('select * from AVRIDE WHERE fk_plan =' + str(myplan))
            result = mycursor.fetchall()
            stroka = ''
            for elem in result:
                stroka =  str(elem[0]) + ' От ' + str(elem[4]) + ' До ' + str(elem[5])
                if elem[7] == '1':
                    stroka += ' Перевозка животных'
                if elem[8] == '1':
                    stroka += ' Детское кресло'
                if elem[9] == '1':
                    stroka += ' Встреча с табличкой'
                avrides.append(stroka)

            conn.close
            return render_template('driver.html', cantake = 1, tarif = tarif,  FIO = FIO, flag = 1, TS_number = TS_number, TS_model = TS_model, Rating = result12, avrides=avrides)
        if (request.form.get('showride')):
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute("SELECT RIDE.Ride_Time, RIDE.Departue, RIDE.Destination, RIDE.Total, RIDE.PHONE FROM RIDE WHERE RIDE.fk_driver =" + str(drid) + " ORDER BY RIDE.RIDE_TIME DESC")
            ride = mycursor.fetchall()
            flag = 1
            avrides=[]
            mycursor.execute('select * from AVRIDE WHERE fk_plan =' + str(myplan))
            result = mycursor.fetchall()
            stroka = ''
            for elem in result:
                stroka =  str(elem[0]) + ' От ' + str(elem[4]) + ' До ' + str(elem[5])
                if elem[7] == '1':
                    stroka += ' Перевозка животных'
                if elem[8] == '1':
                    stroka += ' Детское кресло'
                if elem[9] == '1':
                    stroka += ' Встреча с табличкой'
                avrides.append(stroka)
            conn.close
            
            return render_template('driver.html',cantake=1, tarif = tarif,  FIO = FIO, flag = 1, TS_number = TS_number, TS_model = TS_model, Rating = result12, avrides=avrides, ride=ride, showr = 1)
            #return render_template('driver.html',cantake=1, tarif = tarif,  FIO = FIO, flag = 1, TS_number = TS_number, TS_model = TS_model, Rating = result12,  message = "SELECT RIDE.Ride_Time, RIDE.Departue, RIDE.Destination, RIDE.Total, RIDE.PHONE FROM RIDE WHERE RIDE.fk_driver =" + str(drid) + " ORDER BY RIDE.RIDE_TIME DESC")
        #conn.close
    return render_template('driver.html', flag1 = 1)