from django.db import connection
from collections import namedtuple
from functools import wraps

def map_cursor(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def query(query_str: str):
    hasil = []
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO 'MARMUT'")

        try:
            cursor.execute(query_str)

            if query_str.strip().lower().startswith("select"):
                # Kalau ga error, return hasil SELECT
                hasil = map_cursor(cursor)
            else:
                # Kalau ga error, return jumlah row yang termodifikasi oleh INSERT, UPDATE, DELETE
                hasil = cursor.rowcount
        except Exception as e:
            # Ga tau error apa
            hasil = e

    return hasil

def connectdb(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with connection.cursor() as cursor:
            # cursor.execute("SET search_path to MARMUT;")
            return func(cursor, *args, **kwargs)
        
    return wrapper
