from django.db.models import Sum, F, FloatField
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

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


class TradeShare(APIView):
    """
    Allows for the trading of scrips. Either Buy or Sell.
    """

    @staticmethod
    def _handle_scrip_buy(request: Request, scrip: models.Share, scrip_count: int):
        """
        Handles the buying of the scrip.

        :param request: Request from the client side
        :param scrip: Scrip object
        :param scrip_count: Number of scrip involved in transaction
        :return: response for the client
        """

        total_buy_price = scrip_count * scrip.current_price

        if request.user.wallet.balance < total_buy_price:
            return Response({
                "detail": "Not enough balance.",
                "current_balance": request.user.wallet.balance,
                "required_balance": total_buy_price
            }, status=status.HTTP_401_UNAUTHORIZED)

        if portfolio := models.Portfolio.objects.filter(
                user=request.user,
                share=scrip
        ).first():
            portfolio.number_of_shares += scrip_count
            portfolio.save()
        else:
            portfolio = models.Portfolio(
                user=request.user,
                share=scrip,
                number_of_shares=scrip_count
            )
            portfolio.save()

        request.user.wallet.withdraw(total_buy_price)
        request.user.wallet.save()

        return Response({
            "detail": f"Scrip({scrip}) purchase successful.",
            "current_balance": request.user.wallet.balance,
            "current_scrip_balance": portfolio.number_of_shares,
            "transaction_amount": total_buy_price,
        }, status=status.HTTP_200_OK)

    @staticmethod
    def _handle_scrip_sell(request: Request, scrip: models.Share, scrip_count: int):
        """
        Handles the selling of the scrip.

        :param request: Request from the client side
        :param scrip: Scrip object
        :param scrip_count: Number of scrip involved in transaction
        :return: response for the client
        """

        portfolio = models.Portfolio.objects.filter(user=request.user, share=scrip).first()
        total_sell_price = scrip_count * scrip.current_price

        if not portfolio:
            return Response({
                "detail": f"No scrip({scrip}) in portfolio",
            }, status=status.HTTP_401_UNAUTHORIZED)

        if portfolio.number_of_shares < scrip_count:
            return Response({
                "detail": "Not enough scrips.",
                "current_scrip_balance": portfolio.number_of_shares,
                "required_scrip_balance": scrip_count
            }, status=status.HTTP_401_UNAUTHORIZED)

        portfolio.number_of_shares -= scrip_count

        if portfolio.number_of_shares == 0:
            portfolio.delete()
        else:
            portfolio.save()

        request.user.wallet.deposit(total_sell_price)
        request.user.wallet.save()

        return Response({
            "detail": f"Scrip({scrip}) sell successful.",
            "current_balance": request.user.wallet.balance,
            "current_scrip_balance": portfolio.number_of_shares,
            "transaction_amount": total_sell_price,
        })

    def post(self, request: Request):
        """
        Handles the buying and selling of the scrip.

        :param request: Request from the client side
        :return: response for the client
        """

        trade_serializer = serializer.StockTradeViewSerializer(data=request.data)

        if trade_serializer.is_valid():
            transaction_type = trade_serializer.validated_data.get("transaction_type")
            scrip = get_object_or_404(models.Share, stock_scrip=trade_serializer.validated_data.get("scrip"))
            scrip_count = trade_serializer.validated_data.get("scrip_count")

            if transaction_type == "BUY":
                return self._handle_scrip_buy(request, scrip, scrip_count)
            elif transaction_type == "SELL":
                return self._handle_scrip_sell(request, scrip, scrip_count)

            return Response({
                "detail": "Unknown Error. Please report the issue at 'bhaskar@vaskrneup.com'",
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(trade_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
