from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from datetime import timedelta
import rest_framework.authtoken.models
import logging
logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Token(rest_framework.authtoken.models.Token):
	# key is no longer primary key, but still indexed and unique
	key = models.CharField(_("Key"), max_length=40, db_index=True, unique=True)

	# relation to user is a ForeignKey, so each user can have more than one token
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, related_name='auth_tokens',
		on_delete=models.CASCADE, verbose_name=_("User")
	)

	expiration_time = models.DateTimeField(_("timestamp"))

	class Meta:
		unique_together = (('user', 'expiration_time'),)


def multiple_token_creator(token_model, user, serializer):
	expiration_time = timezone.now() + timedelta(days=30)
	# DO NOT create a new token if the previous one is only 5 seconds old!
	time_threshold = timezone.now() - timedelta(seconds=5)
	fresh_token = Token.objects.filter(
		user=user, created__gt=time_threshold).first()
	if fresh_token is None:
		logger.info("Creating a new token for user: {0}".format(user.username))
		token = token_model.objects.create(
			user=user, expiration_time=expiration_time)
	else:
		logger.info(
			"Not even 5 seconds has passed, ignoring token creation for {0}".format(
				user.username))
		token = fresh_token
	return token
