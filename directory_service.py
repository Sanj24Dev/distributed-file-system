# directory service
import os
import csv      
from socket import *
import nodes


def check_file_mappings(client_msg, list_files):
	msg = client_msg.split('|')
	filename = msg[0]
	RW = msg[1]

	mappings = open("file_mappings.csv",'rt')        # open the .csv file storing the mappings
	reader = csv.DictReader(mappings, delimiter=',')    # read file as a csv file, taking values after commas
	# header = reader.fieldnames    	# skip header of csv file
	file_row = ""
	if list_files == True:
		for row in reader:
			user_filename = row['user_filename']
			file_row = file_row + user_filename +  "\n"		# append filename to return string
		return file_row	
	else:
		for row in reader:
			# use the dictionary reader to read the values of the cells at the current row
			user_filename = row['user_filename']
			primary_copy = row['primary']

			if user_filename == filename and RW == 'w':		# check if file inputted by the user exists	(eg. file123)
				print("WRITING")
				actual_filename = row['actual_filename']	# get actual filename (eg. file123.txt)
				server_addr = row['server_addr']			# get the file's file server IP address
				server_port = row['server_port']			# get the file's file server PORT number

				print("actual_filename: " + actual_filename)
				print("server_addr: " + server_addr)
				print("server_port: " + server_port)

				return actual_filename + "|" + server_addr + "|" + server_port	# return string with the information on the file

			elif user_filename == filename and RW == 'r' and primary_copy == 'no':
				print("READING")
				actual_filename = row['actual_filename']	# get actual filename (eg. file123.txt)
				server_addr = row['server_addr']			# get the file's file server IP address
				server_port = row['server_port']			# get the file's file server PORT number

				print("actual_filename: " + actual_filename)
				print("server_addr: " + server_addr)
				print("server_port: " + server_port)

				return actual_filename + "|" + server_addr + "|" + server_port	# return string with the information on the file	
	return None 	# if file does not exist return None

def main():
	serverPort = nodes.directory_PORT
	serverAddr = nodes.directory_IP
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind((serverAddr, serverPort))
	serverSocket.listen(10)
	print ('DIRECTORY SERVICE is up and ready to receive...')

	while 1:
		connectionSocket, addr = serverSocket.accept()

		response = ""
		recv_msg = connectionSocket.recv(1024)
		recv_msg = recv_msg.decode()

		# check the mappings for the file
		if "LIST" in recv_msg:
			response = check_file_mappings(recv_msg, True)
		else:
			response = check_file_mappings(recv_msg, False)

		if response is None:	
			response = "FILE_DOES_NOT_EXIST"
			print("RESPONSE: \n" + response)
			print("\n")
		else:							# for existance of file
			response = str(response)
			print("RESPONSE: \n" + response)
			print("\n")

		connectionSocket.send(response.encode())	# send the file information or non-existance message to the client
			
		connectionSocket.close()


if __name__ == "__main__":
	main()