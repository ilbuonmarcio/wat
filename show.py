import numpy as np
import matplotlib.pyplot as plt
import pymysql.cursors
from datetime import datetime, timedelta
    
datetime_begin = datetime.today() - timedelta(days=1)

connection = pymysql.connect(host='localhost',
                             user='wat',
                             password='123',
                             database='wat',
                             cursorclass=pymysql.cursors.DictCursor)

# Getting records from database
with connection:
    with connection.cursor() as cursor:
        # Create a new record
        sql = """SELECT
                    HOUR(datetimestamp) AS hour,
                    MIN(input) AS min_input,
                    MAX(input) AS max_input,
                    MIN(output) AS min_output,
                    MAX(output) AS max_output
                FROM
                    logs
                WHERE
                    datetimestamp >= %s
                GROUP BY
                    HOUR(datetimestamp)
                ORDER BY
                    datetimestamp ASC;"""
        cursor.execute(sql, (datetime_begin))

        result = cursor.fetchall()
        result = [[str(row['hour']) for row in result], [float(row['max_input']) for row in result], [row['max_output'] for row in result], [row['min_input'] for row in result], [row['min_output'] for row in result]]

        plt.plot(result[0], result[1])
        plt.plot(result[0], result[2])
        plt.plot(result[0], result[3])
        plt.plot(result[0], result[4])
        plt.ylabel('Input/Output')
        plt.savefig('input_output.png', dpi=600)