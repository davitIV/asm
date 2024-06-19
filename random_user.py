import requests
import time
import psycopg2
from psycopg2 import sql

db_params = {
    'dbname': 'postgres',
    'user': 'meshvela1',
    'password': 'meshvela1',
    'host': 'localhost',
    'port': '5432'
}


def takeinfo():
    response = requests.get('https://randomuser.me/api')

    if response.status_code == 200:
        data = response.json()

        person = data['results'][0]
        name = person['name']
        full_name = f"{name['title']} {name['first']} {name['last']}"
        dob = person['dob']
        age = f"{dob['age']}"
        date_time = f"{dob['date']}"
        print(f"Name:{full_name}")
        print(f"age: {age},{date_time}")
        return full_name, date_time


def save(full_name, date_of_birth):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        create_table_query = '''
        CREATE TABLE IF NOT EXISTS person (
            full_name VARCHAR(100),
            dob DATE
        );
        '''
        cur.execute(create_table_query)
        conn.commit()

        insert_query = '''
        INSERT INTO person (full_name, dob)
        VALUES (%s, %s);
        '''
        cur.execute(insert_query, (full_name, date_of_birth))
        conn.commit()
        print(f"Inserted {full_name} into person table")

        cur.close()
        conn.close()
    except Exception as error:
        print(f"Error connecting to the database: {error}")

def main():
    while True:
        full_name, date_of_birth = takeinfo()
        if full_name and date_of_birth:
            save(full_name, date_of_birth)
        time.sleep(5)

if __name__ == "__main__":
    main()
