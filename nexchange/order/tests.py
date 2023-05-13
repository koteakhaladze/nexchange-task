import pytest
from django.test import Client

from .models import Currency, Order, OrderProcessingTime, Pair
pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return Client()

@pytest.fixture
def quote():
    return Currency.objects.create(name="BTC")

@pytest.fixture
def base():
    return Currency.objects.create(name="USDT")

@pytest.fixture
def pair():
    return Pair.objects.create(name="BTCUSDT")


@pytest.fixture
def order(base, quote, pair):
    return Order.objects.create(base=base, quote=quote, pair=pair)

@pytest.fixture
def order2(base, quote, pair):
    return Order.objects.create(quote=base, base=quote, pair=pair)

@pytest.fixture
def avg_time(order):
    return OrderProcessingTime.objects.create(order=order, minutes=10)

@pytest.fixture
def avg_time2(order2):
    return OrderProcessingTime.objects.create(order=order2, minutes=5)

@pytest.mark.django_db
def test_get_avg_time(client, order, order2, avg_time, avg_time2):
    response = client.get("/api/orders/processing-time")
    data = response.json()
    assert data["avg"] == 7.5

@pytest.mark.django_db
def test_get_avg_time_raises_error(client, order, order2, avg_time, avg_time2):
    response = client.get("/api/orders/processing-time", {"pair": "BTCUSDT", "base": "BTC"})
    assert response.status_code == 400
