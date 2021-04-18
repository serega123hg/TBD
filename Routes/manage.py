from flask.blueprints import Blueprint
from flask import render_template
from flask import request
import cx_Oracle
import os  

cur_plan = ''
cur_auto = ''
cur_promo = ''
cur_work = ''
cur_pos = ''
pl = {}
wd = {}

lib_dir= r"D:\\Documents\\sqldeveloper-19.2.1.247.2212-no-jre\\instantclient-basic-windows.x64-19.10.0.0.0dbru\\instantclient_19_10"
os.environ["PATH"] = lib_dir + ";" + os.environ["PATH"]
dsn = cx_Oracle.makedsn(host='localhost', port=1521, sid='xe')


manage = Blueprint('manage', __name__,
                template_folder='templates',
                static_folder='static')


@manage.route('/manage')
def index3():
    
    return render_template('manage.html')




@manage.route('/manage/plan')
def idx4():
    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    mycursor = conn.cursor()
    mycursor.execute('select * from plans')
    result = mycursor.fetchall()

    conn.close

    return render_template('manage.html', rezplan=result)

@manage.route('/manage/plan/change', methods=['POST', 'GET'])
def idx9():
    global cur_plan
    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    mycursor = conn.cursor()
    mycursor.execute('select * from plans')
    result = mycursor.fetchall()
    plans = []
    for zap in result:
        plans.append(zap[1])

    conn.close

    if request.method == 'POST':
        # выводим данные о выбранном тарифе для его изменения
        if (request.form.get('cur_plan')):
            cur_plan = request.form.get('cur_plan')
            for zap in result:
                if zap[1] == cur_plan:
                    serv = zap
                    break
            flag = 1
            return render_template('changePlans.html', plans=plans, serv = serv, flag = flag, pln = cur_plan)
        # Удаляем выбранный тариф
        elif request.form.get('del_plan'):
            del_plan = request.form.get('del_plan')
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute("DELETE FROM PLANS WHERE Name = " + "'"+ del_plan + "'")
            mycursor.execute('COMMIT')
            mycursor.execute('select * from plans')
            result = mycursor.fetchall()
            plans = []
            for zap in result:
                plans.append(zap[1])
            conn.close

            return render_template('changePlans.html', message = "Тариф успешно удален из базы данных", plans=plans)
        # Обрабатываем запрос на редактирование тарифа
        elif request.form.get('plan_name1'):
            #flag = 2
            fields = []
            fields1 = []
            if request.form.get('plan_name1'):
                plan_name1 = request.form.get('plan_name1')
                fields.append('\''+str(plan_name1)+'\'')
                fields1.append("Name")

            if request.form.get('Min_Price1'):
                Min_Price1 = request.form.get('Min_Price1')
                fields.append(Min_Price1)
                fields1.append("Min_Price")

            if request.form.get('Free_Waiting1'):
                Free_Waiting1 = request.form.get('Free_Waiting1')
                fields.append(Free_Waiting1)
                fields1.append("Free_Waiting")

            if request.form.get('Fee_Waiting1'):
                Fee_Waiting1 = request.form.get('Fee_Waiting1')
                fields.append(Fee_Waiting1)
                fields1.append("Fee_Waiting")

            if request.form.get('Taxometer1'):
                Taxometer1 = request.form.get('Taxometer1')
                fields.append(Taxometer1)
                fields1.append("Taxometer")

            if request.form.get('Meeting1'):
                Meeting1 = request.form.get('Meeting1')
                fields.append(Meeting1)
                fields1.append("Meeting")

            if request.form.get('Animal1'):
                Animal1 = request.form.get('Animal1')
                fields.append(Animal1)
                fields1.append("Animal")

            if request.form.get('Child_Chair1'):
                Child_Chair1 = request.form.get('Child_Chair1')
                fields.append(Child_Chair1)
                fields1.append("Child_Chair")

            if request.form.get('Seats1'):
                Seats1 = request.form.get('Seats1')
                fields.append(Seats1)
                fields1.append('Seats')

            if request.form.get('Luggage1'):
                Luggage1 = request.form.get('Luggage1')
                fields.append(Luggage1)
                fields1.append('Luggage')

            if request.form.get('ToDoor1'):
                ToDoor1 = request.form.get('ToDoor1')
                fields.append(ToDoor1)
                fields1.append('ToDoor')

            if request.form.get('Wait_Reciever1'):
                Wait_Reciever1 = request.form.get('Wait_Reciever1')
                fields.append(Wait_Reciever1)
                fields1.append('Wait_Reciever')

            if request.form.get('Transfer_To1'):
                Transfer_To1 = request.form.get('Transfer_To1')
                fields.append(Transfer_To1)
                fields1.append('Transfer_To')

            if request.form.get('Transfer_From1'):
                Transfer_From1 = request.form.get('Transfer_From1')
                fields.append(Transfer_From1)
                fields1.append('Transfer_From')
            
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

            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute('SELECT PlanID FROM PLANS')


            new_rez = []
            last_idx = -1
            for i in mycursor.fetchall():
                new_rez.append(int(i[0]))
                if int(i[0]) > last_idx:
                    last_idx = int(i[0])
            last_idx += 1

            mycursor.execute('INSERT INTO PLANS (PlanID, ' + mystr1 + ') VALUES (PlanID.NextVal, ' + mystr + ')')
            mycursor.execute('COMMIT')

            mycursor.execute('select * from plans')
            result = mycursor.fetchall()
            plans = []
            for zap in result:
                plans.append(zap[1])
            conn.close
            return render_template('changePlans.html', message = "Тариф успешно добавлен в базу данных", plans=plans)

        else:
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute('select * from plans')
            result = mycursor.fetchall()

            for zap in result:
                if zap[1] == cur_plan:
                    serv = zap

            if request.form.get('plan_name'):
                plan_name = request.form.get('plan_name')
                if serv[1] != plan_name:
                    mycursor.execute('UPDATE PLANS SET Name = ' + '\''+str(plan_name)+'\'' + 'WHERE PlanId = '+ str(serv[0])) 
               

            if request.form.get('Min_Price'):
                Min_Price = request.form.get('Min_Price')
                if Min_Price == "None" and serv[2] != None:
                    mycursor.execute('UPDATE PLANS SET Min_Price = NULL WHERE PlanId = ' + str(serv[0])) 
                elif Min_Price != "None" and serv[2] != Min_Price:
                    mycursor.execute('UPDATE PLANS SET Min_Price = ' +str(Min_Price)+ 'WHERE PlanId = '+ str(serv[0])) 
  

            if request.form.get('Free_Waiting'):
                Free_Waiting = request.form.get('Free_Waiting')
                if Free_Waiting == "None" and serv[3] != None:
                    mycursor.execute('UPDATE PLANS SET Free_Waiting = NULL WHERE PlanId = ' + str(serv[0])) 
                elif Free_Waiting != "None" and serv[3] != Free_Waiting:
                    mycursor.execute('UPDATE PLANS SET Free_Waiting = '+str(Free_Waiting) + 'WHERE PlanId = '+ str(serv[0])) 
 

            if request.form.get('Fee_Waiting'):
                Fee_Waiting = request.form.get('Fee_Waiting')
                if Fee_Waiting == "None" and serv[4] != None:
                    mycursor.execute('UPDATE PLANS SET Fee_Waiting = NULL WHERE PlanId = ' + str(serv[0])) 
                elif Fee_Waiting != "None" and serv[4] != Fee_Waiting:
                    mycursor.execute('UPDATE PLANS SET Fee_Waiting = ' +str(Fee_Waiting)+'WHERE PlanId = '+ str(serv[0])) 
 

            if request.form.get('Taxometer'):
                Taxometer = request.form.get('Taxometer')
                if Taxometer == "None" and serv[5] != None:
                    mycursor.execute('UPDATE PLANS SET Taxometer = NULL WHERE PlanId = ' + str(serv[0])) 
                elif Taxometer != "None" and serv[5] != Taxometer:
                    mycursor.execute('UPDATE PLANS SET Taxometer = ' + str(Taxometer)+ 'WHERE PlanId = '+ str(serv[0])) 


            if request.form.get('Meeting'):
                Meeting = request.form.get('Meeting')
                if Meeting == "None" and serv[6] != None:
                    mycursor.execute('UPDATE PLANS SET Meeting = NULL WHERE PlanId = ' + str(serv[0])) 
                elif Meeting != "None" and serv[6] != Meeting:
                    mycursor.execute('UPDATE PLANS SET Meeting = '+str(Meeting) + 'WHERE PlanId = '+ str(serv[0])) 
 

            if request.form.get('Animal'):
                Animal = request.form.get('Animal')
                if Animal == "None" and serv[7] != None:
                    mycursor.execute('UPDATE PLANS SET Animal = NULL WHERE PlanId = ' + str(serv[0])) 
                elif Animal != "None" and serv[7] != Animal:
                    mycursor.execute('UPDATE PLANS SET Animal = ' +str(Animal)+ 'WHERE PlanId = '+ str(serv[0])) 
  

            if request.form.get('Child_Chair'):
                Child_Chair = request.form.get('Child_Chair')
                if Child_Chair == "None" and serv[8] != None:
                    mycursor.execute('UPDATE PLANS SET Child_Chair = NULL WHERE PlanId = ' + str(serv[0])) 
                elif Child_Chair != "None" and serv[8] != Child_Chair:
                    mycursor.execute('UPDATE PLANS SET Child_Chair = '+str(Child_Chair) + 'WHERE PlanId = '+ str(serv[0])) 


            if request.form.get('Seats'):
                Seats = request.form.get('Seats')
                if Seats == "None" and serv[9] != None:
                    mycursor.execute('UPDATE PLANS SET Seats = NULL WHERE PlanId = ' + str(serv[0])) 
                elif Seats != "None" and serv[9] != Seats:
                    mycursor.execute('UPDATE PLANS SET Seats = ' + str(Seats)+ 'WHERE PlanId = '+ str(serv[0])) 


            if request.form.get('Luggage'):
                Luggage = request.form.get('Luggage')
                if Luggage == "None" and serv[10] != None:
                    mycursor.execute('UPDATE PLANS SET Luggage = NULL WHERE PlanId = ' + str(serv[0]))
                elif Luggage != "None" and serv[10] != Luggage:
                    mycursor.execute('UPDATE PLANS SET Luggage = ' +str(Luggage)+ 'WHERE PlanId = ' + str(serv[0])) 
  

            if request.form.get('ToDoor'):
                ToDoor = request.form.get('ToDoor')
                if ToDoor == "None" and serv[11] != None:
                    mycursor.execute('UPDATE PLANS SET ToDoor=' +ToDoor+ 'WHERE PlanId IN (SELECT PlanID FROM PLANS WHERE PlanID =' + str(serv[0]) + ')') 
                elif ToDoor != "None" and serv[11] != ToDoor:
                    mycursor.execute('UPDATE PLANS SET ToDoor=' +ToDoor+ 'WHERE PlanId IN (SELECT PlanID FROM PLANS WHERE PlanID =' + str(serv[0]) + ')') 

            if request.form.get('Wait_Reciever'):
                Wait_Reciever = request.form.get('Wait_Reciever')
                if Wait_Reciever == "None" and serv[12] != None:
                    mycursor.execute('UPDATE PLANS SET Wait_Reciever = NULL WHERE PlanId = ' + str(serv[0]))
                elif Wait_Reciever != "None" and serv[12] != Wait_Reciever:
                    mycursor.execute('UPDATE PLANS SET Wait_Reciever = ' +str(Wait_Reciever)+ 'WHERE PlanId = ' + str(serv[0])) 


            if request.form.get('Transfer_To'):
                Transfer_To = request.form.get('Transfer_To')
                if Transfer_To == "None" and serv[13] != None:
                    mycursor.execute('UPDATE PLANS SET Transfer_To = NULL WHERE PlanId = ' + str(serv[0]))
                elif Transfer_To != "None" and serv[13] != Transfer_To:
                    mycursor.execute('UPDATE PLANS SET Transfer_To = ' + str(Transfer_To) + 'WHERE PlanId = ' + str(serv[0])) 
 

            if request.form.get('Transfer_From'):
                Transfer_From = request.form.get('Transfer_From')
                if Transfer_From == "None" and serv[14] != None:
                    mycursor.execute('UPDATE PLANS SET Transfer_From = NULL WHERE PlanId = ' + str(serv[0])) 
                elif Transfer_From != "None" and serv[14] != Transfer_From:
                    mycursor.execute('UPDATE PLANS SET Transfer_From = ' + str(Transfer_From) + 'WHERE PlanId = ' + str(serv[0])) 

            
            mycursor.execute('COMMIT')   

            mycursor.execute('select * from plans')
            result = mycursor.fetchall()
            plans = []
            for zap in result:
                plans.append(zap[1])
            conn.close
            return render_template('changePlans.html', message = "Тариф обновлен", plans=plans)

    return render_template('changePlans.html', plans=plans)





