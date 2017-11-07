import socket
import select
import _thread
import sys

def listning_client(srv_sock,client_list):
    while True:
        read_sockets, write_sockets, error_sockets = select.select(client_list, [], [])

        for sock in read_sockets:

            if sock == srv_sock:
                clnt_sock, addr = srv_sock.accept()
                client_list.append(clnt_sock)
                print("Client {} connected".format(str(addr)))
            else:
                try:
                    data = sock.recv(4096)
                except:
                    print("Client {} lost".format(str(addr)))
                    sock.close()
                    client_list.remove(sock)
                    if len(client_list) == 1:
                        break
                    continue
                if data:
                    if data == "exit()":
                        print("Client {} disconnected".format(str(addr)))
                        sock.close()
                        client_list.remove(sock)
                    else:
                        for socket in client_list:
                            if socket != srv_sock and socket != sock:
                                socket.send(data)

def check_list_privat():
    while True:
        print("Enter tha action for list of client:\n"
              "{ 1 - print client to list, 2 - add client to list, 3 - delete client to list, 0 - exit}\n"
              "Action:")
        action = sys.stdin.readline()

        if (int(action)) is 0:
            print ("Exit()")
            _thread.interrupt_main()
            break

        elif (int(action)) is 1:
            try:
                print("Client:")
                with open(file_client) as file:
                    for line in file:
                        line = line.rstrip('\n')
                        print(line)
            except IOError as er:
                print('Can\'t open the "clients.txt" file Error: {}'.format(er))

        elif (int(action)) is 2:
            print("Enter new ID client:")
            new_ID = sys.stdin.readline()
            with open(file_client, 'a') as file:
                file.write(new_ID)

        elif (int(action)) is 3:
            try:
                print("Enter ID client to delete:")
                delete_ID = sys.stdin.readline()
                with open(file_client) as file:
                    clients = file.readlines()  # lines to keep
                with open(file_client, 'w') as file:
                    for id in clients:
                        if int(id) != int(delete_ID):
                            file.writelines(str(id))

            except IOError as er:
                print('Can\'t open the "clients.txt" file. Error: {}'.format(er))


if __name__ == "__main__":

    client_list_pub = []
    client_list_prv = []
    file_client = sys.argv[1]

    srv_sock_pub = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock_pub.bind(("127.0.0.1", 9090))
    srv_sock_pub.listen(100)
    client_list_pub.append(srv_sock_pub)

    srv_sock_prv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock_prv.bind(("127.0.0.1", 9091))
    srv_sock_prv.listen(100)
    client_list_prv.append(srv_sock_prv)

    print("Chat server if running...\n"
          "IP public= 127.0.0.1:9090\n"
          "IP privet= 127.0.0.1:9091")

    _thread.start_new_thread(check_list_privat, ())
    _thread.start_new_thread(listning_client, (srv_sock_pub, client_list_pub))
    _thread.start_new_thread(listning_client, (srv_sock_prv, client_list_prv))

    try:
        while True:
            continue
    except:
        srv_sock_prv.close()
        srv_sock_pub.close()

