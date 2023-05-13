from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Avg, Q
from order.serializers import CurrencySerializer, PairSerializer
from order.models import Currency, OrderProcessingTime, Pair
from order.serializers import AvgOrderTimeSerializer
from rest_framework import serializers


class PairList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        return Response({
            "pairs": PairSerializer(Pair.objects.all(), many=True).data,
            "currencies": CurrencySerializer(Currency.objects.all(), many=True).data
        })


class OrderTimeList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        filter_expr = Q()
        serializer = AvgOrderTimeSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        if serializer.data:
            pair = serializer.data.get("pair", "")
            quote = serializer.data.get("quote", "")
            base = serializer.data.get("base", "")
            date_from = serializer.data.get("date_from", "")
            date_to = serializer.data.get("date_to", "")
            if pair:
                pair = Pair.objects.filter(name=pair).first()
                if not pair:
                    raise serializers.ValidationError("quote does not exist")
                filter_expr &= Q(order__pair=pair)
            if quote:
                quote = Currency.objects.filter(name=quote).first()
                if not quote:
                    raise serializers.ValidationError("quote does not exist")
                filter_expr &= Q(order__quote=quote)
            if base:
                base = Currency.objects.filter(name=base).first()
                if not base:
                    raise serializers.ValidationError("base does not exist")
                filter_expr &= Q(order__base=base)
            if date_from:
                filter_expr &= Q(order__created_on__gte=date_from)
            if date_to:
                filter_expr &= Q(order__created_on__lte=date_to)
        avg = OrderProcessingTime.objects.filter(filter_expr).aggregate(Avg('minutes'))['minutes__avg']
        return Response({"avg": avg or 0})
