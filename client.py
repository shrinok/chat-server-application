import socket
import threading

host = '127.0.0.1'
port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            break

def send_messages():
    while True:
        message = input("Enter your message (recipient:message): ")
        if message.lower() == 'exit':
            client_socket.send(message.encode('utf-8'))
            break
        client_socket.send(message.encode('utf-8'))

client_name = input("Enter your name: ")
client_socket.send(client_name.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()
