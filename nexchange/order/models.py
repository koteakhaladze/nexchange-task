from django.db import models

class Pair(models.Model):
   name = models.CharField(max_length=32, null=False, blank=False)

class Currency(models.Model):
   name = models.CharField(max_length=32, null=False, blank=False)


class Order(models.Model):
   pair = models.ForeignKey(Pair, null=False, blank=False, on_delete=models.PROTECT)
   quote = models.ForeignKey(Currency, null=False, on_delete=models.PROTECT, related_name='quote_currency')
   base = models.ForeignKey(Currency, null=False, on_delete=models.PROTECT, related_name='base_currency')
   created_on = models.DateTimeField(auto_now_add=True)


class OrderProcessingTime(models.Model):
   order = models.ForeignKey(
       Order, related_name='processing_times', on_delete=models.CASCADE)
   minutes = models.IntegerField(null=False, blank=False)
