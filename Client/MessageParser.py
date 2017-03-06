import json

class MessageParser():
	def __init__(self):

		self.possible_responses = {
			'error': self.parse_error,
			'info': self.parse_info,
			'message': self.parse_message,
			'history': self.parse_history
		}

	def parse(self, payload):
		payload = json.loads(payload.decode())

		if payload['response'] in self.possible_responses:
			return self.possible_responses[payload['response']](payload)
		else:
			return 'response not valid'# Response not valid

	def parse_error(self, payload):
		return "[%s] Error: %s" % (payload['timestamp'], payload['content'])

	def parse_info(self, payload):
		return "[%s] Info: %s" % (payload['timestamp'], payload['content'])

	def parse_message(self, payload):
		return "[%s] Message: %s" % (payload['timestamp'], payload['content'])

	def parse_history(self, payload):
		print('parse history')

