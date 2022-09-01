from django.db.models import Sum, F, FloatField
from rest_framework.generics import ListAPIView
from rest_framework.request import Request

from share_manager import models
from share_manager import serializer


class GetAllScrips(ListAPIView):
    """
    Gets the list of all stock, that a user can trade.
    """

    queryset = models.Share.objects.all()
    serializer_class = serializer.StockSerializer


class GetPortfolio(ListAPIView):
    """
    Gets the current portfolio of the user.
    """

    serializer_class = serializer.StockPortfolioSerializer

    def get_queryset(self):
        """
        Gets the queryset for the current state of user portfolio.

        :return: query for the portfolio of the user.
        """

        return models.Portfolio.objects.filter(
            user=self.request.user
        )

    def get(self, request: Request, *args, **kwargs):
        """
        Add total shares and total value to the response.

        :param request: Request object from client
        :param args: Arguments accepted by parent get
        :param kwargs: Keyword arguments accepted by parent get
        :return: updated list of holding
        """

        response = super(GetPortfolio, self).get(request, *args, **kwargs)
        portfolio_aggregate = self.get_queryset().aggregate(
            total_shares=Sum("number_of_shares"),
            total_value=Sum(
                F("number_of_shares") * F("share__current_price"),
                output_field=FloatField()
            )
        )

        response.data["total_shares"] = portfolio_aggregate.get("total_shares", 0)
        response.data["total_value"] = round(portfolio_aggregate.get("total_value", 0.00), 2)

        return response
