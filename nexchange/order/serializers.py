from datetime import datetime as dt
from rest_framework import serializers

from order.models import Currency, Pair

class AvgOrderTimeSerializer(serializers.Serializer):
    pair = serializers.CharField(required=False)
    quote = serializers.CharField(required=False)
    base = serializers.CharField(required=False)
    date_from = serializers.CharField(required=False)
    date_to = serializers.CharField(required=False)

    def validate_date_from(self, value):
        try:
            return dt.fromisoformat(value)
        except ValueError as exc:
            raise serializers.ValidationError(exc)
        
    def validate_date_to(self, value):
        try:
            return dt.fromisoformat(value)
        except ValueError as exc:
            raise serializers.ValidationError(exc)

    def validate(self, data):
        if data.get("pair", "") and (data.get("base", "") or data.get("quote", "")):
            raise serializers.ValidationError("pair cannot be used with base or quote")
        try:
            date_from = data.get("date_from", "")
            date_to = data.get("date_to", "")
            if date_from and date_to:
                if date_from > date_to:
                    raise serializers.ValidationError("date_from must be less than date_to")
        except ValueError as exc:
            raise serializers.ValidationError(exc)
        
        return data


class PairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pair
        fields = '__all__'

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("name", )