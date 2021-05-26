import socket
import sys
from client_command_handler import parseInput

HOST = "127.0.0.1"
PORT = 8000


def client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Unable to connect to the server')
        sys.exit(-1)
    try:
        s.connect((HOST, PORT))
        while True:
            message = input()
            toSendMessage = parseInput(message)
            if toSendMessage == "":
                print("Invalid input!!!")
                continue
            s.sendall(str(len(toSendMessage.encode('utf-8'))).encode('ascii'))
            s.sendall(toSendMessage.encode('ascii'))
            data = s.recv(1024)
            print('Received from the server:', str(data.decode('ascii')))
            if message == 'stop':
                break

    except socket.error:
        print('Shit hit the fan!')
    finally:
        s.close()


if __name__ == '__main__':
    client()
