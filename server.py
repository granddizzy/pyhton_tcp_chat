import socket
import threading

host = '192.168.1.98'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = {}

# Sending Messages To All Connected Clients
def broadcast(message, nickname):
    for nickname_recipient in clients:
        if nickname_recipient == nickname:
            continue

        clients[nickname_recipient].send((nickname + "|" + message).encode("utf-8"))


def unicast(message, nickname_recipient, nickname):
    clients[nickname_recipient].send((nickname + "|" + message).encode("utf-8"))


# Handling Messages From Clients
def handle(nickname):
    global nickname_recipient, message
    while True:
        try:
            data = clients[nickname].recv(1024)
            msg = data.decode('utf-8')
            arr = msg.split("|")

            if len(arr) > 1:
                nickname_recipient, message = arr[0], arr[1]

            if nickname_recipient:
                if nickname_recipient in clients:
                    unicast(message, nickname_recipient, nickname)
                else:
                    unicast("There's no such nickname in the chat", nickname, "")
            else:
                broadcast(message, nickname)
        except:
            # Removing And Closing Clients
            clients[nickname].close()
            del clients[nickname]
            broadcast('{} left!'.format(nickname), "")
            print("Disconnected " + nickname)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        while True:
            nickname = client.recv(1024).decode('utf-8')
            if nickname not in clients:
                clients[nickname] = client
                client.send('NICK_OK'.encode('utf-8'))
                break
            else:
                client.send('NICK_ERROR'.encode('utf-8'))

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname), "")
        broadcast("{} joined!".format(nickname), "")
        client.send('Connected to server!'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(nickname,))
        thread.start()


print("Server if listening...")
receive()
