from socket import *
from collections import defaultdict		# for dictionary list 
import sys
import nodes

def check_if_unlocked(filename, lock_map):
	if filename in lock_map:		# check for existance of filename as a key in the dictionary
		if lock_map[filename] == "unlocked":
			return True
		else:
			return False
	else:
		lock_map[filename] = "unlocked"
		return True

def main():

	serverAddr = nodes.lockingserver_IP
	serverPort = nodes.lockingserver_PORT
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind((serverAddr, serverPort))
	serverSocket.listen(10)
	print ('LOCKING SERVICE is up and ready to receive...')

	lock_map = {}
	client_queue = defaultdict(list)
	waiting_client = False
	client_timeout_map = {}


	while 1:
		connectionSocket, addr = serverSocket.accept()
		recv_msg = connectionSocket.recv(1024)
		recv_msg = recv_msg.decode()

		print("\nRECEIVED: " + recv_msg )

		if "_1_:" in recv_msg:
			msg = recv_msg.split("_1_:")
			client_id = msg[0]
			filename = msg[1]
			waiting_client = False


			unlocked = check_if_unlocked(filename, lock_map)
			if unlocked == True:
				count_temp = 0		# a count to check if current client is first in the queue

				if len(client_queue[filename]) == 0:	# if no clients currently waiting on the file
					lock_map[filename] = "locked"	# lock the file
					grant_message = "file_granted"
					print("SENT: " + grant_message + " ---- " + client_id)
					connectionSocket.send(grant_message.encode())	# send the grant message

				elif filename in client_queue:			
					for filename,values in client_queue.items():	# find the current file in the map
						for v in values:									# iterate though the clients waiting on this file
							if v == client_id and count_temp == 0:			# if the client is the first client waiting
								client_queue[filename].remove(v)	# remove it from the waiting list
								lock_map[filename] = "locked"	# lock the file
								grant_message = "file_granted"			
								print("SENT: " + grant_message +" ---- " + client_id)	
								connectionSocket.send(grant_message.encode())	# send the grant message
							count_temp += 1

			else:				# if the file is locked
				grant_message = "file_not_granted"

				if client_id in client_timeout_map:		# check if first time requesting file
					client_timeout_map[client_id] = client_timeout_map[client_id] + 1		# if first time, set timeout value to 0
					print("TIME: " + str(client_timeout_map[client_id]))
				else:
					client_timeout_map[client_id] = 0	# if not first time, increment timeout value of client


				if client_timeout_map[client_id] == 100:	# if client polled 100 times (10 sec), send timeout
					timeout_msg = "TIMEOUT"
					for filename,values in client_queue.items():	# find the current file in the map
						for v in values:									# iterate though the clients waiting on this file 
							if v == client_id:		# if the client is the first client waiting
								client_queue[filename].remove(v)	# remove it from the waiting list
					del client_timeout_map[client_id]			# remove client from timeout map
					connectionSocket.send(timeout_msg.encode())	# send timeout msg
				else:
					if filename in client_queue:						
						for filename,values in client_queue.items():	# find the current file in the map
							for v in values:							# iterate though the clients waiting on this file 
								if v == client_id:					# check if client is already waiting on the file
									waiting_client = True			# if already waiting, set flag - so client is not added to waiting list multiple times for the file 
					
					if waiting_client == False:			# if not already waiting
						client_queue[filename].append(client_id)	# append client to lists of clients waiting for the file

					print("SENT: " + grant_message + client_id)
					connectionSocket.send(grant_message.encode())	# send file not granted message

		elif "_2_:" in recv_msg:		# if unlock message (_2_) received 
			msg = recv_msg.split("_2_:")
			client_id = msg[0]
			filename = msg[1]

			lock_map[filename] = "unlocked"		# unlock the current file
			grant_message = "File unlocked..."
			connectionSocket.send(grant_message.encode())	# tell the current client that the file was unlocked

		connectionSocket.close()



if __name__ == "__main__":
	main()