@manage.route('/manage/auto')
def idx5():
    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    mycursor = conn.cursor()
    mycursor.execute('SELECT AUTO.AutoID, AUTO.Model, AUTOPLANS.fk_plan FROM AUTO JOIN AUTOPLANS ON AUTOPLANS.fk_auto = AUTO.AutoID ORDER BY AUTOPLANS.fk_plan')
    temp = mycursor.fetchall()
    mycursor.execute('select PlanID, Name from Plans')
    result1 = mycursor.fetchall()
    tmp = []
    result = []
    global pl
    for k in result1:
        pl[k[1]] = k[0]  

    for elem in temp:
        for i in elem:
            tmp.append(i)
        result.append(tmp)
        tmp = []

    for elem in result:
        for elem1 in result1:
            if elem[2] == elem1[0]:
                elem[2] = elem1[1]

    conn.close

    return render_template('manage.html', rezauto=result, plans = pl)

@manage.route('/manage/auto/change', methods=['POST', 'GET'])
def idx10():
    global cur_auto
    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    mycursor = conn.cursor()
    mycursor.execute('select * from auto')
    result = mycursor.fetchall()
    auto = []
    for zap in result:
        auto.append(zap[1])

    mycursor.execute('select PlanID, Name from Plans')
    result1 = mycursor.fetchall()
    for k in result1:
        pl[k[1]] = k[0] 
    conn.close

    if request.method == 'POST':
        # выводим данные о выбранной модели для её изменения
        if (request.form.get('cur_auto')):
            cur_auto = request.form.get('cur_auto')
            
            for zap in result:
                if zap[1] == cur_auto:
                    serv = zap
                    break
            flag = 1
            return render_template('changeAuto.html', auto=auto, serv = serv, flag = flag, aut = cur_auto, plans = pl)
        # Удаляем выбранную модель
        elif request.form.get('del_auto'):
            del_auto = request.form.get('del_auto')
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute("DELETE FROM AUTO WHERE Model = " + "'"+ del_auto + "'")
            mycursor.execute('COMMIT')


            mycursor.execute('select * from auto')
            result = mycursor.fetchall()
            auto = []
            for zap in result:
                auto.append(zap[1])

            conn.close

            return render_template('changeAuto.html', message = "Модель успешно удалена из базы данных",  auto=auto , plans = pl)
        # Обрабатываем запрос на добавление модели
        elif request.form.get('model1'):
            #fields = []
            #fields1 = []
            if request.form.get('model1'):
                model1 = request.form.get('model1')
                #fields.append('\''+str(model1)+'\'')
                #fields1.append("Model")
                modelka = '\''+str(model1)+'\''

            if request.form.get('fk_plan1'):

                fk_plan1 = request.form.get('fk_plan1')
                fk_plan1 = str(pl[fk_plan1])
                #fields.append(fk_plan1)
                #fields1.append('fk_plan')
            
            # mystr = ''
            # mystr1 = ''
            # for elem in fields:
            #     mystr += elem + ', '
            # mystr = mystr[:-1]
            # mystr = mystr[:-1]

            # for element in fields1:
            #     mystr1 += element + ', '
            # mystr1 = mystr1[:-1]
            # mystr1 = mystr1[:-1]

            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()


            mycursor.execute('INSERT INTO AUTO (AUTOID, MODEL) VALUES (AutoID.NextVal, ' + modelka + ')')
            mycursor.execute('select * from auto')
            result = mycursor.fetchall()
            ids = []
            for zap in result:
                ids.append(zap[0])
            curids = max(ids)
            mycursor.execute('INSERT INTO AUTOPLANS (fk_auto, fk_plan) VALUES (' + str(curids) + ', ' + fk_plan1 + ')')
            mycursor.execute('COMMIT')

            mycursor.execute('select * from auto')
            result = mycursor.fetchall()
            auto = []
            for zap in result:
                auto.append(zap[1])
            conn.close
            return render_template('changeAuto.html', message = "Модель успешно добавлена в базу данных", auto=auto , plans = pl)
        # тут уже изменение данных
        else:
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute('select * from auto')
            result = mycursor.fetchall()

            for zap in result:
                if zap[1] == cur_auto:
                    serv = zap

            if request.form.get('model'):
                model = request.form.get('model')
                if serv[1] != model:
                    mycursor.execute('UPDATE AUTO SET Model = ' + '\''+str(model)+'\'' + 'WHERE AutoId = '+ str(serv[0])) 
               

            if request.form.get('fk_plan'):
                fk_plan = request.form.get('fk_plan')
                fk_plan = pl[fk_plan]
                #if serv[2] != fk_plan:
                mycursor.execute('SELECT * FROM AUTOPLANS WHERE fk_auto = '+ str(serv[0])) 
                result2121 = mycursor.fetchall()
                plan_fk = result2121[0][1]
                mycursor.execute('UPDATE AUTOPLANS SET fk_plan = ' +str(fk_plan)+ 'WHERE fk_auto = '+ str(serv[0]) + ' AND fk_plan = ' +str(plan_fk)) 
            
            mycursor.execute('COMMIT')   

            mycursor.execute('select * from auto')
            result = mycursor.fetchall()
            auto = []
            for zap in result:
                auto.append(zap[1])
            conn.close
            return render_template('changeAuto.html', message = "Данные о модели обновлены", auto=auto, plans = pl)

    return render_template('changeAuto.html', auto=auto, plans = pl)





