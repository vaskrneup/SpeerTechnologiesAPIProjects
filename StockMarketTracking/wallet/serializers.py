from rest_framework import serializers
from wallet import models


class WalletDepositViewSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=1, required=True)

    class Meta:
        fields = ("amount",)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wallet
        fields = ("user", "balance")
        read_only_fields = ("user", "balance")
