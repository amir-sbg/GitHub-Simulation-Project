import socket
import sys

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
            s.sendall(message.encode('ascii'))
            data = s.recv(1024)
            print('Received from the server :', str(data.decode('ascii')))
            if message == 'stop':
                break

    except socket.error:
        print('Shit hit the fan!')
    finally:
        s.close()


if __name__ == '__main__':
    client()
