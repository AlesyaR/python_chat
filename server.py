import socket
import select
import sys



if __name__ == "__main__":
    
    client_list = []
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock.bind(("127.0.0.1", 9090))
    srv_sock.listen(100)
    client_list.append(srv_sock)

    print("Chat server if running...IP = 127.0.0.1:9090")

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

    srv_sock.close()
