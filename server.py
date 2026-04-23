import socket
import threading


HOST = "0.0.0.0"

while True:
	try:
		PORT = int(input("Enter TCP port to start server on: ").strip())
		if 1024 <= PORT <= 65535:
			print(f"=== USING PORT {PORT} ===")
			break
		else:
			print("Invalid input. Enter a valid TCP port between 1024 and 65535")
	except ValueError:
		print("Invalid input. Enter a valid TCP port")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"=== SERVER RUNNING ON {HOST} : {PORT} ===")
print("=== TYPE \"ABORT\" TO CLOSE CONNECTION ===")

def receive(connection, nicknameClient, CONNECTION_ACTIVE):
	while CONNECTION_ACTIVE[0]:
		try:
			data = connection.recv(1024)
			if not data:
				print(f"\n=== CLIENT {address[0]} ({nicknameClient}) DISCONNECTED ===")
				print("=== TERMINATING CONNECTION ===")
				CONNECTION_ACTIVE[0] = False
				break
			
			messageClient = data.decode()
			print(f"\r{nicknameClient}: {messageClient}\nSERVER: ", end = "", flush = True)
		
		except Exception as exceptionReceive:
			print("=== RECEPTION ERROR ===")
			print(f"{type(exceptionReceive)}: {exceptionReceive}")
			CONNECTION_ACTIVE[0] = False
			break

def send(connection, CONNECTION_ACTIVE):
	while CONNECTION_ACTIVE[0]:
		try:
			messageServer = input("SERVER: ")
			
			if not messageServer.strip():
				print("Invalid input. Enter a message\n")
			
			else:
				connection.sendall(messageServer.encode())
				
				if messageServer == "ABORT":
					print("=== SERVER DISCONNECTED ===")
					print("=== TERMINATING CONNECTION ===")
					connection.sendall("=== SERVER DISCONNECTED ===\n=== TERMINATING CONNECTION ===".encode())
					CONNECTION_ACTIVE[0] = False
					break
		
		except Exception as exceptionSend:
			print("=== SENDING ERROR ===")
			print(f"{type(exceptionSend)}: {exceptionSend}")
			CONNECTION_ACTIVE[0] = False
			break

while True:
	try:
		connection, address = server.accept()
		
		print(f"=== CONNECTION FROM {address[0]} ===")
		
		nicknameClient = connection.recv(1024).decode()
		print(f"=== {address[0]} IDENTIFIED AS {nicknameClient} ===")
		
		CONNECTION_ACTIVE = [True]
		
		threadReceive = threading.Thread(target = receive, args = (connection, nicknameClient, CONNECTION_ACTIVE))
		threadSend = threading.Thread(target = send, args = (connection, CONNECTION_ACTIVE))
		
		threadReceive.start()
		threadSend.start()
		
		threadReceive.join()
		threadSend.join()
	
	except Exception as runtimeException:
		print("=== RUNTIME ERROR ===")
		print(f"{type(runtimeException)}: {runtimeException}")
	
	finally:
		connection.close()
		connection = None
		continue