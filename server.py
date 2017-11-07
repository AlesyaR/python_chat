import socket
import select
import _thread
import sys

# listing client end resend data
def listning_client(srv_sock,client_list, privat=False):
    while True:
        read_sockets, write_sockets, error_sockets = select.select(client_list, [], [])

        for sock in read_sockets:

            # add new client in chat
            if sock == srv_sock:
                clnt_sock, addr = srv_sock.accept()

                # check id client for privet chat
                if privat:
                    list_id = []
                    # get list of Client's ID
                    try:
                        with open(file_client) as file:
                            for line in file:
                                list_id.append(int(line.rstrip('\n')))
                    except IOError as er:
                        print('Can\'t open the "clients.txt" file Error: {}'.format(er))

                    id = clnt_sock.recv(4096)
                    if int(id.decode()) in list_id:
                        # ID was found => open connection
                        clnt_sock.send("open".encode())
                        client_list.append(clnt_sock)
                    else:
                        # ID wasn't found => close connection
                        clnt_sock.send("close".encode())
                        clnt_sock.close()
                        continue
                else:
                    # chat is public => open connection
                    client_list.append(clnt_sock)
            else:
                try:
                    data = sock.recv(4096)
                except:
                    print("Client {} lost".format(str(addr)))
                    sock.close()
                    client_list.remove(sock)
                    continue
                if data:
                    if data == "exit()":
                        print("Client {} disconnected".format(str(addr)))
                        sock.close()
                        client_list.remove(sock)
                    else:
                        # send data to all clients excluding recover & srv
                        for socket in client_list:
                            if socket != srv_sock and socket != sock:
                                socket.send(data)

def check_list_privat():
    while True:
        print("Enter tha action for list of client:\n"
              "{ 1 - print client to list, 2 - add client to list, 3 - delete client to list, 0 - exit}\n"
              "Action:")
        action = sys.stdin.readline()

        # Exit ()
        if (int(action)) is 0:
            print ("Exit()")
            _thread.interrupt_main()
            break

        # print all Client's ID
        elif (int(action)) is 1:
            try:
                print("Client:")
                with open(file_client) as file:
                    for line in file:
                        line = line.rstrip('\n')
                        print(line)
            except IOError as er:
                print('Can\'t open the "clients.txt" file Error: {}'.format(er))

        # Add new Client ID in list of clients
        elif (int(action)) is 2:
            print("Enter new ID client:")
            new_ID = sys.stdin.readline()
            with open(file_client, 'a') as file:
                file.write(new_ID)

        # Delete new Client ID in list of clients
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

    # create socket for public chat
    srv_sock_pub = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock_pub.bind(("127.0.0.1", 9090))
    srv_sock_pub.listen(100)
    client_list_pub.append(srv_sock_pub)

    # create socket for privet chat
    srv_sock_prv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock_prv.bind(("127.0.0.1", 9091))
    srv_sock_prv.listen(100)
    client_list_prv.append(srv_sock_prv)

    print("Chat server if running...\n"
          "IP public= 127.0.0.1:9090\n"
          "IP privet= 127.0.0.1:9091")

    _thread.start_new_thread(check_list_privat, ())
    _thread.start_new_thread(listning_client, (srv_sock_pub, client_list_pub))
    _thread.start_new_thread(listning_client, (srv_sock_prv, client_list_prv, True))

    try:
        while True:
            continue
    except:
        srv_sock_prv.close()
        srv_sock_pub.close()

