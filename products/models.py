# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

class ProductCategory(models.Model):
	name = models.CharField(verbose_name = 'имя', max_length=64, blank=True, null=True, default=None)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return "%s" % self.name

	class Meta:
		verbose_name = 'Категория товара'
		verbose_name_plural = 'Категория товаров'

class SubCategory(models.Model):
	name = models.CharField(verbose_name = 'имя', max_length=64, blank=True, null=True, default=None)
	is_active = models.BooleanField(default=True)
	category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, blank=True, null=True, default=None, verbose_name = 'категория')

	def __str__(self):
		return "%s" % self.name

	class Meta:
		verbose_name = 'Суб-Категория товара'
		verbose_name_plural = 'Суб-Категория товаров'

class Product(models.Model):

	name = models.CharField(verbose_name = 'имя', max_length=200)
	price = models.DecimalField(verbose_name = 'цена', max_digits=9, decimal_places=2, default=0)
	description = models.TextField(verbose_name = 'описание', max_length=1000, blank=True, null=True, default=None)
	is_active = models.BooleanField(default=True)
	weight = models.DecimalField(verbose_name = 'вес', max_digits=9, decimal_places=2, default=0)
	category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, blank=True, null=True, default=None, verbose_name = 'категория')
	sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True, default=None, verbose_name = 'суб-категория')

	created = models.DateTimeField(verbose_name = 'создан', auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(verbose_name = 'обновлен', auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'

	def __str__(self):
		return "%s" % self.name

class ProductImage(models.Model):

	product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None)
	image = models.ImageField(upload_to='static/img/products_images/')
	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name = 'Картинка товара'
		verbose_name_plural = 'Картинки товаров'

	def __str__(self):
		return "%s" % self.id
