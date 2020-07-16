# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render


def cart(request):
	return render(request, 'shopping-cart.html', locals())
