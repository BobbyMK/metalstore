
$(document).ready(function(){

	var $form = $(this);

	function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			const cookies = document.cookie.split(';');
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	const csrftoken = getCookie('csrftoken');

	function basketUpdating(product_id, nmb, image, is_delete){
		var data = {};
		data.product_id = product_id;
		data.nmb = nmb;
		data.image_id = image;
		data["csrfmiddlewaretoken"] = csrftoken;
		console.log(data);

		if (is_delete){
			data["is_delete"] = true;
		}
		var url = "/basket_adding/";
		$.ajax({
			url: url,
			type: 'POST',
			data: data,
			cache: true,
			success: function (data) {
				console.log("OK");
				if (data.products_total_nmb || data.products_total_nmb == 0){
					console.log(data);
					$('#prod_nmb').text(data["products_total_nmb"]);
					$('.cart_single_item').empty();
					$('.drop-cart').html("");
					$.each(data.products, function(k, v){
						$('#shopping-cart-table').append('<tr class="cart_single_item"><td class="sop-cart an-shop-cart"><a href="#"><img class="primary-image" alt="" src="' + v.image_url + '"></a><a href="#">'
							+ v.name + '</a></td><td class="sop-cart an-sh"><form action="' + url + '"><input type="hidden" name="csrfmiddlewaretoken" value="'+ data.csrf +'"><div class="quantity ray"><input class="input-text qty text" id="cart_input" data-prod_id="'
							+ v.prod_id + '" data-image_id="' + v.image_id + '" data-nmb="' + v.nmb + '" type="number" size="4" value="' + v.nmb +
							'" min="0" step="1"></div><div class="cart_remove" data-product_id="'+ v.id +'"><a class="remove" href="#"><span>x</span></a></div></form></td><td class="sop-cart"><div class="tb-product-price font-noraure-3"><span class="amount">'
							+ v.price_per_item + 'RUB</span></div></td><td class="cen"><span class="amount" id="amount">'
							+ v.summ + 'RUB</span></td></tr>');
						$('.drop-cart').prepend('<li><div class="add-cart-text"><p><a href="#">'
							+ v.name + '</a></p><p>' + v.price_per_item + 'RUB</p><span>Количество: '
							+ v.nmb + '</span><span>Сумма : ' + v.summ +
							'RUB</span></div><div class="pro-close" data-product_id="'+ v.id +'"><i class="pe-7s-close"></i></div></li>');
					});
					if (data["total_amount"])
						$('#tot_amount').text(data["total_amount"] + " RUB");
					else{
						if (data["total_amount"] == undefined)
							data["total_amount"] = 0;
						$('#tot_amount').text("0 RUB");
					}
					$('.drop-cart').append('<li class="total-amount clearfix"><span class="floatleft"><h6>Сумма</h6></span><span class="floatright"><strong>= ' + data.total_amount +
					'RUB</strong></span></li><li><div class="goto text-center"><a href="/cart/"><strong>в корзину &nbsp;<i class="pe-7s-angle-right"></i></strong></a></div></li><li class="checkout-btn text-center"><a href="/checkout/">Оформить</a></li>');
				}
			},
			error: function (){
				console.log("error");
			}
		})
	}

	//add item into basket
	$(document).on('submit', '#form_input', function(e) {

		e.preventDefault();
		var $form = $(this);
		var nmb = $form.find('#number').val();
		var submit_btn = $form.find('#submit_btn');
		var product_id = submit_btn.data("product_id");
		var name = submit_btn.data("name");
		var image = submit_btn.data("image");
		var price = parseFloat(submit_btn.data("price").replace(',', '.'));
		var summ = (nmb * price).toFixed(2);

		basketUpdating(product_id, nmb, image, is_delete=false);

	});

	//show summ on catalog page
	$(document).on('change', '#form_input', function(e) {
		e.preventDefault();
		var $form = $(this);
		var nmb = $form.find('#number').val();
		var submit_btn = $form.find('#submit_btn');
		var price = parseFloat(submit_btn.data("price").replace(',', '.'));
		var summ = (nmb * price).toFixed(2);

		$form.find('#summ').text(summ);
	});

	//delete item in bar
	$(document).on('click', '.pro-close', function(e) {
		e.preventDefault();
		var nmb = 0;
		var product_id = $(this).data("product_id");
		var image = 0

		basketUpdating(product_id, nmb, image, is_delete=true);
	});

	//delete item on cart page
	$(document).on('click', '.cart_remove', function(e) {
		e.preventDefault();
		var nmb = 0;
		var product_id = $(this).data("product_id");
		var image = 0

		basketUpdating(product_id, nmb, image, is_delete=true);
	});

	//change values in database on cart page by click
	$(document).on('change', '#cart_input', function(e) {
		e.preventDefault();
		var $input = $(this);
		var product_id = $input.data("prod_id");
		var nmb = $input.val();
		var old = $input.data("nmb");
		var image = $input.data("image_id");

		nmb = nmb - old;

		basketUpdating(product_id, nmb, image, is_delete=false);
	});
});
