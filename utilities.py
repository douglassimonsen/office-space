import psycopg2
import json
env = json.load(open('env.json'))


def get_conn():
    return psycopg2.connect(**env['postgres'])


if __name__ == "__main__":
    get_conn()