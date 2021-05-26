import math
import socket
import threading
from copy import deepcopy
from file_system import *

HOST = "127.0.0.1"
PORT = 8000


# def server2():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((HOST, PORT))
#         s.listen()
#         connection, address = s.accept()
#         with connection:
#             print("Connected by", address)
#             while True:
#                 data = connection.recv(2048)
#                 if not data:
#                     break
#                 connection.sendall(data)
######################################################################################
#
#
# print_lock = threading.Lock()
#
#
# def thread(connection):
#     while True:
#         data = connection.recv(1024)
#         print('data from client: {}'.format(data))
#         if not data:
#             print('Disconnected')
#             print_lock.release()
#             break
#
#         connection.sendall(data)
#     connection.close()
#
#
# def server():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((HOST, PORT))
#         s.listen()
#         print("Server is listening on {}".format(PORT))
#
#         while True:
#             connection, address = s.accept()
#             print_lock.acquire()
#             print('Connected to :', address[0], ':', address[1])
#             start_new_thread(thread, (connection,))
######################################################################################


class ClientThread(threading.Thread):
    def __init__(self, address, client_socket):
        threading.Thread.__init__(self)
        self.connection = client_socket
        self.address = address
        print("connection established with: ", address)

    def run(self):
        username = password = current_repository = None
        while True:
            data = self.connection.recv(2048)
            data = data.decode()
            string_data = ""
            for i in range(math.ceil(int(data) / 2048)):
                temp = self.connection.recv(2048)
                temp = temp.decode()
                string_data = string_data + str(temp)
            if not string_data:
                break
            # print("from client at {}: {}".format(self.address[1], data))
            if username is not None:
                answer = parseReceivedMessage(string_data, authenticate_user(username, password), current_repository)
            else:
                answer = parseReceivedMessage(string_data, None, current_repository)

            if type(answer) == list and len(answer) == 2:
                username = deepcopy(answer[0])
                password = deepcopy(answer[1])
                answer = "User logged in"
            if type(answer) == list and len(answer) == 1:
                current_repository = answer[0]
                answer = "Repository selected :)"

            if answer is None:
                answer = "ERROR!"

            self.connection.sendall(bytes(answer, 'UTF-8'))

        self.connection.close()
        print("client at ", self.address, " disconnected.")


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        print("Server is on!")
        while True:
            s.listen(1)
            connection, address = s.accept()
            new_thread = ClientThread(address, connection)
            new_thread.start()


def parseReceivedMessage(command, user, current_repository):
    parts = command.split("$")
    action = parts[0]
    print("action: ", action)
    if action == '1' and user is None:
        allocate_new_user(parts[1], parts[2])
        user = authenticate_user(parts[1], parts[2])
        return "User created"

    if action == '2' and user is None:
        user = authenticate_user(parts[1], parts[2])
        if user is None:
            return None
        return [user.get_username(), user.get_password()]

    if action == '3' and user is not None:
        create_repository_for_user(user.get_username(), user.get_password(), parts[1])
        return "done"

    if action == '4' and user is not None:
        repositories = user.get_repositories()
        answer = ""
        for x in repositories:
            answer = answer + "\n" + str(x)
        return answer

    if action == '5' and user is not None:
        if current_repository is not None:
            return "Your are currently in a repository!!!"
        repository_name = parts[1]
        repositories = user.get_repositories()
        exist = False
        for x in repositories:
            if str(x) == str(repository_name):
                exist = True
                break
        if not exist:
            return None
        return [repository_name]

    if action == '6' and user is not None:
        push_server_side(user.get_username(), user.get_password(), parts[2], current_repository)


if __name__ == '__main__':
    server()
