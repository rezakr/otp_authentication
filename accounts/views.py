from rest_auth.views import LoginView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, OTPSerializer, OTPRequestSerializer

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	lookup_field = 'username'
	permission_classes = (IsAuthenticated,)


# Create your views here.
class OTPLoginView(LoginView):
	serializer_class = OTPSerializer
	pass


class OTPRequestView(GenericAPIView):
	serializer_class = OTPRequestSerializer

	def post(self, request, *args, **kwargs):
		self.request = request
		self.serializer = self.get_serializer(
			data=self.request.data, context={'request': request})
		self.serializer.is_valid(raise_exception=True)

		# TODO: Add a time so that it doesn't be spammed for token
		response = self.serializer.send_token()

		if self.serializer.validated_data['new_user']:
			status_code = status.HTTP_201_CREATED
		else:
			status_code = status.HTTP_200_OK

		return Response(response, status=status_code)
