import socket
import threading
import time

# ======= Init variables =========
PORT = 2210
SERVER_IP = '127.0.0.1'

separator = '<SEP>'

clients = set()


# ======= Functions =========
# Takes client_socket and client_address for arguments
def listen_for_clients(cs, ca):
	while True:
		try:
			message = cs.recv(1024)
			message = message.decode('utf-8')

			#message = message.replace(separator, ': ')

			if '/exit' in message:
				loc_time = time.localtime()
				print('[SERVER] client disconnected from: {} at: ({}:{}:{})'.format(ca, loc_time.tm_hour, loc_time.tm_min, loc_time.tm_sec))
				clients.remove(cs)
				break

			if '/clients' in message:
				print('[SERVER] client {} checking status.'.format(cs))
				msg = '[SERVER] current clients: {}'.format(len(clients))
				cs.send(msg.encode('utf-8'))

			for client in clients:
				if client != cs:
					print('1')
					client.send(message.encode('utf-8'))
		
		except ConnectionResetError:
			loc_time = time.localtime()
			print('[SERVER] client disconnected from: {} at: ({}:{}:{})'.format(ca, loc_time.tm_hour, loc_time.tm_min, loc_time.tm_sec))
			clients.remove(cs)
			break

		# if '/exit' in message:
		# 	print('[SERVER] client disconnected from: {}'.format(cs))
		# 	clients.remove(cs)

		# for client in clients:
		# 	if client != cs:
		# 		client.send(message.encode('utf-8'))


# ======= Start a server ==========
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, PORT))

# ======= Listen for connection =========
server_socket.listen(1)
print('[SERVER] listening on {}'.format(server_socket.getsockname()))

while True:
	client_socket, client_address = server_socket.accept()
	loc_time = time.localtime()

	print('[SERVER] client connected from: {} at: ({}:{}:{})'.format(client_address, loc_time.tm_hour, loc_time.tm_min, loc_time.tm_sec))

	clients.add(client_socket)

	thread = threading.Thread(target=listen_for_clients, args=(client_socket, client_address))
	thread.daemon = True
	thread.start()


for client in clients:
	client.close()

server_socket.close()