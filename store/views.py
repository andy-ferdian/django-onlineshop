from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from django.db.models import Avg, Max, Min, Sum
from decimal import *

from .models import *
from . utils import *

# Create your views here.
def store(request):
	data = cartData(request)

	cartItems = data['cartItems']

	products = Product.objects.all()

	for obj in products:
		min_prc = ProductVariation.objects.filter(product=obj.product_id).aggregate(Min('price'))
		max_prc = ProductVariation.objects.filter(product=obj.product_id).aggregate(Max('price'))
		obj.min_prc = min_prc['price__min']
		obj.max_prc = max_prc['price__max']

	# import pdb; pdb.set_trace()
	# min_price, max_price = product_price_range(ProductVariation)
	# import pdb; pdb.set_trace()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def product(request, product_slug, product_id):
	data = cartData(request)

	cartItems = data['cartItems']
	# import pdb; pdb.set_trace()
	product = Product.objects.get(product_id=product_id)
	# main_image = ProductMainImage.objects.select_related('product').filter(product=product_id)
	# additional_image = ProductAdditionalImage.objects.select_related('product').filter(product=product_id)
	# all_color = ProductVariation.objects.select_related('color').filter(product=product_id).values('color__color_name').distinct()
	# all_color_id = ProductVariation.objects.select_related('color').filter(product=product_id).values('color__id').distinct()
	all_colors = ProductVariation.objects.select_related('color').filter(product=product_id).distinct()
	all_sizes = ProductVariation.objects.select_related('size').filter(product=product_id).distinct()
	# all_size = ProductVariation.objects.select_related('size').filter(product=product_id).values('size__size').distinct()
	# all_size_id = ProductVariation.objects.select_related('size').filter(product=product_id).values('size__id').distinct()
	# colors = [obj['color__color_name'] for obj in all_color]
	# sizes = [obj['size__size'] for obj in all_size]
	# for obj in all_color_all:
		# import pdb; pdb.set_trace()
	# 	sizes.append(obj['size__size'])
	min_prc = ProductVariation.objects.filter(product=product_id).aggregate(Min('price'))
	max_prc = ProductVariation.objects.filter(product=product_id).aggregate(Max('price'))

	min_price = min_prc['price__min']
	max_price = max_prc['price__max']

	product_variations = ProductVariation.objects.select_related('product').filter(product=product_id)
	# import pdb; pdb.set_trace()
	context = 	{'product':product, 'cartItems':cartItems,
	 			 'all_colors':all_colors, 'all_sizes':all_sizes,
				 # 'product_variations':product_variations,
				 'min_price':min_price, 'max_price':max_price
				 }

	return render(request, 'store/product.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	# import pdb; pdb.set_trace()
	return render(request, 'store/cart.html', context)


def checkout(request):
	data = cartData(request)

	if request.user.is_authenticated:
		customer = Customer.objects.get(user=request.user)
	else:
		customer = {}

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems, 'customer':customer}
	# import pdb; pdb.set_trace()
	return render(request, 'store/checkout.html', context)


