# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

class Review(models.Model):

	review_title = models.CharField('Название отзыва', max_length=50)
	review_text = models.TextField('Текст отзыва', max_length=1000)
	review_date = models.DateField('Дата отзыва', auto_now=True, auto_now_add=False)

	class Meta:
		verbose_name = 'Отзыв'
		verbose_name_plural = 'Отзывы'

	def __str__(self):
		return self.review_title

	def get_absolute_url(self):
		return reverse("_detail", kwargs={"pk": self.pk})