# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 0

class SubCategoryInline(admin.TabularInline):
	model = SubCategory
	extra = 0

class ProductInline(admin.TabularInline):
	model = Product
	extra = 0

class ProductCategoryAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ProductCategory._meta.fields]
	inlines = [SubCategoryInline]

	class Meta:
		model = ProductCategory

admin.site.register(ProductCategory, ProductCategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
	list_display = [field.name for field in SubCategory._meta.fields]
	list_filter = ['category']
	inlines = [ProductInline]

	class Meta:
		model = SubCategory

admin.site.register(SubCategory, SubCategoryAdmin)

class ProductAdmin (admin.ModelAdmin):
	list_display = [field.name for field in Product._meta.fields]
	list_filter = ['category', 'sub_category' , 'created']
	inlines = [ProductImageInline]

	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)

class ProductImageAdmin (admin.ModelAdmin):
	list_display = [field.name for field in ProductImage._meta.fields]

	class Meta:
		model = ProductImage

admin.site.register(ProductImage, ProductImageAdmin)
