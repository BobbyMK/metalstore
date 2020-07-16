from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render
from .forms import CheckoutForm
from django.core.mail import send_mail


#return to ajax a return_dict as JsonResponse
def	basket_adding(request):
	return_dict = dict()
	session_key = request.session.session_key
	print(request.POST)
	data = request.POST
	product_id = data.get("product_id")
	nmb = data.get("nmb")
	csrf = data.get("csrfmiddlewaretoken")
	image_id = data.get("image_id")
	is_delete = data.get("is_delete")

	if is_delete == 'true':
		ProductInBasket.objects.filter(id=product_id).update(is_active=False)
	else:
		new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, image_id=image_id , product_id=product_id, is_active=True, defaults={"nmb":nmb})
		if not created:
			new_product.nmb += int(nmb)
			new_product.save(force_update=True)

#get objects filtered by session_key
	products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
	products_total_nmb = products_in_basket.count()
	return_dict["products_total_nmb"] = products_total_nmb
	return_dict["products"] = list()
	return_dict["csrf"] = csrf
	total_amount = 0
	for item in products_in_basket:
		product_dict = dict()
		product_dict["prod_id"] = item.product.id
		product_dict["image_url"] = item.image.image.url
		product_dict["image_id"] = item.image.id
		product_dict["name"] = item.product.name
		product_dict["price_per_item"] = item.price_per_item
		product_dict["nmb"] = item.nmb
		product_dict["summ"] = item.nmb * item.price_per_item
		product_dict["id"] = item.id
		total_amount += item.nmb * item.price_per_item
		return_dict["total_amount"] = total_amount
		return_dict["products"].append(product_dict)

	return JsonResponse(return_dict)

#get from form customer data
def checkout(request):
	session_key = request.session.session_key
	product_list = [];
	total = 0;
	products_in_basket = ProductInBasket.objects.filter(session_key=session_key,
		is_active=True, order__isnull=True)

	form = CheckoutForm(request.POST or None)
	if request.POST:
		print(request.POST)
		if form.is_valid():
			print("FORM NORM")
			data = request.POST
			name = data.get("name")
			email = data["email"]
			phone = data["phone"]
			address = data.get("address")
			comment = data.get("comment")

			order = Order.objects.create(customer_name=name, customer_phone=phone,
				customer_email=email, customer_address=address, comment=comment, status_id=1)
			to_print = data.items()
			print(to_print)
			for product in products_in_basket:
				total += product.total_price
				product_list.append(str(product.product.name) + ' кол-во: ' + str(product.nmb) + ' цена за шт: ' + str(product.price_per_item) + 'руб')
				ProductInOrder.objects.create(product=product.product, nmb=product.nmb,
					price_per_item=product.price_per_item, total_price=product.total_price, order=order)
			print(order)
			print(product_list)
#send mail to our company
			send_mail('Новый заказ №' + str(order.id), 'Имя: ' + order.customer_name + '\nАдрес: '+ order.customer_address + '\nНомер: '+ order.customer_phone +
			'\nПочта: '+ order.customer_email + '\n\n' +'\n'.join(product_list) + '\nОбщая сумма: ' + str(total),
				'callback.smm@gmail.com', ['callback.smm@gmail.com'], fail_silently=False)
#send mail to customer
			send_mail('Ваш заказ №' + str(order.id), 'Спасибо за ваш заказ в СтройМаркетМеталл! \nНомер вашего заказа: ' + str(order.id) + '\nСумма: '+ str(total) + '\nМы свяжемся с Вами в течении 30 минут.',
				'callback.smm@gmail.com', [order.customer_email], fail_silently=False)
			return render(request, 'success.html/', locals())
		else:
			print("form is not valid")
	return render(request, 'checkout.html/', locals())