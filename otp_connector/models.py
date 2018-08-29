# A simple Connector to check the data
import logging
logger = logging.getLogger(__name__)


class OTPConnector(object):
	_tokens = None

	def __init__(self, data=None):
		self._tokens = {}
		# Data on how to connect to the device
		self.data = data

	def send_token(self, phone):
		try:
			# TODO: Call the device, log the followup code somewhere
			# self._tokens['phone'] = phone[-4:]
			pass
		except Exception as e:
			logger.error("Some error happened somewhere: {0}".format(e))
			# TODO: Handle the exception here if feasible.
			pass

		return "Use the last 4 digits of your phone"

	def verify_token(self, phone, code):
		# Call the device for verification
		if phone[-4:] == code:
			return True
		else:
			return False
