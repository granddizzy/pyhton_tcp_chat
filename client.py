import socket
import sys
import threading

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(('lepihov.by', 55555))
except:
    print("Couldn't connect to the server")
    sys.exit()

# Choosing Nickname
nickname = None


# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('utf-8')

            if not message:
                continue

            arr = message.split("|")
            if arr[0]:
                print(arr[0] + ": " + arr[1])
            else:
                print(arr[1])
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


def write():
    while True:
        message = input('').replace("|", "")

        arr = message.split(":")
        if len(arr) > 1:
            message = arr[0] + "|" + arr[1]
        else:
            message = "|" + arr[0]

        try:
            client.send(message.encode('utf-8'))
        except:
            print("An error occured!")
            break


def input_nickname():
    global nickname
    while True:
        nickname = input("Choose your nickname: ")
        try:
            client.send(nickname.encode('utf-8'))
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK_OK':
                break
            else:
                print("There's already a nickname like that in the chat")
                nickname = None
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break


input_nickname()

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
