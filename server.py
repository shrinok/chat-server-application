import socket
import threading

host = '127.0.0.1'
port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print('Server is listening...')

clients = []
client_names = {}  # Dictionary to store client names

def handle_client(client_socket, client_name):
    print(f"{client_name} connected")
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            
            if not message:
                print(f"{client_name} disconnected")
                break
            
            if message == 'exit':
                clients.remove(client_socket)
                del client_names[client_socket]  # Remove from the dictionary
                client_socket.close()
                print(f"{client_name} disconnected")
                break
            
            recipient, actual_message = message.split(':', 1)
            
            if client_name == recipient:
                print(f"{client_name}: {actual_message}")
            else:
                print(f"{client_name} to {recipient}: {actual_message}")
            
            for client in clients:
                if client != client_socket and client_names[client] == recipient:
                    client.send(f"{client_name}: {actual_message}".encode('utf-8'))
        except Exception as e:
            clients.remove(client_socket)
            del client_names[client_socket]  # Remove from the dictionary
            client_socket.close()
            print(f"{client_name} disconnected due to an error: {e}")
            break


while True:
    client_socket, client_address = server_socket.accept()
    print(f'Connected with {client_address}')
    
    client_name = client_socket.recv(1024).decode('utf-8')
    client_names[client_socket] = client_name
    
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_name))
    client_thread.start()
