from django.urls import path
from .views import UserViewSet, OTPLoginView, OTPRequestView

user_list = UserViewSet.as_view({
	'get': 'list',
})

app_name = "accounts"

urlpatterns = [
	path('users/', user_list, name='user_list'),
	path('login/', OTPLoginView.as_view(), name='otp_login'),
	path('otp-request/', OTPRequestView.as_view(), name='otp_request'),
]
