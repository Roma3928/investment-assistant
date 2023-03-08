from django.db import models


class CompanyCategory(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=250, unique=True)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(
        CompanyCategory,
        related_name='companies',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    exchange = models.CharField(max_length=250, null=True, blank=True)
    rate = models.CharField(max_length=50, null=True, blank=True)
    income = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Promotion(models.Model):
    company = models.ForeignKey(Company, related_name='promotions', on_delete=models.CASCADE)
    buy_to = models.CharField(max_length=30)
    register = models.CharField(max_length=30)
    price = models.CharField(max_length=100)
    lot = models.CharField(max_length=100)
    dividend = models.CharField(max_length=100)
    income = models.CharField(max_length=100)

    def __str__(self):
        return self.company.name


class Tax(models.Model):
    state = models.CharField(max_length=40, verbose_name='Страна эмитента')
    tax_rate = models.IntegerField(verbose_name='Налоговая ставка')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.state