# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from products.models import *
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save

class Status(models.Model):

	name = models.CharField(verbose_name = 'категория', max_length=50)
	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name = 'Статус заказа'
		verbose_name_plural = 'Статусы заказа'

	def __str__(self):
		return "Статус %s" % self.name

class Order(models.Model):

	total_price = models.DecimalField(verbose_name = 'общая стоимость', max_digits=9, decimal_places=1, default=0) #total price for all products in order

	customer_name = models.CharField(verbose_name = 'имя', max_length=50)
	customer_email = models.EmailField(verbose_name = 'почта', blank=True, null=True, default=None)
	customer_phone = models.CharField(verbose_name = 'номер тел', max_length=15, default=None)
	customer_address = models.CharField(verbose_name = 'адрес', max_length=150, default=None)
	comment = models.TextField(blank=True, null=True, default=None)
	status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name = 'статус')
	created = models.DateTimeField(verbose_name = 'создан', auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(verbose_name = 'обновлен', auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'

	def __str__(self):
		return "%s %s" % (self.id, self.status.name)

	def save(self, *args, **kwargs):

		super(Order, self).save(*args, **kwargs)

class ProductInOrder(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, default=None, verbose_name = 'заказ')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None, verbose_name = 'товар')
	nmb = models.IntegerField(default=1, verbose_name = 'кол-во')
	price_per_item = models.DecimalField(max_digits=6, decimal_places=1, default=0, verbose_name = 'цена за шт')
	total_price = models.DecimalField(max_digits=9, decimal_places=1, default=0, verbose_name = 'общая стоимость') #price*nmb
	is_active = models.BooleanField(default=True)

	created = models.DateTimeField(verbose_name = 'создан', auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(verbose_name = 'обновлен', auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name = 'Товар в заказе'
		verbose_name_plural = 'Товары в заказе'

	def __str__(self):
		return "%s" % self.product.name

	def save(self, *args, **kwargs):
		price_per_item = self.product.price
		self.price_per_item = price_per_item
		self.total_price = int(self.nmb) * price_per_item

		super(ProductInOrder, self).save(*args, **kwargs)

#calculate order total amount
def products_in_order_post_save(sender, instance, created, **kwargs):

	order = instance.order
	order_total_price = 0

	all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

	for item in all_products_in_order:
		order_total_price += item.total_price

	instance.order.total_price = order_total_price
	instance.order.save(force_update=True)

post_save.connect(products_in_order_post_save, sender=ProductInOrder)

class ProductInBasket(models.Model):
	session_key = models.CharField(max_length=128, blank=True, null=True, default=None, verbose_name = 'сессия')
	order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, default=None, verbose_name = 'заказ')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None, verbose_name = 'товар')
	image = models.ForeignKey(ProductImage, on_delete=models.CASCADE, blank=True, null=True, default=None, verbose_name = 'картинка')
	nmb = models.IntegerField(default=1,verbose_name = 'количество')
	price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name = 'цена за штуку')
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name = 'общая сумма')#price*nmb
	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name = 'создан')
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name = 'обновлен')

	def __str__(self):
		return "%s" % self.product.name

	class Meta:
		verbose_name = 'Товар в корзине'
		verbose_name_plural = 'Товары в корзине'


	def save(self, *args, **kwargs):
		price_per_item = self.product.price
		self.price_per_item = price_per_item
		self.total_price = int(self.nmb) * price_per_item

		super(ProductInBasket, self).save(*args, **kwargs)
