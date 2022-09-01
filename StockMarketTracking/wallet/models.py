from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User


class Wallet(models.Model):
    """
    keeps track of money in users wallet.
    """

    user = models.OneToOneField(
        verbose_name=_("User"),
        to=User,
        on_delete=models.CASCADE,
        help_text=_("User"),
    )
    balance = models.FloatField(
        verbose_name=_("Balance"),
        default=0,
        help_text=_("current balance of the user", )
    )

    def deposit(self, amount: float) -> float:
        """
        Deposit the given amount ot the wallet.

        :param amount: amount of money to deposit.
        :return: current balance.
        """

        self.balance += amount
        return self.balance

    def withdraw(self, amount: float):
        """
        Withdraw money from the account. If the account goes below 0, raises value error.

        :param amount: The amount to withdraw
        :return: current balance
        """

        final_balance = self.balance - amount

        if final_balance < 0:
            raise ValueError("Can't have balance less than 0.")

        self.balance = final_balance
        return self.balance

    def __str__(self):
        return str(self.balance)
