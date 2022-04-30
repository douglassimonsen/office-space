import psycopg2
import json
env = json.load(open('env.json'))


def get_conn():
    return psycopg2.connect(**env['postgres'])


def run_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    fields = [x[0] for x in cursor.description]
    return [dict(zip(fields, row)) for row in cursor.fetchall()]



if __name__ == "__main__":
    get_conn()