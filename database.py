import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None


def create_table(connection, create_table_sql):
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)


def add_user(connection, user):
    sql = '''INSERT INTO users(login) VALUES(?)'''

    cursor = connection.cursor()
    cursor.execute(sql, user)
    connection.commit()

    return cursor.lastrowid


def check_exist_user(connection, user):
    sql = '''SELECT id FROM users WHERE login like ?'''

    cursor = connection.cursor()
    cursor.execute(sql, user)
    connection.commit()

    login = cursor.fetchone()
    return login[0] if login else None


def insert_message(connection, client_id, message):
    sql = '''INSERT INTO chat(client_id, message) VALUES (?, ?)'''

    send = (client_id, message)

    cursor = connection.cursor()
    cursor.execute(sql, send)
    connection.commit()
    return cursor.lastrowid


def all_messages(connection):
    sql = '''SELECT users.login, chat.message FROM users JOIN chat WHERE users.id=chat.client_id'''

    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()

    return cursor.fetchall()


def clear_chat(connection):
    sql = '''DELETE FROM chat'''

    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()

    return cursor.fetchall()


def initialize_database():
    baza = 'server_db.db'

    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        login text NOT NULL
                                    );"""

    sql_create_chat_table = """CREATE TABLE IF NOT EXISTS chat (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    client_id integer NOT NULL,
                                    message text NOT NULL,
                                    FOREIGN KEY (client_id) REFERENCES users (id)
                                );"""

    connection = create_connection(baza)

    if connection is not None:
        create_table(connection, sql_create_users_table)
        create_table(connection, sql_create_chat_table)
    else:
        print("Error! Nie udało się stworzyć tabel :(")

    connection.close()


def all_users(connection):
    sql = '''SELECT id, login FROM users'''

    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()

    return cursor.fetchall()


def remove_user(connection, nick):
    sql = '''DELETE FROM users WHERE login LIKE ?'''

    cursor = connection.cursor()
    cursor.execute(sql, nick)
    connection.commit()

    return cursor.fetchall()

def check_users_id(connection, user_id):
    sql = '''SELECT id FROM users WHERE id = ?'''

    cursor = connection.cursor()
    cursor.execute(sql, user_id)
    connection.commit()

    login = cursor.fetchone()
    return login[0] if login else None

def add_user_with_id(connection,user_id,login):
    sql = '''INSERT INTO users(id, login) VALUES(?, ?)'''

    send=(user_id,login)

    cursor = connection.cursor()
    cursor.execute(sql, send)
    connection.commit()

    return cursor.lastrowid

if __name__ == '__main__':
    initialize_database()
