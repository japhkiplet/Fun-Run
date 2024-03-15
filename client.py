import socket

def main():
    host = '127.0.0.1'
    port = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        command = input("Enter command (RECOMMEND or REGISTER): ").upper()
        if command == 'QUIT':
            break

        client_socket.send(command.encode('utf-8'))

        response = client_socket.recv(4096).decode('utf-8')
        print(response)

    client_socket.close()

if __name__ == "__main__":
    main()
