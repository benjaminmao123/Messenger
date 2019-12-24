import socket
import sys
import getpass
import threading

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Created Socket')
except socket.error:
    print('Failed to create socket.')
    sys.exit()

port = 8888
host = 'localhost'

sock.connect((host, port))
print('Connected')

# Variables

server_message = ''

# end

def Login():
    server_message = sock.recv(1024).decode()

    if server_message[0:2] == 'uu':
        username = input(server_message[2:])
        sock.send(username.encode())
    elif server_message[0:2] == 'pp':
        password = getpass.getpass(server_message[2:])
        sock.send(password.encode())
    elif server_message[0:2] == 'tt' or server_message[0:2] == 'ff':
        print(server_message[2:])

        if server_message[0:2] == 'tt':
            return True

    server_message = ''

    return False

def Receive():
    global server_message

    while True:
        data = sock.recv(1024).decode()

        if data != '':
            server_message = data

            if server_message[0:2] == 'tt':
                print(server_message[2:])
            elif server_message[0:2] == 'ff':
                print(server_message[2:])
            elif server_message[0:2] == 'um':
                print(server_message[2:])
            elif server_message[0:2] == 'lo':
                print(server_message[2:])
                break

def Send():
    global server_message

    while True:
        if server_message != '':
            if server_message[0:2] == 'mm':
                choice = input(server_message[2:])
                sock.send(choice.encode())
            elif server_message[0:2] == 'uu':
                username = input(server_message[2:])
                sock.send(username.encode())
            elif server_message[0:2] == 'pp':
                password = getpass.getpass(server_message[2:])
                sock.send(password.encode())
            elif server_message[0:2] == 'rc':
                recipient = input(server_message[2:])
                sock.send(recipient.encode())

                while (server_message[0:2] != 'tt' and server_message[0:2] != 'ff'):
                    pass

                if server_message[0:2] == 'tt':
                    message = ''
                    
                    while True:
                        message = input()
                        sock.send(message.encode())
                        
                        if message == '!exit':
                            break
            elif server_message[0:2] == 'bm':
                message = input(server_message[2:])
                sock.send(message.encode())
            elif server_message[0:2] == 'lo':
                break
            elif server_message[0:2] == 'rf':
                command = input(server_message[2:])
                sock.send(command.encode())
                
            server_message = ''

def Main():
    while Login() == False:
        pass

    t1 = threading.Thread(target = Send)
    t1.start()
    Receive()

Main()
    
sock.close()

            

