from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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


class StockTradeViewSerializer(serializers.Serializer):
    transaction_type = serializers.ChoiceField(
        choices=(
            ("BUY", "BUY"),
            ("SELL", "SELL"),
        ),
        error_messages={
            'invalid_choice': _('"{input}" is not a valid choice. Valid choices are "BUY", "SELL".'),
        }
    )
    scrip = serializers.CharField(
        max_length=16,
    )
    scrip_count = serializers.FloatField(
        min_value=1,
    )

    def validate_scrip(self, scrip: str):
        if not models.Share.objects.filter(stock_scrip=scrip).exists():
            raise ValidationError(
                f"{scrip} is not a valid Stock Symbol. "
                f"See all available scrip through '{reverse('share_manager:GetAllScrips')}'"
            )

        return scrip

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