@manage.route('/manage/promo')
def idx6():
    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    mycursor = conn.cursor()
    mycursor.execute('select * from PROMO')
    result = mycursor.fetchall()
    #global pl

    conn.close

    return render_template('manage.html', rezpromo=result)

@manage.route('/manage/promo/change', methods=['POST', 'GET'])
def idx11():
    global cur_promo
    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    mycursor = conn.cursor()
    mycursor.execute('select * from promo')
    result = mycursor.fetchall()
    promo = []
    for zap in result:
        promo.append(zap[1])

    conn.close

    if request.method == 'POST':
        # выводим данные о выбранном промокоде для его изменения
        if (request.form.get('cur_promo')):
            cur_promo = request.form.get('cur_promo')
            
            for zap in result:
                if zap[1] == cur_promo:
                    serv = zap
                    break
            flag = 1
            return render_template('changePromo.html', promo=promo, serv = serv, flag = flag, prm = cur_promo)
        # Удаляем выбранную модель
        elif request.form.get('del_promo'):
            del_promo = request.form.get('del_promo')
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute("DELETE FROM PROMO WHERE Code = " + "'"+ del_promo + "'")
            mycursor.execute('COMMIT')


            mycursor.execute('select * from promo')
            result = mycursor.fetchall()
            promo = []
            for zap in result:
                promo.append(zap[1])
            conn.close

            return render_template('changePromo.html', message = "Промокод успешно удален из базы данных",  promo=promo)
        # Обрабатываем запрос на добавление промокода
        elif request.form.get('Code1'):
            fields = []
            fields1 = []
            if request.form.get('Code1'):
                code1 = request.form.get('Code1')
                fields.append('\''+str(code1)+'\'')
                fields1.append("Code")

            if request.form.get('Discount1'):

                Discount1 = request.form.get('Discount1')
                fields.append(Discount1)
                fields1.append('Discount')
            
            if request.form.get('Amount1'):

                Amount1 = request.form.get('Amount1')
                fields.append(Amount1)
                fields1.append('Amount')

            if request.form.get('valid_until11'):

                valid_until1 = request.form.get('valid_until1').replace('-', '/')
                valid_until2 = 'TO_DATE(\'' + valid_until1 + '\' ,' + '\'YYYY/MM/DD\')'
                fields.append(valid_until2)
                fields1.append('valid_until')

            
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

            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()

            mycursor.execute('INSERT INTO PROMO (PromoID, ' + mystr1 + ') VALUES (PromoID.NextVal, ' + mystr + ')')
            mycursor.execute('COMMIT')

            mycursor.execute('select * from promo')
            result = mycursor.fetchall()
            promo = []
            for zap in result:
                promo.append(zap[1])
            conn.close
            return render_template('changePromo.html', message = "Промокод успешно добавлен в базу данных", promo=promo)
        # тут уже изменение данных
        else:
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute('select * from promo')
            result = mycursor.fetchall()

            for zap in result:
                if zap[1] == cur_promo:
                    serv = zap

            if request.form.get('Code'):
                Code = request.form.get('Code')
                if serv[1] != Code:
                    mycursor.execute('UPDATE PROMO SET Code = ' + '\''+str(Code)+'\'' + 'WHERE PromoId = '+ str(serv[0])) 
               

            if request.form.get('Discount'):
                Discount = request.form.get('Discount')
                if serv[2] != Discount:
                    mycursor.execute('UPDATE PROMO SET Discount = ' +str(Discount)+ 'WHERE PromoId = '+ str(serv[0])) 

            if request.form.get('Amount'):
                Amount = request.form.get('Amount')
                if Amount == "None" and serv[3] != None:
                    mycursor.execute('UPDATE PROMO SET Amount = NULL WHERE PromoId = ' + str(serv[0])) 
                elif Amount != "None" and serv[3] != Amount:
                    mycursor.execute('UPDATE PROMO SET Amount = ' + str(Amount) + 'WHERE PromoId = ' + str(serv[0]))


            if request.form.get('valid_until'):
                valid_until = request.form.get('valid_until').replace('-', '/')
                valid_until1 = 'TO_DATE(\'' + valid_until + '\' ,' + '\'YYYY/MM/DD\')'
                if valid_until == "None" and serv[4] != None:
                    mycursor.execute('UPDATE PROMO SET valid_until = NULL WHERE PromoId = ' + str(serv[0])) 
                    #pass
                elif valid_until != "None" and serv[4] != valid_until:
                    mycursor.execute('UPDATE PROMO SET valid_until = ' + str(valid_until1) + 'WHERE PromoId = ' + str(serv[0]))
                    #mes = 'UPDATE PROMO SET valid_until = ' + str(valid_until1) + 'WHERE PromoId = ' + str(serv[0])
            mycursor.execute('COMMIT')   

            mycursor.execute('select * from promo')
            result = mycursor.fetchall()
            promo = []
            for zap in result:
                promo.append(zap[1])
            conn.close
            return render_template('changePromo.html', message = "Данные о промокоде обновлены", promo=promo)
            #return render_template('changePromo.html', message = mes, promo=promo)

    return render_template('changePromo.html', promo=promo)











