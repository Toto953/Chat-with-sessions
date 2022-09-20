import socket
import threading
import os

from session import Session

HOST, PORT = "localhost", 8989
FORMAT = "UTF-8"

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, PORT))
socket.listen()
os.system("cls")
print("> Server ON <")

session = Session()

global sessions
server_on = True
stop_thread = False
sessions = [[["main_session", "any"]]]

def handling(user_name, s_client, h_client, stop_thread):

    id_session = ""
    password_session = ""

    print(f"{user_name} has join the main session!")

    option = s_client.recv(4).decode(FORMAT)
    running = True
    if option == '1':
        while running:
            id_session = s_client.recv(24).decode(FORMAT)
            password_session = s_client.recv(24).decode(FORMAT)
            if not session.id_is_already(id_session):
                s_client.send(id_session.encode(FORMAT))
                session.set_id_and_password(id_session, password_session)
                for i in sessions[0]:
                    if i[1] == s_client:
                        sessions[0].remove(i)
                sessions.append([[id_session, password_session], [user_name, s_client, h_client, stop_thread]])
                running = False
            else:
                s_client.send("already id".encode(FORMAT))
    elif option == '2':
        running = True
        while running:
            id_session = s_client.recv(24).decode(FORMAT)
            password_session = s_client.recv(24).decode(FORMAT)
            if session.id_is_already(id_session):
                index = 0
                for i in sessions:
                    if i[0][0] == id_session:
                        if i[0][1] == password_session:
                            s_client.send(id_session.encode(FORMAT))
                            for i in sessions[0]:
                                if i[1] == s_client:
                                    sessions[0].remove(i)
                            sessions[index].append([user_name, s_client, h_client, stop_thread])
                            running = False
                            break
                        else:
                            s_client.send("password is invalid...".encode(FORMAT))
                    index+=1
            else:
                s_client.send("id doesn't exist...".encode(FORMAT))

    running = True
    while running:

        try:
            c_data = s_client.recv(500).decode(FORMAT)
        except ConnectionResetError:
            running = False
            break
        except ConnectionAbortedError:
            running = False
            break

        print(f"{user_name}: {c_data}")

        for i in sessions:
            for j in i[1:]:
                if i[0][0] == id_session:
                    if j[1] == s_client:
                        if j[-1] == True:
                            running = False
                    else:
                        j[1].send(f"{user_name}: {c_data}".encode(FORMAT))



    for i in sessions:
        for j in i[1:]:
            if j[1] != s_client:
                j[1].send(f"Server: {user_name} has left...".encode(FORMAT))

    s_client.close()
    index = 0
    for i in sessions:
        for j in i[1:]:
            if j[1] == s_client:
                j[1].close()
                sessions[index].remove(j)
        index+=1

    for i in sessions:
        if len(i) == 1 and i != [["main_session", "any"]]:
            sessions.remove(i)

def admin():
    global sessions
    running = True
    while running:
        user_input = input("")

        os.system("cls")
        print("""
            0: shutdown the server
            1: Number of sessions
            2 <username>: remove a client
            3: list of usernames client
        """)

        if user_input == '0':
            user_input = input("> Are you sure? (Y/n): ").lower()
            if user_input == '' or user_input == 'y' or user_input == 'yes': 
                for i in sessions:
                    for j in i[1:]:
                        j[-1] = True
                    running = False
            else:
                print("> Shutdowning is canceled. <")

        elif user_input == '1':
            print(f"> {len(sessions)-1} of session in server <")
        
        elif user_input == f"2 {user_input[2:]}":
            for i in sessions:
                if i[1][0] == user_input[2:]:
                    i[1][1].send("Server: Disconnected by admin!".encode(FORMAT))
                    i[1][1].close()
                    print(f"> {i[1][1]} is ban! <")

        elif user_input == '3':
            for i in sessions:
                for j in i[1:]:
                    print(j[0])
        
        elif user_input == '4':
            print(sessions)

    socket.close()


threading.Thread(target=admin).start()

print("""
    0: shutdown the server
    1: Number of clients connected
    2 <username>: remove a client
    3: Instructions
""")

while server_on:

    try:
        s_client, h_client = socket.accept()
    except OSError:
        for i in sessions:
            for j in i[1:]:
                j[1].close()
        print("> Server shutdowning <")
        server_on = False
        break
    user_name = s_client.recv(24).decode(FORMAT)
    sessions[0].append([user_name, s_client, h_client, stop_thread])
    threading.Thread(target=handling, args=(user_name, s_client, h_client, stop_thread)).start()

print("> Server is OFF <")
