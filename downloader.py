import csv
import pymysql.cursors
import settings


def csv_reader(file_obj):
    reader = csv.reader(file_obj)
    next(reader)
    exit_list = []
    list_of_products = []
    for row in reader:
        list_of_products.append(row)
    for n in list_of_products:
        exit_list.append(tuple(n))
    connect = pymysql.connect(host='localhost',
                              user='root',
                              password=settings.password,
                              db='my_db',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor
                              )
    for n in exit_list:
        with connect.cursor() as cursor:
            cursor.execute(
                F"insert into tablets(name,price,price_for,"
                F"brand,active_substance,form,pack,date) values{n}")
        connect.commit()
    return exit_list


with open('base.csv', "r") as f_obj:
    print(csv_reader(f_obj))
