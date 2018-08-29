# from .models import Token
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from django.urls import reverse
from .models import Token
from datetime import timedelta


class OTPAccessTestCase(APITestCase):
	def setUp(self):
		self.url = reverse('accounts:user_list')
		self.user = User.objects.get_or_create(
			username='989112224444')

	def test_access_page(self):
		valid_information = {'phone': '989112224444', 'code': 4444}
		response = self.client.post(reverse('accounts:otp_login'), valid_information)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		token = response.json()['key']
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_no_access(self):
		header = {'Authorization': "Token sdfsdfs09vxc"}
		response = self.client.get(self.url, **header)
		self.assertFalse(response.status_code == status.HTTP_200_OK)


class OTPExpirationTestCase(APITestCase):
	def setUp(self):
		self.url = reverse('accounts:otp_login')
		self.user = User.objects.get_or_create(
			username='989112224444')

	def test_token_expiration_after_30_days(self):
		valid_information = {'phone': '989112224444', 'code': 4444}
		response = self.client.post(self.url, valid_information)
		key = response.json()['key']
		key_token = Token.objects.filter(key=key).first()
		self.assertEqual(key_token.user.username, valid_information['phone'])
		key_token.expiration_time -= timedelta(days=30, seconds=1)
		key_token.created -= timedelta(days=30, seconds=1)
		key_token.save()

		self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
		response = self.client.get(reverse('accounts:user_list'))
		result = response.json()
		self.assertEqual(
			result['detail'], "This token has expired!",
			_('Token should expire after 30 days'))


class OTPLoginTestCase(APITestCase):
	def setUp(self):
		self.url = reverse('accounts:otp_login')
		self.user = User.objects.get_or_create(
			username='989112224444')

	def test_with_valid_phone_n_code(self):
		valid_information = {'phone': '989112224444', 'code': 4444}
		response = self.client.post(self.url, valid_information)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_wrong_combination(self):
		wrong_combination = {'phone': '989112224444', 'code': 1111}
		response = self.client.post(self.url, wrong_combination)
		self.assertFalse(response.status_code == status.HTTP_200_OK)

	def test_phone_doesnt_exist(self):
		user_doesnt_exist = {'phone': '989112224445', 'code': 4445}
		response = self.client.post(self.url, user_doesnt_exist)
		self.assertFalse(response.status_code == status.HTTP_200_OK)

	def test_login_invalid_phone(self):
		response = self.client.post(
			self.url, {'phone': 'Unknown Phone', 'code': 4444})

		result = response.json()
		self.assertEqual(400, response.status_code)
		self.assertEqual(
			result['non_field_errors'][0],
			"Phone number should be 12 digits (with country code)")

	def test_invalid_code(self):
		invalid_information = {'phone': '989112224444', 'code': "asdasd"}

		response = self.client.post(
			self.url, invalid_information)

		result = response.json()

		self.assertEqual(400, response.status_code)
		self.assertEqual(
			result['non_field_errors'][0], "Code should be 4 digits")

	def test_token_creation_limit(self):
		valid_information = {'phone': '989112224444', 'code': 4444}
		response = self.client.post(self.url, valid_information)
		first_key = response.json()['key']
		response = self.client.post(self.url, valid_information)
		second_key = response.json()['key']

		self.assertEqual(first_key, second_key, _('No Creation limit for tokens'))

	def test_token_reuse_after_reauth(self):
		valid_information = {'phone': '989112224444', 'code': 4444}
		response = self.client.post(self.url, valid_information)
		first_key = response.json()['key']
		first_key_token = Token.objects.filter(key=first_key).first()
		self.assertEqual(first_key_token.user.username, valid_information['phone'])
		first_key_token.expiration_time -= timedelta(hours=1)
		first_key_token.created -= timedelta(hours=1)
		first_key_token.save()

		response = self.client.post(self.url, valid_information)
		second_key = response.json()['key']

		self.assertFalse(
			first_key == second_key, _('Two different keys should be issued'))

		self.client.credentials(HTTP_AUTHORIZATION='Token ' + first_key)
		response = self.client.get(reverse('accounts:user_list'))
		self.assertEqual(
			response.status_code, status.HTTP_200_OK,
			_('First token should still work'))


class OTPRequestTestCase(APITestCase):
	url = reverse("accounts:otp_request")

	def setUp(self):
		self.new_phone = "989112224445"
		self.phone = "989112224444"
		self.user = User.objects.get_or_create(username=self.phone)
		# self.user.save()
		# self.client = APIClient()

	def test_request_valid_phone(self):
		response = self.client.post(
			self.url, {'phone': self.phone})

		result = response.json()

		self.assertEqual(200, response.status_code)
		self.assertEqual(result['result'], "success")

	def test_request_invalid_phone(self):
		response = self.client.post(
			self.url, {'phone': 'Unknown Phone'})

		result = response.json()
		self.assertEqual(400, response.status_code)
		self.assertEqual(
			result['non_field_errors'][0],
			"Phone number should be 12 digits (with country code)")

	def test_registration_in_database(self):
		response = self.client.post(
			self.url, {'phone': self.new_phone})

		result = response.json()

		self.assertEqual(201, response.status_code)
		self.assertEqual(result['result'], "success")
