import pymysql

# Connect to the database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1223',
    database='userdata'
)

def execute_query(query, params=None):
    with conn.cursor() as cursor:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        description = cursor.description
        return result, description

def execute_update(query, params=None):
    with conn.cursor() as cursor:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
