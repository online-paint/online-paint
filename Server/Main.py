from multiprocessing import Process, Pipe
from threading import Thread
import socket
from PaintAppInstance import paint_app_instance


def handle_client(client_socket, client_address):
    print(f"Handling connection from {client_address}")

    parent_conn, child_conn = Pipe()

    kivy_process = Process(target=paint_app_instance, args=(child_conn,))
    kivy_process.start()

    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8")

        parent_conn.send(request)

        if request.lower() == "close":
            client_socket.send("closed".encode("utf-8"))
            break
        response = "accepted".encode("utf-8")
        client_socket.send(response)

        print(f"Received: {request} from {client_address}")


    client_socket.close()
    print(f"Connection to client {client_address} closed")

    kivy_process.join()


def server_listener():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "172.20.10.11"
    port = 8000

    server.bind((server_ip, port))
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")

    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        client_thread = Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    server_listener()
