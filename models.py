import pymysql.cursors
import settings

# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password=settings.password)
# try:
#     connection.cursor().execute("""drop database my_db""")
# except:
#     pass
# create="""create database my_db;
#        use my_db;
#       create table tablets(name varchar(50), price varchar(50),
#       price_for varchar(50), brand varchar(50),active_substance varchar(50),
#       form varchar(50),pack varchar(50),date varchar(50));"""
#
# for element in create.split(';'):
#     try:
#         print(element)
#         connection.cursor().execute(element)
#         connection.commit()
#     except:
#         print("FAIL IN " + str(element))
#
# connection.close()

connect = pymysql.connect(host='localhost',
                          user='root',
                          password=settings.password,
                          db='my_db',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor
                          )

# with connect.cursor() as cursor:
#     cursor.execute("""show tables""")
#     print(cursor.fetchall())
#     cursor.execute('''insert into tablets(name,price,price_for,brand,
#     active_substance,form,pack,date) values('Амоксил','93,20',
#     'Упаковка / 20 шт.','КИЕВМЕДПРЕПАРАТ ОАО','500','Таблетки',
#     '20 таблеток (2 блистера по 10 шт.)','27/02/2020')''')
# connect.commit()
with connect.cursor() as cursor:
    cursor.execute("""select * from tablets;""")
    print(cursor.fetchall())
connect.close()