import socket
import sys
import threading
import time

try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('Socket Created')
except socket.error:
        print('Failed to create socket.')
        sys.exit()

port = 8888
host = ''

try:
        sock.bind((host, port))
        print('Bind Complete')
except socket.error:
        print('Bind failed.')
        sys.exit()

print('Listening')
sock.listen(3)

# Variables

LoginInfo = {'a': 'a', 'b': 'b', 'c': 'c'}
LiveUserMessage = {'a': [0, ''], 'b': [0, ''], 'c': [0, '']}
Users = ['a', 'b', 'c']
UnreadUserMessages = {'a': [], 'b': [], 'c': []}
UserMessengerStatus = {'a': 0, 'b': 0, 'c': 0}
UserStatus = {'a': 0, 'b': 0, 'c': 0}
FriendRequests = {'a': [], 'b': [], 'c': []}
Friends = {'a': [], 'b': [], 'c': []}
StatusUpdates = {'a': [], 'b': [], 'c': []}

# end

def Login(conn):
    global UserStatus
    global LoginInfo

    conn.send(('uu' + '\nEnter your username: ').encode())
    username = conn.recv(1024).decode()
    
    conn.send(('pp' + 'Enter your password: ').encode())
    password = conn.recv(1024).decode()

    if LoginInfo.get(username) == password:
        conn.send(('tt' + '\nSuccessfully logged in.').encode())
        UserStatus[username] = 1
        return True, username
    else:
        conn.send(('ff' + '\nFailed to log in.').encode())

    return False, username

def ChangePassword(conn, username):
    global LoginInfo

    conn.send(('pp' + '\nEnter your old password: ').encode())
    old_password = conn.recv(1024).decode()

    if LoginInfo.get(username) == old_password:
        conn.send(('pp' + 'Enter your new password: ').encode())
        LoginInfo[username] = conn.recv(1024).decode()
        
        conn.send(('tt' + '\nSuccessfully changed password.').encode())
    else:
        conn.send(('ff' + '\nFailed to change password.').encode())

def ReceiveMessage(conn, username, recipient):
    global LiveUserMessage
    global UserMessengerStatus
    global UnreadUserMessages

    while True:
        data = conn.recv(1024).decode()
        
        if (data != '!exit'):
            if UserMessengerStatus[recipient] == 1:
                LiveUserMessage[recipient][0] = 1
                LiveUserMessage[recipient][1] = username + ': ' + data
            else:
                UnreadUserMessages[recipient].append(username + ': ' + data)
        else:
            LiveUserMessage[username][0] = 1
            LiveUserMessage[username][1] = data
            return

def SendMessage(conn, username, recipient):
    global LiveUserMessage

    while True:
        if LiveUserMessage[username][0] == 1:
            if LiveUserMessage[username][1] != '!exit':
                conn.send(('um' + LiveUserMessage[username][1]).encode())
                LiveUserMessage[username][0] = 0
            else:
                LiveUserMessage[username][0] = 0
                break

def Messenger(conn, username):
    global UserMessengerStatus

    conn.send(('rc' + '\nEnter the message recipient: ').encode())
    recipient = conn.recv(1024).decode()

    if (LoginInfo.get(recipient) != None):
        conn.send(('tt' + '\nYou are chatting with: ' + recipient + '. Type \'!exit\' to quit.\n').encode())
        UserMessengerStatus[username] = 1
    else:
        conn.send(('ff' + '\nUser does not exist.').encode())
        return

    t1 = threading.Thread(target = ReceiveMessage, args = (conn, username, recipient,))
    t1.start()
    SendMessage(conn, username, recipient)
    UserMessengerStatus[username] = 0

def UnreadMessages(conn, username):
    global UnreadUserMessages

    if len(UnreadUserMessages[username]) <= 0:
        conn.send(('ff' + '\nYou have no unread messages.').encode())
    else:
        conn.send(('tt' + '\nYour unread messages are: \n').encode())

        messages = ''

        for i in range(len(UnreadUserMessages[username]) - 1):
            messages += UnreadUserMessages[username][i] + '\n'

        messages += UnreadUserMessages[username][len(UnreadUserMessages[username]) - 1]
        conn.send(('um' + messages).encode())

        del UnreadUserMessages[username][:]

def BroadcastMessage(conn, username):
    global UnreadUserMessages
    global UserStatus

    conn.send(('bm' + '\nEnter a message to broadcast: ').encode())
    data = conn.recv(1024).decode()

    for i in Users:
        if i != username and UserStatus[i] == 1:
            UnreadUserMessages[i].append(username + ': ' + data)

def Logout(conn, username):
    global UserStatus

    UserStatus[username] = 0
    conn.send(('lo' + '\nLogging out.').encode())
    conn.close()

