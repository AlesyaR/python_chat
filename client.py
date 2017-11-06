import socket
import sys
import thread

def send_msg():
    while True:
        print("Enter message:  ")
        msg = sys.stdin.readline()
        if "exit()" in msg:
            sock.send(msg)
            thread.interrupt_main()
            break
        else:
            sock.send(str(name) + str(" send:  ") + msg)

def recv_msg():
    while True:
        try:
            data = sock.recv(4096)
        except Exception as e:
            print(e)
            thread.interrupt_main()
            break

        if not data:
            print('Disconnected from chat-server')
            thread.interrupt_main()
            break
        else:
            print(data)

if __name__ == "__main__":

    print("Enter your name:  ")
    client = sys.stdin.readline()
    while len(client) <= 1:
        print("You enter invalid name. Please, enter new name:  ")
        client = str(sys.stdin.readline())

    name = client.rstrip()
    sock = socket.socket()
    sock.connect(("127.0.0.1", 9090))

    print("{}, Welcome to the Chat!".format(name))
    print("Connection to chat-server.")
    print("Please enter the message...(enter 'exit()' for exit from app)")

    thread.start_new_thread(send_msg, ())
    thread.start_new_thread(recv_msg, ())

    try:
        while True:
            continue
    except:
        sock.close()
