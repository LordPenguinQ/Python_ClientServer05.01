import socket
import threading
from database import *

PORT = 12345
IP_ADDRESS = '127.0.0.1'

shutdown_flag = threading.Event()

initialize_database()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP_ADDRESS, PORT))

clients = []
lock = threading.Lock()


def broadcast(message, client_socket):
    with lock:
        for client in clients:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)


def new_user(login):
    connection = create_connection('../server_db.db')
    try:
        with connection:
            user_id = check_exist_user(connection, (login,))
            if not user_id:
                user_id = add_user(connection, (login,))
            return user_id
    except Error as e:
        print(e)
    finally:
        connection.close()


def handle_client(client_socket):
    try:
        user_login = client_socket.recv(1024).decode('utf-8')
        user_id = new_user(user_login)

        stored_messages = all_messages(create_connection('../server_db.db'))
        firstMessage=True
        for stored_message in stored_messages:
            if(firstMessage):
                client_socket.send((stored_message[0] + ': ' + stored_message[1]).encode('utf-8'))
                firstMessage=False
            else:
                client_socket.send((stored_message[0] + ': ' + stored_message[1] + '\n').encode('utf-8'))

        client_socket.send(('==KONIEC HISTORI==\n').encode('utf-8'))
        client_socket.send(('/exit -> logout\n').encode('utf-8'))

        broadcast(f'{user_login} dołączył.', client_socket)

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            full_message = f'{user_login}: {message}'
            broadcast(full_message, client_socket)
            insert_message(create_connection('../server_db.db'), user_id, message)
    except Exception as e:
        # user_login = ''
        print(f"Error during client connection: {e}")
    finally:
        broadcast(f'{user_login} opuścił chat.', client_socket)
        clients.remove(client_socket)
        client_socket.close()


def accept_connections():
    while True:
        client, address = server.accept()
        clients.append(client)
        print(f"Połączono z: {address}")
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()


server.listen()
print(f"Serwer nasłuchuje: {IP_ADDRESS}:{PORT}")

accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()