@manage.route('/manage/workers')
def idx7():
       
    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    mycursor = conn.cursor()
    mycursor.execute('select * from WORKERS ORDER BY fk_pos')
    temp = mycursor.fetchall()
    mycursor.execute('select PosID, Pos_Name from POSITIONS')
    result1 = mycursor.fetchall()
    tmp = []
    result = []
    global wd
    for k in result1:
        wd[k[1]] = [k[0]]  

    for elem in temp:
        for i in elem:
            tmp.append(i)
        result.append(tmp)
        tmp = []

    for elem in result:
        for elem1 in result1:
            if elem[4] == elem1[0]:
                elem[4] = elem1[1]

    conn.close

    return render_template('manage.html', rezworker=result, work = wd)
@manage.route('/manage/workers/change', methods=['POST', 'GET'])
def idx12():
    global cur_work
    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    mycursor = conn.cursor()
    mycursor.execute('select * from workers')
    result = mycursor.fetchall()
    work = []
    for zap in result:
        work.append(zap[1])

    mycursor.execute('select PosID, Pos_Name from POSITIONS')
    result1 = mycursor.fetchall()
    for k in result1:
        wd[k[1]] = [k[0]]  
    conn.close

    if request.method == 'POST':
        # выводим данные о выбранном сотруднике для их изменения
        if (request.form.get('cur_work')):
            cur_work = request.form.get('cur_work')
            
            for zap in result:
                if zap[1] == cur_work:
                    serv = zap
                    break
            flag = 1
            return render_template('changeWorkers.html', work=work, serv = serv, flag = flag, wrk = cur_work, workers = wd)
        # Удаляем выбранного сотрудника
        elif request.form.get('del_work'):
            del_work = request.form.get('del_work')
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute("DELETE FROM WORKERS WHERE FIO = " + "'"+ del_work + "'")
            mycursor.execute('COMMIT')


            mycursor.execute('select * from WORKERS')
            result = mycursor.fetchall()
            work = []
            for zap in result:
                work.append(zap[1])
            
            conn.close

            return render_template('changeWorkers.html', message = "Данные успешно удалены из базы данных",  work=work , workers = wd)
        # Обрабатываем запрос на добавление данных
        elif request.form.get('FIO1'):
            fields = []
            fields1 = []
            if request.form.get('FIO1'):
                FIO1 = request.form.get('FIO1')
                fields.append('\''+str(FIO1)+'\'')
                fields1.append("FIO")

            if request.form.get('Birth_Date1'):
                Birth_Date1 = request.form.get('Birth_Date1').replace('-', '/')
                Birth_Date2 = 'TO_DATE(\'' + Birth_Date1 + '\' ,' + '\'YYYY/MM/DD\')'
                fields.append(Birth_Date2)
                fields1.append('Birth_Date')

            if request.form.get('Phone1'):
                Phone1 = request.form.get('Phone1')
                fields.append('\''+str(Phone1)+'\'')
                fields1.append("Phone")

            if request.form.get('fk_pos1'):
                fk_pos1 = request.form.get('fk_pos1')
                fk_pos1 = str(wd[fk_pos1][0])
                fields.append(fk_pos1)
                fields1.append('fk_pos')
            
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

            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()

            mycursor.execute('INSERT INTO WORKERS (WorkerID, ' + mystr1 + ') VALUES (WorkerID.NextVal, ' + mystr + ')')
            mycursor.execute('COMMIT')

            mycursor.execute('select * from workers')
            result = mycursor.fetchall()
            work = []
            for zap in result:
                work.append(zap[1])
            conn.close
            return render_template('changeWorkers.html', message = 'Данные успешно добавлены', work=work , workers = wd)
        # тут уже изменение данных
        else:
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute('select * from workers')
            result = mycursor.fetchall()

            for zap in result:
                if zap[1] == cur_work:
                    serv = zap

            if request.form.get('FIO'):
                FIO = request.form.get('FIO')
                if serv[1] != FIO:
                    mycursor.execute('UPDATE WORKERS SET FIO = ' + '\''+str(FIO)+'\'' + 'WHERE WorkerId = '+ str(serv[0])) 
               
            if request.form.get('Phone'):
                Phone = request.form.get('Phone')
                if serv[3] != Phone:
                    mycursor.execute('UPDATE WORKERS SET Phone = ' + '\''+str(Phone)+'\'' + 'WHERE WorkerId = '+ str(serv[0])) 

            if request.form.get('fk_pos'):
                fk_pos = request.form.get('fk_pos')
                fk_pos = wd[fk_pos]
                if serv[4] != fk_pos:
                    mycursor.execute('UPDATE WORKERS SET fk_pos = ' +str(fk_pos[0])+ 'WHERE WorkerId = '+ str(serv[0])) 
                    

            if request.form.get('Birth_Date'):
                Birth_Date = request.form.get('Birth_Date').replace('-', '/')
                Birth_Date1 = 'TO_DATE(\'' + Birth_Date + '\' ,' + '\'YYYY/MM/DD\')'
                if Birth_Date == "None" and serv[2] != None:
                    mycursor.execute('UPDATE WORKERS SET Birth_Date = NULL WHERE WorkerId = ' + str(serv[0])) 
                elif Birth_Date != "None" and serv[2] != Birth_Date:
                    mycursor.execute('UPDATE WORKERS SET Birth_Date = ' + str(Birth_Date1) + 'WHERE WorkerId = ' + str(serv[0]))
            
            mycursor.execute('COMMIT')   

            mycursor.execute('select * from workers')
            result = mycursor.fetchall()
            work = []
            for zap in result:
                work.append(zap[1])
            conn.close
            return render_template('changeWorkers.html', message = "Данные о сотруднике обновлены", work=work, workers = wd)
            #return render_template('changeWorkers.html', message = str(fk_pos[0]), work=work, workers = wd)

    return render_template('changeWorkers.html', work=work, workers = wd)



