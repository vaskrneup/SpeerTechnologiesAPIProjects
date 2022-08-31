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

    like_count = models.BigIntegerField(
        verbose_name=_("Like Count"),
        help_text=_("Keeps track for number of likes made to the tweet."),
        default=0,
    )
    retweet_count = models.BigIntegerField(
        verbose_name=_("Retweet Count"),
        help_text=_("Keeps track of how many retweets had been made."),
        default=0,
    )

    retweet = models.ForeignKey(
        verbose_name=_("Retweet"),
        to="tweet.Tweet",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        help_text=_("Determines if this tweet is a repost."),
        related_name="tweet_retweet",
    )
    thread = models.ForeignKey(
        verbose_name=_("Thread"),
        to="tweet.Tweet",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        help_text=_("Determines if this tweet is a part of a thread."),
        related_name="tweet_thread",
    )

    @property
    def striped_tweet(self):
        """
        Simply returns the first 30 characters of the tweet.
        """

        return f"{self.tweet[:30]}..." if len(self.tweet) > 30 else self.tweet

    def __str__(self):
        return self.striped_tweet


class Like(models.Model):
    """
    Keeps track of tweet liked by the user.
    """

    creation_datetime = models.DateTimeField(
        verbose_name=_("Creation Date"),
        help_text=_("Date posted"),
        auto_now_add=True
    )

    author = models.ForeignKey(
        verbose_name=_("Liked By"),
        to=get_user_model(),
        on_delete=models.CASCADE,
        help_text=_("Liker of a tweet")
    )
    tweet = models.ForeignKey(
        verbose_name=_("Liked Tweet"),
        to=Tweet,
        on_delete=models.CASCADE,
        help_text=_("Tweet that was liked")
    )


class Retweet(models.Model):
    """
    Keeps track of retweet done by the user.
    """

    creation_datetime = models.DateTimeField(
        verbose_name=_("Creation Date"),
        help_text=_("Date posted"),
        auto_now_add=True
    )

    author = models.ForeignKey(
        verbose_name=_("Retweeted By"),
        to=get_user_model(),
        on_delete=models.CASCADE,
        help_text=_("One who retweeted")
    )
    tweet = models.ForeignKey(
        verbose_name=_("Retweeted Tweet"),
        to=Tweet,
        on_delete=models.CASCADE,
        help_text=_("The tweet that was retweeted"),
        related_name="retweet_tweet"
    )
