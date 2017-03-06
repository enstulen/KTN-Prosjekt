# -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
	"""
	This is the chat client class
	"""
	host = ""
	server_port = 9998
	possible_requests_with_content = ["login", "msg"]
	possible_requests_without_content = ["logout", "names", "help"]

	def __init__(self, host, server_port):
		"""
		This method is run when creating a new Client object
		"""

		# Set up the socket connection to the server
		print("Welcome to this chat thing")
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = host
		self.server_port = server_port
		self.message_parser = MessageParser()
		self.message_reciever = MessageReceiver(self, self.connection)

		self.run()
		while True:
			text_input = input("")
			input_array = text_input.split(" ")
			first_word = input_array[0]
			if first_word in self.possible_requests_with_content:
				rest_of_string = text_input.split(None, 1)[1]
				json_object = self.createJSON(first_word, rest_of_string)
				self.send_payload(json_object)
			elif first_word in self.possible_requests_without_content:
				json_object = self.createJSON(first_word, None)
				self.send_payload(json_object)
			else:
				print("Error, not a valid request")

	def run(self):
		# Initiate the connection to the server
		self.connection.connect((self.host, self.server_port))
		self.message_reciever.start()

	def disconnect(self):
		self.connection.close()

	def receive_message(self, message):
		parsed_message = self.message_parser.parse(message)
		print(parsed_message)

	def send_payload(self, data):
		self.connection.send(data.encode())

	def createJSON(self, request, content):
		dict = {"request": request, "content": content}
		json_object = json.dumps(dict)
		return json_object


if __name__ == '__main__':
	"""
	This is the main method and is executed when you type "python Client.py"
	in your terminal.

	No alterations are necessary
	"""
	client = Client('localhost', 9998)
