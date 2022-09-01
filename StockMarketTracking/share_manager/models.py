import random

from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User


class Share(models.Model):
    """
    Models the value of share.
    """

    last_updated = models.DateTimeField(
        verbose_name=_("Price Last Updated"),
        auto_now=True,
        help_text=_("Last time, when the price was updated.")
    )
    stock_scrip = models.CharField(
        verbose_name=_("Stock Scrip"),
        max_length=16,
        help_text=_("Symbol of the stock")
    )
    current_price = models.FloatField(
        verbose_name=_("Current Price"),
        help_text=_("Current price of the share."),
    )

    # !! This is just for demo !!
    # To create random values for the stock price!!
    def set_random_value(self):
        self.current_price = random.randint(1000, 20000) / 100

    def save(self, *args, **kwargs):
        self.current_price = round(self.current_price, 2)

        return super(Share, self).save(*args, **kwargs)

    def __str__(self):
        return self.stock_scrip


class Portfolio(models.Model):
    """
    Keeps track of users' portfolio.
    """

    user = models.ForeignKey(
        verbose_name=_("User"),
        to=User,
        on_delete=models.CASCADE,
        help_text=_("Owner of the share.")
    )
    share = models.ForeignKey(
        verbose_name=_("Share"),
        to=Share,
        on_delete=models.CASCADE,
        help_text=_("Share holding detail.")
    )
    number_of_shares = models.IntegerField(
        verbose_name=_("Number of shares"),
        default=0,
        help_text=_("Number of shares that user have."),
    )

    @property
    def total_holding(self):
        return round(self.share.current_price * self.number_of_shares, 2)

    def __str__(self):
        return self.share.stock_scrip
