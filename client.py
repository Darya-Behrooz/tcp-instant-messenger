import socket
import threading
import ipaddress
# import re


# while True:
#     SERVER_IPV4 = input("Enter server IPv4 address: ").strip()
#     validIPV4regex = r"^(?!0\.0\.0\.0$)(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])$"
#     if re.fullmatch(validIPV4regex, SERVER_IPV4):
#         print(f"=== CONNECTING TO {SERVER_IPV4} ===")
#         break
#     else:
#         print("Invalid input. Enter a valid IPv4 address")

while True:
    SERVER_IPV4 = input("Enter server IPv4 address: ").strip()
    try:
        ipaddress.IPv4Address(SERVER_IPV4)
        print(f"=== CONNECTING TO {SERVER_IPV4} ===")
        break
    except ipaddress.AddressValueError:
        print("Invalid input. Enter a valid IPv4 address")

while True:
    try:
        PORT = int(input("Enter server TCP port: ").strip())
        if 1024 <= PORT <= 65535:
            print(f"=== USING PORT {PORT} ===")
            break
        else:
            print("Invalid input. Enter a valid TCP port between 1024 and 65535")
    except ValueError:
        print("Invalid input. Enter a valid TCP port")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IPV4, PORT))

print(f"=== CONNECTED TO SERVER AT {SERVER_IPV4} : {PORT} ===")
print("=== TYPE \"ABORT\" TO CLOSE CONNECTION ===")

def receive(client, CONNECTION_ACTIVE):
    ACK = True
    while CONNECTION_ACTIVE[0]:
        try:
            data = client.recv(1024)
            if not data:
                print(f"\n=== SERVER DISCONNECTED ===")
                print("=== TERMINATING CONNECTION ===")
                CONNECTION_ACTIVE[0] = False
                break
            
            messageServer = data.decode()
            
            if ACK:
                print(f"\rSERVER: {messageServer}")
                ACK = False
            else:
                print(f"\rSERVER: {messageServer}\n{nicknameClient}: ", end = "", flush = True)
        
        except Exception as exceptionReceive:
            print("=== RECEPTION ERROR ===")
            print(f"{type(exceptionReceive)}: {exceptionReceive}")
            CONNECTION_ACTIVE[0] = False
            break

def send(client, nicknameClient, CONNECTION_ACTIVE):
    while CONNECTION_ACTIVE[0]:
        try:
            messageClient = input(f"{nicknameClient}: ")
            
            if not messageClient.strip():
                print("Invalid input. Enter a message\n")
            
            else:
                client.sendall(messageClient.encode())
                
                if messageClient == "ABORT":
                    print(f"=== {nicknameClient} DISCONNECTED ===")
                    print("=== TERMINATING CONNECTION ===")
                    client.sendall(f"=== {nicknameClient} DISCONNECTED ===\n=== TERMINATING CONNECTION ===".encode())
                    CONNECTION_ACTIVE[0] = False
                    break
        
        except Exception as exceptionSend:
            print("=== SENDING ERROR ===")
            print(f"{type(exceptionSend)}: {exceptionSend}")
            CONNECTION_ACTIVE[0] = False
            break

while True:
    try:
        nicknameClient = input("Enter a nickname or press [Enter] to remain anonymous: ").strip()
        if not nicknameClient:
            nicknameClient = "CLIENT"
        client.sendall(nicknameClient.encode())
        
        CONNECTION_ACTIVE = [True]

        threadReceive = threading.Thread(target = receive, args = (client, CONNECTION_ACTIVE))
        threadSend = threading.Thread(target = send, args = (client, nicknameClient, CONNECTION_ACTIVE))

        threadReceive.start()
        threadSend.start()

        threadReceive.join()
        threadSend.join()
    
    except Exception as runtimeException:
        print("=== RUNTIME ERROR ===")
        print(f"{type(runtimeException)}: {runtimeException}")
    
    finally:
        client.close()
        client = None
        break