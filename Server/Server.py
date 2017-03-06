# -*- coding: utf-8 -*-
import socketserver
import json
import time
import datetime

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

class ClientHandler(socketserver.BaseRequestHandler):
	"""
	This is the ClientHandler class. Everytime a new client connects to the
	server, a new ClientHandler object will be created. This class represents
	only connected clients, and not the server itself. If you want to write
	logic for the server, you must write it outside this class
	"""
	help_text = "Available commands are: login <username>, logout, help, message <user>, names"
	clients = {}
	logged_in_usernames = []

	def handle(self):
		"""
		This method handles the connection between a client and the server.
		"""
		self.possible_requests = {
			'login': self.handle_login,
			'logout': self.handle_logout,
			'help': self.handle_help,
			'message': self.handle_message,
			'names': self.handle_names,
		}

		self.ip = self.client_address[0]
		self.port = self.client_address[1]
		self.connection = self.request

		# Loop that listens for messages from the client
		while True:
			received_string = self.connection.recv(4096)
			print(received_string)
			content = json.loads(received_string.decode())["content"]
			request = json.loads(received_string.decode())["request"]
			print(content)
			print(request)

			if request in self.possible_requests:
				if request == 'login' or request == 'message':
					self.possible_requests[request](content)
				elif request == 'logout' or request == 'help' or request == 'names':
					self.possible_requests[request](self)


	def handle_login(self, username):
		if username in self.logged_in_usernames:
			self.create_and_send_response("server", "error", "Username already taken.")
		else:
			self.logged_in_usernames.append(username)
			self.clients.update({username: self.connection})
			self.create_and_send_response("server", "info", "%s Logged in" % (username))
			self.username = username


	def handle_logout(self):
		print("handle logout")

	def handle_help(self):
		self.create_and_send_response("server", "info", self.help_text)

	def handle_message(self, message):
		print("handle message")

	def handle_names(self):
		print("handle names")

	def create_timestamp(self):
		time_stamp = time.time()
		return datetime.datetime.fromtimestamp(time_stamp).strftime('%d-%m-%Y %H:%M:%S')

	def create_response(self, sender, response_type, content):
		response = {
			'timestamp': self.create_timestamp(),
			'sender': None,
			'response': None,
			'content': None,
		}
		response['sender'] = sender
		response['response'] = response_type
		response['content'] = content
		return response

	def send_response(self, response):
		json_object = json.dumps(response)
		self.connection.send(json_object.encode())

	def create_and_send_response(self, sender, response_type, content):
		response = self.create_response(sender, response_type, content)
		self.send_response(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	"""
	This class is present so that each client connected will be ran as a own
	thread. In that way, all clients will be served by the server.

	No alterations are necessary
	"""
	allow_reuse_address = True

if __name__ == "__main__":
	"""
	This is the main method and is executed when you type "python Server.py"
	in your terminal.

	No alterations are necessary
	"""
	HOST, PORT = 'localhost', 9998
	print ('Server running...')

	# Set up and initiate the TCP server
	server = ThreadedTCPServer((HOST, PORT), ClientHandler)
	server.serve_forever()
