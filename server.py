import socket
# from _thread import *
import threading

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
        while True:
            data = self.connection.recv(2048)
            data = data.decode()
            if not data:
                break
            print("from client at {}: {}".format(self.address[1], data))
            self.connection.sendall(bytes(data, 'UTF-8'))

        self.connection.close()
        print("client at ", self.address, " disconnected.")


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        print("Server is on!")
        while True:
            s.listen(1)
            connection, address = s.accept()
            new_thread = ClientThread(address, connection)
            new_thread.start()


if __name__ == '__main__':
    server()
