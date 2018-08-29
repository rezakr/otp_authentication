import rest_framework.authentication
from rest_framework import exceptions
from .models import Token
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import logging
logger = logging.getLogger(__name__)


class TokenAuthentication(rest_framework.authentication.TokenAuthentication):
	model = Token

	def authenticate_credentials(self, key):
		data = super().authenticate_credentials(key)
		expiration_time = data[1].expiration_time
		current_time = timezone.now()
		if current_time > expiration_time:
			logger.debug('The expiration time on \"{0}\" has long passed!'.format(key))
			msg = _('This token has expired!')
			raise exceptions.AuthenticationFailed(msg)
		return data
