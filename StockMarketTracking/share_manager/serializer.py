from rest_framework import serializers
from share_manager import models


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Share
        fields = ("last_updated", "stock_scrip", "current_price",)


class StockPortfolioSerializer(serializers.ModelSerializer):
    share = StockSerializer()

    class Meta:
        model = models.Portfolio
        fields = ("user", "share", "number_of_shares", "total_holding")
