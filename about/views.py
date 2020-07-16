# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

def about(request):
	return render(request, 'about-us.html', locals())
