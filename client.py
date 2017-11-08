import socket
import sys
import _thread

def send_msg():
    while True:
        print("Enter message:  ")
        msg = sys.stdin.readline()
        if "exit()" in msg:
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

    # for opening privet chat, user must enter his ID.
    if type_chat is 1:
        authorization = False
        client_list = []

        while not authorization:
            print("Enter your ID for privet chat {0 - exit}:  ")
            client = sys.stdin.readline()

            sock = socket.socket()
            sock.connect(("127.0.0.1", 9091))
            sock.send(client.encode())
            data = sock.recv(4096)
            if data.decode() == "open":
                authorization = True
            else:
                print ("Inbalid ID.")

        name = client.rstrip()

    elif type_chat is 2:
        print("Enter your name for public chat or your ID for privet chat:  ")
        client = sys.stdin.readline()
        while len(client) <= 1:
            print("You enter invalid name. Please, enter new name:  ")
            client = str(sys.stdin.readline())

        name = client.rstrip()
        sock = socket.socket()
        sock.connect(("127.0.0.1", 9090))

    elif type_chat is 0:
        sys.exit()

    print("{}, Welcome to the Chat!".format(name))
    print("Connection to chat-server.")
    print("Please enter the message...(enter 'exit()' for exit from app)")

    _thread.start_new_thread(send_msg, ())
    _thread.start_new_thread(recv_msg, ())


    try:
        while True:
            continue
    except:
        _thread.exit()
        sock.close()