@manage.route('/manage/pos')
def idx8():
       
    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    mycursor = conn.cursor()
    mycursor.execute('select * from POSITIONS')
    result = mycursor.fetchall()

    conn.close

    return render_template('manage.html', rezposition=result)

@manage.route('/manage/pos/change', methods=['POST', 'GET'])
def idx13():
    global cur_pos
    conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
    mycursor = conn.cursor()
    mycursor.execute('select * from positions')
    result = mycursor.fetchall()
    pos = []
    for zap in result:
        pos.append(zap[1])
    conn.close

    if request.method == 'POST':
        # выводим данные о выбранном сотруднике для их изменения
        if (request.form.get('cur_pos')):
            cur_pos = request.form.get('cur_pos')
            
            for zap in result:
                if zap[1] == cur_pos:
                    serv = zap
                    break
            flag = 1
            return render_template('changePos.html', pos=pos, serv = serv, flag = flag, ps = cur_pos)
        # Удаляем выбранную должность
        elif request.form.get('del_pos'):
            del_pos = request.form.get('del_pos')
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute("DELETE FROM POSITIONS WHERE Pos_Name = " + "'"+ del_pos + "'")
            mycursor.execute('COMMIT')


            mycursor.execute('select * from POSITIONS')
            result = mycursor.fetchall()
            pos = []
            for zap in result:
                pos.append(zap[1])
            
            conn.close

            return render_template('changePos.html', message = "Данные успешно удалены из базы данных",  pos=pos)
        # Обрабатываем запрос на добавление данных
        elif request.form.get('Pos_Name1'):
            fields = []
            fields1 = []
            if request.form.get('Pos_Name1'):
                Pos_Name1 = request.form.get('Pos_Name1')
                fields.append('\''+str(Pos_Name1)+'\'')
                fields1.append("Pos_Name")

            if request.form.get('Salary1'):
                Salary1 = request.form.get('Salary1')
                fields.append(str(Salary1))
                fields1.append("Salary")
            
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

            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()

            mycursor.execute('INSERT INTO POSITIONS (PosID, ' + mystr1 + ') VALUES (PosID.NextVal, ' + mystr + ')')
            mycursor.execute('COMMIT')

            mycursor.execute('select * from POSITIONS')
            result = mycursor.fetchall()
            pos = []
            for zap in result:
                pos.append(zap[1])
            conn.close
            return render_template('changePos.html', message = 'Данные успешно добавлены', pos=pos)
        # тут уже изменение данных
        else:
            conn = cx_Oracle.connect(user='KURS', password='KOLOBOK', dsn=dsn)
            mycursor = conn.cursor()
            mycursor.execute('select * from positions')
            result = mycursor.fetchall()

            for zap in result:
                if zap[1] == cur_pos:
                    serv = zap

            if request.form.get('Pos_Name'):
                Pos_Name = request.form.get('Pos_Name')
                if serv[1] != Pos_Name:
                    mycursor.execute('UPDATE POSITIONS SET Pos_Name = ' + '\''+str(Pos_Name)+'\'' + 'WHERE PosId = '+ str(serv[0])) 
               
            if request.form.get('Salary'):
                Salary = request.form.get('Salary')
                if serv[2] != Salary:
                    mycursor.execute('UPDATE POSITIONS SET Salary = ' +str(Salary) + 'WHERE PosId = '+ str(serv[0])) 
            
            mycursor.execute('COMMIT')   

            mycursor.execute('select * from POSITIONS')
            result = mycursor.fetchall()
            pos = []
            for zap in result:
                pos.append(zap[1])
            conn.close
            return render_template('changePos.html', message = "Данные о должности обновлены", pos=pos)
            #return render_template('changePos.html', message, pos=pos)
           

    return render_template('changePos.html', pos=pos)