def Refresh():
    return

def SendFriendRequest(conn, username):
    global FriendRequests

    conn.send(('uu' + '\nEnter the name of the user you want to add: ').encode())
    name = conn.recv(1024).decode()
    
    if FriendRequests.get(name) != None:
        FriendRequests[name].append(username)

def ViewFriendRequests(conn, username):
    global FriendRequests
    global Friends

    if len(FriendRequests[username]) <= 0:
        conn.send(('ff' + '\nYou have no pending friend requests.').encode())
    else:
        while True:
            conn.send(('tt' + '\nYour pending friend requests are from: \n').encode())
            
            friends = ''

            for i in range(len(FriendRequests[username]) - 1):
                friends += FriendRequests[username][i] + '\n'

            friends += FriendRequests[username][len(FriendRequests[username]) - 1]
            conn.send(('um' + friends).encode())

            time.sleep(0.1)

            conn.send(('rf' + '\nType !accept <name> or !reject <name> to accept or reject a friend request.'
                            + '\nFor example: \'!accept a\' to add \'a\' as a friend.'
                            + '\nType \'!exit\' to quit.\n\n').encode())

            command = conn.recv(1024).decode()

            if command == '!exit':
                break

            if command[0:7] == '!accept':
                Friends[username].append(command[8:])
                Friends[command[8:]].append(username)
            
            FriendRequests[username] = [name for name in FriendRequests[username] if name is not command[8:]]
            FriendRequests[command[8:]] = [name for name in FriendRequests[command[8:]] if name is not username]

def PostStatus(conn, username):
    global StatusUpdates

    conn.send(('bm' + '\nEnter your message for your status update: ').encode())
    message = conn.recv(1024).decode()
    StatusUpdates[username].append(message)
    conn.send(('tt' + '\nStatus successfully posted.'))

def ViewWall(conn, username):
    global StatusUpdates

    conn.send(('tt' + '\nYour wall: \n').encode())

    wall = ''
    j = 0

    for i in range(len(StatusUpdates[username]) - 1, -1, -1):
        j += 1
        wall += str(j) + ': ' + '\nName: ' + username + '\n' + 'Status: ' + StatusUpdates[username][i] + '\n\n'
    
    conn.send(('um' + wall).encode())

def ViewFriendStatus(conn, username):
    global StatusUpdates
    global Friends

    conn.send(('tt' + '\nYour friends\' statuses: ').encode())

    print(Friends[username][0])
    wall = ''

    for i in Friends[username]:
        order = 0

        for j in range(len(StatusUpdates[i]) - 1, -1, -1):
            order += 1
            wall += '\n' + str(order) + ': ' + '\nName: ' + i + '\n' + 'Status: ' + StatusUpdates[i][j] + '\n'
    
        conn.send(('um' + wall).encode())

def Menu(conn, username):
    while True:
        try:
            time.sleep(0.1)

            unreadMessageCount = len(UnreadUserMessages[username])
            friendRequestCount = len(FriendRequests[username])

            conn.send(('mm' + '\nMenu'
                            + '\n1. Change Password'
                            + '\n2. Messenger'
                            + '\n3. View Unread Messages (' + str(unreadMessageCount) + ')'
                            + '\n4. Broadcast Message'
                            + '\n5. Logout'
                            + '\n6. Refresh'
                            + '\n7. Send Friend Request'
                            + '\n8. View Friend Requests (' + str(friendRequestCount) + ')'
                            + '\n9. Post Status'
                            + '\n10. View Wall'
                            + '\n11. View Friend Status'
                            + '\n\nChoose an option: ').encode())

            choice = conn.recv(1024).decode()

            if choice == '1':
                ChangePassword(conn, username)
            elif choice == '2':
                Messenger(conn, username)
            elif choice == '3':
                UnreadMessages(conn, username)
            elif choice == '4':
                BroadcastMessage(conn, username)
            elif choice == '5':
                Logout(conn, username)
                return
            elif choice == '6':
                Refresh()
            elif choice == '7':
                SendFriendRequest(conn, username)
            elif choice == '8':
                ViewFriendRequests(conn, username)
            elif choice == '9':
                PostStatus(conn, username)
            elif choice == '10':
                ViewWall(conn, username)
            elif choice == '11':
                ViewFriendStatus(conn, username)
        except:
            continue

def ClientThread(conn):
    username = ''

    while True:
        success, username = Login(conn)

        if (success):
            break

    Menu(conn, username)

while True:
    conn, addr = sock.accept()

    print('Connected with ' + addr[0] + ':' + str(addr[1]))

    t1 = threading.Thread(target = ClientThread, args = (conn,))
    t1.start()

sock.close()