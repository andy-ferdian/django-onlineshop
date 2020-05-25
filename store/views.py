from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from decimal import *

from .models import *
from . utils import cookieCart,cartData, guessOrder

# Create your views here.
def store(request):
	data = cartData(request)

	cartItems = data['cartItems']

	product = Product.objects.all()
	context = {'products':product, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


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
		action = data['action']

		print('Action:', action)
		print('ProductId:', productId)

		customer = request.user.customer
		product = Product.objects.get(id=productId)
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

		orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

		if action == 'add':
			orderItem.quantity = (orderItem.quantity + 1)
		elif action == 'remove' and orderItem.quantity > 0:
			orderItem.quantity = (orderItem.quantity - 1)

		orderItem.save()

		if orderItem.quantity == 0:
			orderItem.delete()
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

			product = Product.objects.get(id=i)
			total = (product.price * cart[i]['quantity'])
			grand_total += total
			cart_total += cart[i]['quantity']

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'product':{
					'id':product.id,
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
