from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
from django.utils.translation import ugettext_lazy as _
import re
from otp_connector.models import OTPConnector
import logging
logger = logging.getLogger(__name__)


class UserSerializer(serializers.Serializer):
	class Meta:
		model = User
		fields = ('username', 'email', 'is_staff')


class OTPRequestSerializer(serializers.Serializer):
	phone = serializers.CharField(
		required=True, allow_blank=True)

	def _validate_phone(self, attrs):
		phone = attrs.get('phone', '').lower()
		phone_re = re.compile(r'\d{12}$')
		if phone_re.match(phone) is None:
			msg = _('Phone number should be 12 digits (with country code)')
			raise serializers.ValidationError(msg)
		return phone

	def validate(self, attrs):
		phone = self._validate_phone(attrs)
		user = User.objects.filter(username=phone).first()
		attrs['new_user'] = False
		if user is None:
			logger.info("A new user {0} has been created!".format(phone))
			user = User.objects.create(username=phone)
			attrs['new_user'] = True

		attrs['user'] = user
		return attrs

	def send_token(self):
		try:
			connector = OTPConnector()
			result = connector.send_token(self.data['phone'])
			logger.debug("SMS connector result for {0} is {1}".format(
				self.data['phone'], result))
		except Exception as e:
			raise exceptions.ValidationError(
				'problem with SMS service, please try again later')
		return {'result': 'success'}


class OTPSerializer(serializers.Serializer):
	phone = serializers.CharField(
		required=True, allow_blank=True)
	code = serializers.CharField(
		style={'input_type': 'password'}, required=False)

	def _validate_phone(self, attrs):
		phone = attrs.get('phone', '').lower()
		phone_re = re.compile(r'\d{12}$')

		if phone_re.match(phone) is None:
			msg = _('Phone number should be 12 digits (with country code)')
			raise serializers.ValidationError(msg)
		return phone

	def _validate_code(self, attrs):
		code = attrs.get('code', None)
		code_re = re.compile(r'\d{4}$')

		if code_re.match(code) is None:
			msg = _('Code should be 4 digits')
			raise serializers.ValidationError(msg)
		return code

	def _validate_user(self, phone, code):
		try:
			connector = OTPConnector()
			return connector.verify_token(phone, code)
		except Exception as e:
			logger.error("OTP Service failed for {0}/{1} combination".format(
				phone, code))

			raise exceptions.ValidationError(
				'problem with SMS service, please try again later')

	def validate(self, attrs):
		phone = self._validate_phone(attrs)
		code = self._validate_code(attrs)

		user = User.objects.filter(username=phone).first()

		if user is None:
			msg = _("User not registered in system!")
			raise exceptions.ValidationError(msg)

		if self._validate_user(phone, code) is False:
			logger.info("Failed to authenticate {0}".format(phone))
			msg = _("Could't Validate the combination provided")
			raise exceptions.ValidationError(msg)
		attrs['user'] = user
		return attrs