def updateItem(request):

	if request.user.is_authenticated:
		data = json.loads(request.body)
		productId = data['productId']
		# productVarId = data['productVarId']
		action = data['action']

		print('Action:', action)
		print('ProductId:', productId)
		# print('ProductVarId:', productVarId)

		customer = request.user.customer
		# import pdb; pdb.set_trace()
		product = Product.objects.get(product_id=productId)
		product_stock = product.stock

		order, created = Order.objects.get_or_create(customer=customer, complete=False)

		if product.variation:
			product_variation = ProductVariation.objects.get(product__product_id=productId, image__main_image=True)
			product_stock = product_variation.stock
			orderItem, created = OrderItem.objects.get_or_create(order=order, product_variation=product_variation)
		else:
			# import pdb; pdb.set_trace()
			orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

		# if action == 'add':
		# 	orderItem.quantity = (orderItem.quantity + 1)
		if action == 'add' and orderItem.quantity < product_stock:
			orderItem.quantity = (orderItem.quantity + 1)
		elif action == 'remove' and orderItem.quantity > 0:
			orderItem.quantity = (orderItem.quantity - 1)

		orderItem.save()

		if orderItem.quantity == 0:
			orderItem.delete()
		# import pdb; pdb.set_trace()
		data = {
					'orderItemQty':orderItem.quantity,
					'cartTotal':order.get_cart_total,
					'itemTotal':orderItem.get_total,
					'cartItems':order.get_cart_items
					}
	else:
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}
		print('Cart:', cart)
		items = []
		order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
		cartItems = order['get_cart_items']
		grand_total = 0
		cart_total = 0

		for i in cart:
			cartItems += cart[i]['quantity']

			product = Product.objects.get(product_id=i)
			product_variation = ProductVariation.objects.get(product__product_id=i, image__main_image=True)
			total = (product_variation.price * cart[i]['quantity'])
			grand_total += total
			cart_total += cart[i]['quantity']

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'product':{
					'id':product.product_id,
					},
				'quantity':cart[i]['quantity'],
				'get_total':total,
				}
			items.append(item)

		# import pdb; pdb.set_trace()
		data = {
				'items':items,
				'grand_total':grand_total,
				'cart_total':cart_total
				}

	# import pdb; pdb.set_trace()
	return JsonResponse(data, safe=False)


def updateVariation(request):

	if request.user.is_authenticated:
		data = json.loads(request.body)
		productId = data['productId']
		# productVarId = data['productVarId']
		action = data['action']
		var_id = data['var_id']

		print('Action:', action)
		print('ProductId:', productId)
		print('color_id:', color_id)
		print('size_id:', size_id)
		# print('ProductVarId:', productVarId)

		customer = request.user.customer
		# import pdb; pdb.set_trace()
		product = Product.objects.get(product_id=productId)
		product_stock = product.stock

		order, created = Order.objects.get_or_create(customer=customer, complete=False)

		# if product.variation:
		product_variation = ProductVariation.objects.get(product__product_id=productId, color=color_id, size=size_id)
		product_stock = product_variation.stock
		orderItem, created = OrderItem.objects.get_or_create(order=order, product_variation=product_variation)
		# else:
		# 	# import pdb; pdb.set_trace()
		# 	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

		# if action == 'add':
		# 	orderItem.quantity = (orderItem.quantity + 1)
		if action == 'add' and orderItem.quantity < product_stock:
			orderItem.quantity = (orderItem.quantity + 1)
		elif action == 'remove' and orderItem.quantity > 0:
			orderItem.quantity = (orderItem.quantity - 1)

		orderItem.save()

		if orderItem.quantity == 0:
			orderItem.delete()
		# import pdb; pdb.set_trace()
		data = {
					'orderItemQty':orderItem.quantity,
					'cartTotal':order.get_cart_total,
					'itemTotal':orderItem.get_total,
					'cartItems':order.get_cart_items
					}
	else:
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}
		print('Cart:', cart)
		items = []
		order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
		cartItems = order['get_cart_items']
		grand_total = 0
		cart_total = 0

		for i in cart:
			cartItems += cart[i]['quantity']

			product = Product.objects.get(product_id=i)
			product_variation = ProductVariation.objects.get(product__product_id=i, image__main_image=True)
			total = (product_variation.price * cart[i]['quantity'])
			grand_total += total
			cart_total += cart[i]['quantity']

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'product':{
					'id':product.product_id,
					},
				'quantity':cart[i]['quantity'],
				'get_total':total,
				}
			items.append(item)

		# import pdb; pdb.set_trace()
		data = {
				'items':items,
				'grand_total':grand_total,
				'cart_total':cart_total
				}

	# import pdb; pdb.set_trace()
	return JsonResponse(data, safe=False)


def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)


	else:
		customer, order = guessOrder(request, data)

	total = Decimal(data['form']['total'])
	order.transaction_id = transaction_id

	# import pdb; pdb.set_trace()
	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			kecamatan=data['shipping']['kecamatan'],
			province=data['shipping']['province'],
			postcode=data['shipping']['postcode'],
		)

	return JsonResponse('Payment complete!', safe=False)
