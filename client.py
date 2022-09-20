import socket
import threading

HOST, PORT = "localhost", 8989
FORMAT = "UTF-8"

user_name = input("> Your name: ")

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))
socket.send(user_name.encode(FORMAT))

print("1: Create a session")
print("2: Join a session")
quest = input("> ")
if quest == '1':
    socket.send(quest.encode(FORMAT))
elif quest == '2':
    socket.send(quest.encode(FORMAT))
while True:
    if quest == '1':
        id_session = input("> create an id: ")
        socket.send(id_session.encode(FORMAT))
        password_session = input("> create a password: ")
        socket.send(password_session.encode(FORMAT))
        response = socket.recv(24).decode(FORMAT)
        if response == id_session:
            break
            # IT'S GOOD!
        else:
            print(f"Server: {response}")
            # RETRY
    elif quest == '2':
        id_session = input("> id: ")
        password_session = input("> password: ")
        socket.send(id_session.encode(FORMAT))
        socket.send(password_session.encode(FORMAT))
        response = socket.recv(24).decode(FORMAT)
        if response == id_session:
            break
            # IT'S GOOD!
        else:
            print(f"Server: {response}")
            # RETRY


def sending():
    running = True
    while running:

        try:
            message_input = input("").encode(FORMAT)
        except EOFError:
            print("Error: leaving")
            running = False
            break

        try:
            socket.send(message_input)
        except OSError:
            print("Error: SERVER OFF, message not sent...")
            running = False
            break

    socket.close()


def recving():
    running = True
    s_data = ""
    while running:

        try:
            s_data = socket.recv(500).decode(FORMAT)
        except ConnectionAbortedError:
            running = False
            print("Error: leaving")
            break
        except ConnectionResetError:
            print("Error: SERVER OFF, battery is low...")
            break

        if s_data == "quit":
            running = False
            print("Error: SERVER OFF, is shutdowned")
            break

        print(s_data)

    socket.close()

threading.Thread(target=sending).start()
threading.Thread(target=recving).start()


