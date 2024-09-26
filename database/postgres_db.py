import psycopg2
from decouple import config

connect_db = {
    'dbname': config('DB_NAME'),
    'user':  config('DB_USER'),
    'host': config('DB_HOST'),
    'password': config('DB_PASSWORD'),
    'port': config('DB_PORT')
}
def connect():
   

   try:
        conn = psycopg2.connect(**connect_db)
        cursor = conn.cursor()

        create_table = (

                """
                CREATE TABLE students(
                      id SERIAL PRIMARY KEY,
                      surname_name VARCHAR(100),
                      first_name VARCHAR(100),
                      last_name VARCHAR(100),
                      email VARCHAR(50) UNIQUE NOT NULL,
                      phone_number NUMERIC(11),
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS transaction(
                       id SERIAL PRIMARY KEY,
                       name VARCHAR(100)
                       account_number NUMERIC(10) NOT NULL,
                       account NUMERIC (10,2), 
                       user_id INT,
                       FOREIGN KEY(user_id) REFERENCES user_acct(id),
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
        )

        cursor.execute(create_table)
        conn.commit()
        print("Table Created Successfully")
   except psycopg2.Error as e:
              if conn:
                     conn.rollback()
              print(e)
              return conn
#    finally:
    #          if conn:
    #                    conn.close()
    #          if cursor:
    #                    cursor.close()