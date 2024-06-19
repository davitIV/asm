import os
import time
import requests
import psycopg2
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'txt.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Database:
    def __init__(self):
        self.db_params = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT')
        }
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_params['dbname'],
                user=self.db_params['user'],
                password=self.db_params['password'],
                host=self.db_params['host'],
                port=self.db_params['port']
            )
            self.cur = self.conn.cursor()
            print("Connected to the database successfully")
        except Exception as error:
            print(f"Error connecting to the database: {error}")

    def insert_person(self, full_name, dob):
        try:
            insert_query = '''
            INSERT INTO person (full_name, dob)
            VALUES (%s, %s);
            '''
            self.cur.execute(insert_query, (full_name, dob))
            self.conn.commit()
            print(f"Inserted {full_name} into person table")
        except Exception as error:
            print(f"Error inserting data: {error}")

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed")

def take_info():
    response = requests.get('https://randomuser.me/api')
    if response.status_code == 200:
        data = response.json()
        person = data['results'][0]
        name = person['name']
        full_name = f"{name['title']} {name['first']} {name['last']}"
        dob = person['dob']['date']
        print(f"Name: {full_name}")
        print(f"Date of Birth: {dob}")
        return full_name, dob
    else:
        print("Failed to retrieve data")
        return None, None

def main():
    db = Database()
    db.connect()
    while True:
        full_name, date_of_birth = take_info()
        if full_name and date_of_birth:
            db.insert_person(full_name, date_of_birth)
        time.sleep(5)
    db.close()

if __name__ == "__main__":
    main()
