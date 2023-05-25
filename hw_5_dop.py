from pprint import pprint
import psycopg2



def create_db(cur):
    ''' 1. Функция, создающая структуру БД (таблицы)'''

    cur.execute("""
        DROP TABLE  number_telefon, customer_data CASCADE;
    """)
# Создание таблицы с даными клиента

    cur.execute("""
    CREATE TABLE IF NOT EXISTS customer_data(
        client_id INTEGER UNIQUE PRIMARY KEY,
        client_name VARCHAR(35) NOT NULL,
        client_last_name VARCHAR(35) NOT NULL,
        client_email VARCHAR(35) NOT NULL
    );
    """)

# Создание таблицы с номерами телефонов клиентов

    cur.execute("""
    CREATE TABLE IF NOT EXISTS number_telefon(
        number_tel_id SERIAL PRIMARY KEY,
        client_phonenumber VARCHAR(15),
        client_id INTEGER REFERENCES customer_data(client_id)
    );
    """)

def add_client(cur, client_id, client_name, client_last_name, client_email, phones=None):
    ''' 2. Функция, позволяющая добавить нового клиента '''

# Добавляем данные клиента



    cur.execute("""
        INSERT INTO customer_data(client_id, client_name, client_last_name, client_email)
            VALUES(%s, %s, %s, %s);
    """, (client_id, client_name, client_last_name, client_email))


##    cur.execute("""
##        SELECT * FROM customer_data;
##    """)
##    print(cur.fetchall())


# Добавляем телефонный номер клиента

    cur.execute("""
        INSERT INTO number_telefon(client_phonenumber, client_id) VALUES(%s, %s);
    """, (phones, client_id))


##    cur.execute("""
##        SELECT * FROM number_telefon;
##    """)
##    print(cur.fetchall())


def add_phone(cur, client_id, phone):
    ''' 3. Функция, позволяющая добавить телефон для существующего клиента '''
    cur.execute("""
        INSERT INTO number_telefon(client_id, client_phonenumber) VALUES(%s, %s);
    """, (client_id, phone))



def change_client(cur, client_id, first_name=None, last_name=None, email=None, phones=None):
    ''' 4. Функция, позволяющая изменить данные о клиенте '''

# Меняем данные клиента

    if first_name is not None:
        cur.execute("""
        UPDATE customer_data SET client_name=%s WHERE client_id=%s;
        """, (first_name, client_id))

    if last_name is not None:
        cur.execute("""
        UPDATE customer_data SET client_last_name=%s WHERE client_id=%s;
        """, (last_name, client_id))

    if email is not None:
        cur.execute("""
        UPDATE customer_data SET client_email=%s WHERE client_id=%s;
        """, (email, client_id))


# меняем телефон клиента
    if phones is not None:
        cur.execute("""
            UPDATE number_telefon SET client_phonenumber=%s WHERE client_id=%s;
        """, (phones, client_id,))


def delete_phone(cur, client_id, phone):
    '''5. Функция, позволяющая удалить телефон для существующего клиента '''

    cur.execute("""
        DELETE FROM number_telefon WHERE client_id=%s AND client_phonenumber=%s;
    """, (client_id, phone))



def delete_client(cur, client_id):
    '''6. Функция, позволяющая удалить существующего клиента '''

    cur.execute("""
        DELETE FROM number_telefon WHERE client_id=%s;
    """, (client_id,))


    cur.execute("""
        DELETE FROM customer_data WHERE client_id=%s;
    """, (client_id,))


def find_client(cur, first_name=None, last_name=None, email=None, phones=None):
    '''7. Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону. '''
    if first_name is not None or last_name is not None or email is not None or phones is not None:
        cur.execute("""
            SELECT * FROM customer_data cd
            JOIN number_telefon nt ON cd.client_id=nt.client_id
            WHERE client_name=%s or client_last_name=%s or client_email=%s or client_phonenumber=%s;
            """, (first_name, last_name, email, phones))
        pprint(cur.fetchall())
        print()


def main():
    conn = psycopg2.connect(database="test7", user="postgres", password="password")
    with conn.cursor () as cur:
        create_db(cur)
        add_client(cur, 1, 'Иван', 'Иванов', 'wert@mm.com', '89998887766')
        add_client(cur, 2, 'Петр', 'Петров', 'wart@mm.com', '89998887755')
        add_client(cur, 3, 'Сидор', 'Сидоров', 'wуrt@mm.com', '89998887744')
        add_client(cur, 4, 'Буратино', 'Карлович', 'bur@bb.com' )
        add_client(cur, 5, 'Карабас', 'Барабас', 'karbar@bb.com', '89993222233' )
        add_phone(cur, 3, "89998887711")
        add_phone(cur, 3, "89998887722")
        add_phone(cur, 4, "89998887700")
        change_client(cur, 1, last_name='Монтан')
        change_client(cur, 1, phones='87771113366')
        delete_phone(cur, 3, '89998887711')
        delete_client(cur, 2)
        find_client(cur, last_name='Сидоров', phones='89993222233', first_name='Иван')

    conn.close

if __name__ == '__main__':
    main()


