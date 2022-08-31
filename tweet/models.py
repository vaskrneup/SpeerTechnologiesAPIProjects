from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Tweet(models.Model):
    """
    Database table representation of tweet. Also, contains additional methods related to Tweet.
    """

    author = models.ForeignKey(
        verbose_name=_("Tweet Author"),
        to=get_user_model(),
        on_delete=models.CASCADE,
        help_text=_("Creator of tweet")
    )

    creation_datetime = models.DateTimeField(
        verbose_name=_("Creation Date"),
        help_text=_("Date posted"),
        auto_now_add=True
    )
    update_datetime = models.DateTimeField(
        verbose_name=_("Update Date"),
        help_text=_("Date updated"),
        auto_now=True,
    )

    tweet = models.TextField(
        verbose_name=_("Tweet"),
        max_length=281,
        help_text=_("Main content of the tweet"),
    )

    @property
    def striped_tweet(self):
        return self.tweet[:30]

    def __str__(self):
        return self.striped_tweet
