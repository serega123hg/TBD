from managers.DatabaseManager import DatabaseManager

from app import db
from models.lecturer import Lecturer
from models.schedule import Schedule


db_manager = DatabaseManager(db)

# db_manager.add_interval(interval='9:30 - 11:05')
# db_manager.add_interval(interval='11:20 - 12:55')
# db_manager.add_interval(interval='13:10 - 14:45')
# db_manager.add_interval(interval='15:25 - 17:00')

# db_manager.add_group(name='БФИ1801')
# db_manager.add_group(name='БВТ1801')
# db_manager.add_group(name='БСТ1801')
# db_manager.add_group(name='БФИ1802')
# db_manager.add_group(name='БФИ1701')
# db_manager.add_group(name='БВТ1802')
# db_manager.add_group(name='БСТ1701')

# db_manager.add_subject(subject_name="АВС")
# db_manager.add_subject(subject_name="ОС")
# db_manager.add_subject(subject_name="ОИБК")
# db_manager.add_subject(subject_name="ОИБ")
# db_manager.add_subject(subject_name="СТ")
# db_manager.add_subject(subject_name="РиСПСиИТ")
# db_manager.add_subject(subject_name="РКПО")
# db_manager.add_subject(subject_name="ФИЗРА")
# db_manager.add_lecturer(name='Тимур', last_name='Фатхулин', surname='Джалилевич')
# db_manager.add_lecturer(name="Владимир", last_name='Владимиров', surname='Львович')
# db_manager.add_lecturer(name="Светлана", last_name='Королева', surname='Анатольевна')
# db_manager.add_lecturer(name="Алексей", last_name='Смирнов', surname='Эдуардович')
# db_manager.add_lecturer(name="Алексей", last_name='Руднев', surname='Николаевич')
# db_manager.add_lecturer(name="Михаил", last_name='Городничев', surname='Геннадьевич')
# db_manager.add_lecturer(name="Татьяна", last_name='Королькова', surname='Валерьевна')
# db_manager.add_lecturer(name="Наталья", last_name='Трубникова', surname='Владимировна')

# row = db.session.query(Lecturer).all()
# for r in row:
#     if r.name == "Тимур"
#         print("{}, {}".format(r.name, r.last_name))
#         print("\n")
# lecturer = "Тимур Фатхулин Джалилевич"
# lecturer_id = db.session.query(Lecturer.id).filter_by(lecturer=lecturer).first()[0]
# print(lecturer_id)
# x =  db.session.query(Schedule).get(1)
# db.session.delete(x)
# print(x)



# ЛОГИКА
# идти по дням в цикле, например от 0 до 6 (дни), в каждом цикле от 0 до 4 (пары), далее, проверять условие: если день, интервал
# и неделя совпадают, то мы выводит по id нужную запись, иначе идем дальше. 
# Как проверить понедельник: day = понедельник
# Как проверить интервал: if inteval.id == schedule.interval_id and interval.interval == "9:30-11:05" 

# Либо, брать и проходить все записи в расписании, дальше смотреть на id интервала и дня недели. 
# И по ним расставлять.