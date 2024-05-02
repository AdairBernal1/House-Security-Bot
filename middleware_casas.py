import threading
from pyswip import Prolog

prolog_lock = threading.Lock()

def get_alerta_recursiva():
    with prolog_lock:
        prolog = Prolog()
        prolog.consult('casas.pl')

        results = list(prolog.query('generar_hechos'))

        results = list(prolog.query('alerta_recursiva(Alerta)'))

        return ', '.join(map(str, results))

get_alerta_recursiva()

import pymysql
from datetime import datetime, timedelta

connection = pymysql.connect(host='localhost',
                             user='user2',
                             password='123',
                             db='casas_db')

try:
    with connection.cursor() as cursor:
        now = datetime.now()

        one_hour_ago = now - timedelta(hours=1)

        now_str = now.strftime('%Y-%m-%d')
        one_hour_ago_str = one_hour_ago.strftime('%Y-%m-%d %H:%M:%S')

        query_today = f"SELECT * FROM alertas WHERE DATE(fecha) = '{now_str}'"

        cursor.execute(query_today)

        result_today = cursor.fetchall()

        print("Alertas from today:")
        for row in result_today:
            print(row)

        query_last_hour = f"SELECT * FROM alertas WHERE fecha >= '{one_hour_ago_str}' AND DATE(fecha) = '{now_str}'"

        cursor.execute(query_last_hour)

        result_last_hour = cursor.fetchall()

        print("Alertas from the last hour of today:")
        for row in result_last_hour:
            print(row)

finally:
    connection.close()
