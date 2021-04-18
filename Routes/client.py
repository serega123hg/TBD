from flask.blueprints import Blueprint
from flask import render_template
from flask import request
import cx_Oracle
import os  

crds = [] 
Name1 = ''
Last_Name1 = ''
result12 = ''
clid = ''
clients = []
plans = []


lib_dir= r"D:\\Documents\\sqldeveloper-19.2.1.247.2212-no-jre\\instantclient-basic-windows.x64-19.10.0.0.0dbru\\instantclient_19_10"
os.environ["PATH"] = lib_dir + ";" + os.environ["PATH"]
dsn = cx_Oracle.makedsn(host='localhost', port=1521, sid='xe')


client = Blueprint('client', __name__,
                template_folder='templates',
                static_folder='static')


@client.route('/client', methods=['POST', 'GET'])
def index5():
    global clients
    global clid 
    global Name1 
    global Last_Name1 
    global result12 
    global crds 
    global plans 
    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    mycursor = conn.cursor()
    if request.method == 'POST':
        if (request.form.get('Name')):
            fields = []
            fields1 = []
            if (request.form.get('Name')):
                Name1 = request.form.get('Name')
                Name = '\''+str(Name1)+'\''
            if (request.form.get('Last_Name')):
                Last_Name1 = request.form.get('Last_Name')
                Last_Name = '\''+str(Last_Name1)+'\''
            if (request.form.get('Phone')):
                Phone1 = request.form.get('Phone')
                Phone = '\''+str(Phone1)+'\''

            mycursor.execute('select * from CLIENTS WHERE Name = ' + Name + 'AND  Last_Name = ' + Last_Name + 'AND Phone='+ Phone)
            temp = mycursor.fetchall()[0]
            clid = temp[0]
            
            for zap in temp:
                clients.append(zap)
            mycursor.execute('select Card_Number from CARDS WHERE fk_client =' + str(clid))
            result = mycursor.fetchall()
            crds=[]
            for elem in result:
                crds.append(elem[0])
            flag = 1
            flag1 = 1
            mycursor.execute('select Rating from CLIENTS WHERE CLIENTID =' + str(clid))
            result12 = mycursor.fetchall()[0][0]
            if result12 == None:
                result12 = 'У вас ещё нет оценок'

            mycursor.execute('select Name from Plans')
            pl = mycursor.fetchall()
            for elem in pl:
                plans.append(elem[0])

            conn.close
        
            return render_template('client.html', cards=crds, flag = flag, Name = Name1, Last_Name = Last_Name1, Rating = result12, plans=plans)
        if (request.form.get('cardadd')):
            return render_template('client.html', flag2=1,  cards=crds, flag = 1, Name = Name1, Last_Name = Last_Name1, Rating = result12, plans=plans)
        if (request.form.get('cardadd1')):
            fields = []
            fields1 = []
            if (request.form.get('Card_Number')):
                Card_Number = request.form.get('Card_Number')
                fields.append('\''+str(Card_Number)+'\'')
                fields1.append("Card_Number")
            fields.append(str(clid))
            fields1.append("fk_client")
            if (request.form.get('Year')):
                Year = request.form.get('Year')
                fields.append(str(Year))
                fields1.append("Year")
            if (request.form.get('Month')):
                Month = request.form.get('Month')
                fields.append(str(Month))
                fields1.append("Month")
            if (request.form.get('SK')):
                SK = request.form.get('SK')
                fields.append(str(SK))
                fields1.append("CVC")

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


            mycursor.execute('INSERT INTO CARDS (CardID, ' + mystr1+ ') VALUES (CardID.NextVal, ' + mystr + ')')
            mycursor.execute('COMMIT')
            

            mycursor.execute('select Card_Number from CARDS WHERE fk_client =' + str(clid))
            result = mycursor.fetchall()
            crds=[]
            for elem in result:
                crds.append(elem[0])
            flag = 1
            flag1 = 1

            conn.close
            return render_template('client.html', cards=crds, flag = 1, Name = Name1, Last_Name = Last_Name1, Rating = result12, plans=plans)
            #return render_template('client.html', message='INSERT INTO CARDS (CardID, ' + mystr1+ ') VALUES (CardID.NextVal, ' + mystr + ')')
        if (request.form.get('carddel')):
            if (request.form.get('cardchange')):
                cardchange = request.form.get('cardchange')
                cardchange = '\''+str(cardchange)+'\''
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute("DELETE FROM CARDS WHERE Card_NUMBER = " + cardchange + 'AND fk_client = '+ str(clid))
            mycursor.execute('COMMIT')
            mycursor.execute('select Card_Number from CARDS WHERE fk_client =' + str(clid))
            result = mycursor.fetchall()
            crds=[]
            for elem in result:
                crds.append(elem[0])
            flag = 1
            flag1 = 1

            conn.close
            return render_template('client.html', cards=crds, flag = 1, Name = Name1, Last_Name = Last_Name1, Rating = result12, plans=plans)
        if (request.form.get('showride')):
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute("SELECT RIDE.Ride_Time, RIDE.Departue, RIDE.Destination, RIDE.Total, DRIVERS.FIO, DRIVERS.PHONE FROM RIDE JOIN DRIVERS ON RIDE.fk_driver = Drivers.driverid WHERE RIDE.fk_client =" + str(clid) + "ORDER BY RIDE.RIDE_TIME DESC")
            ride = mycursor.fetchall()
            flag = 1

            conn.close
            return render_template('client.html', cards=crds, flag = 1, Name = Name1, Last_Name = Last_Name1, Rating = result12, ride=ride, showr = 1, plans=plans)
        if (request.form.get('calltaxi')):
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            fields = []
            fields1 = []
            if (request.form.get('Plan')):
                Plan = request.form.get('Plan')
                Plan = '\''+str(Plan)+'\''
                mycursor.execute('SELECT PlanID FROM PLANS WHERE Name='+ Plan)
                pln = mycursor.fetchall()
                pln = pln[0][0]
                fields.append(str(pln))
                fields1.append("fk_plan")
            fields.append(str(clid))
            fields1.append("fk_client")
            if (request.form.get('Av_Departue')):
                Av_Departue = request.form.get('Av_Departue')
                fields.append('\''+str(Av_Departue)+'\'')
                fields1.append("Av_Departue")
            if (request.form.get('Av_Destination')):
                Av_Destination = request.form.get('Av_Destination')
                fields.append('\''+str(Av_Destination)+'\'')
                fields1.append("Av_Destination")
            if (request.form.get('Promo')):
                Promo = request.form.get('Promo')
                Promo = '\''+str(Promo)+'\''
                try:
                    mycursor.execute('SELECT PromoID FROM PROMO WHERE Code='+ Promo)
                    prm = mycursor.fetchall()
                    prm = prm[0][0]
                    fields.append(str(prm))
                    fields1.append("fk_promo")
                except:
                    pass
                    
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
            return render_template('client.html', cards=crds, flag = 1, Name = Name1, Last_Name = Last_Name1, Rating = result12, plans=plans, mes = 'Такси заказано')
    return render_template('client.html', flag1 = 1)
    