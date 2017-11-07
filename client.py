import socket
import sys
import _thread

def send_msg():
    while True:
        print("Enter message:  ")
        msg = sys.stdin.readline()
        if "exit()" in msg:
            sock.send(msg)
            _thread.interrupt_main()
            break
        else:
            data = str(name) + str(" send:  ") + msg
            sock.send(data.encode())

def recv_msg():
    while True:
        try:
            data = sock.recv(4096)
        except Exception as e:
            print(e)
            _thread.interrupt_main()
            break

        if not data:
            print('Disconnected from chat-server')
            _thread.interrupt_main()
            break
        else:
            print(data.decode())

if __name__ == "__main__":

    print ("Enter type of chat {1 - privet chat, 2 - public chat, 0 - exit}:")
    type_chat = int(sys.stdin.readline())
    while not type_chat in [1,2,3]:
        print("Invalid param.Enter type of chat {1 - privet chat, 2 - public chat, 0 - exit}:")
        type_chat = int(sys.stdin.readline())

    if type_chat is 1:
        authorization = False
        client_list = []
        Port = 9091

        while not authorization:
            print("Enter your ID for privet chat {0 - exit}:  ")
            client = sys.stdin.readline()
            try:
                with open(sys.argv[1]) as file:
                    for line in file:
                        client_list.append(int(line.rstrip('\n')))
            except IOError as er:
                print('Can\'t open the "clients.txt" file Error: {}'.format(er))
            if int(client) in client_list:
                authorization = True
            else:
                print("You enter invalid ID. Please, enter new ID:  ")

        name = client.rstrip()

    elif type_chat is 2:
        print("Enter your name for public chat or your ID for privet chat:  ")
        client = sys.stdin.readline()
        Port = 9090
        while len(client) <= 1:
            print("You enter invalid name. Please, enter new name:  ")
            client = str(sys.stdin.readline())

        name = client.rstrip()

    elif type_chat is 0:
        sys.exit()

    sock = socket.socket()
    sock.connect(("127.0.0.1", Port))

    print("{}, Welcome to the Chat!".format(name))
    print("Connection to chat-server.")
    print("Please enter the message...(enter 'exit()' for exit from app)")

    _thread.start_new_thread(send_msg, ())
    _thread.start_new_thread(recv_msg, ())


    try:
        while True:
            continue
    except:
        sock.close()
