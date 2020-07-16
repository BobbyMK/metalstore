# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

def checkout(request):
	return render(request, 'checkout.html', locals())
