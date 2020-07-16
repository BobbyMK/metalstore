# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .forms import ReviewForm

def main(request):
#	form = ReviewForm(request.POST or None)
#	if request.method == "POST" and form.is_valid():
#		new_form = form.save()
	return render(request, 'index.html', locals())
