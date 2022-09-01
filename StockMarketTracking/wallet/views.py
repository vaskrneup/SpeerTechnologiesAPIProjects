from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from wallet import serializers
from rest_framework import status
from wallet import models


class AddMoney(APIView):
    """
    Adds money to the wallet.
    """

    def post(self, request: Request):
        """
        Add money to the user wallet.

        :param request: Request data from client side.
        :return: updated user wallet data.
        """
        serializer = serializers.WalletDepositViewSerializer(data=request.data)

        if serializer.is_valid():
            if hasattr(request.user, "wallet"):
                request.user.wallet.deposit(
                    amount=serializer.validated_data.get("amount")
                )
                request.user.wallet.save()
            else:
                models.Wallet(
                    user=request.user,
                    balance=serializer.validated_data.get("amount")
                ).save()

            return Response(
                serializers.WalletSerializer(
                    instance=request.user.wallet
                ).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
