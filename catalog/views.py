# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from products.models import *

#add filter by category
def catalog(request):
	session_key = request.session.session_key
	if not session_key:
		request.session.cycle_key()
	sub = SubCategory.objects.all()
	category = ProductCategory.objects.all()
	products_images = ProductImage.objects.filter(is_active=True, product__is_active=True)
	id = request.GET.get('id')
	value = request.GET.get('value')
	if value is not None:
		if value == 'sub':
			products_images_armatura = products_images.filter(product__sub_category__id=id)
		else:
			products_images_armatura = products_images.filter(product__category__id=id)
	return render(request, 'shop.html', locals())
