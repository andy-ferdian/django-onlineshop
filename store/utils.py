import json
from . models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:', cart)

    items = []

    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        cartItems += cart[i]['quantity']

        product_variation = ProductVariation.objects.get(product__product_id=i, image__main_image=True)
        product = Product.objects.get(product_id=i)
        # import pdb; pdb.set_trace()
        image = ProductImage.objects.get(product__product_id=i, main_image=True)
        total = (product_variation.price * cart[i]['quantity'])

        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]['quantity']

        item = {
            'product':{
                'product_id':product.product_id,
                'name':product.name,
                'price':product_variation.price,
                'image':image.main_image
                },
            'quantity':cart[i]['quantity'],
            'get_total':total,
            }

        items.append(item)

        if product_variation.digital == False:
            order['shipping'] = True

    return {'items':items, 'order':order, 'cartItems':cartItems}


def cartData(request):
    if request.user.is_authenticated:
    	customer = request.user.customer
    	order, created = Order.objects.get_or_create(customer=customer, complete=False)
    	items = order.orderitem_set.all()
    	cartItems = order.get_cart_items
    else:
    	cookieData = cookieCart(request)
    	cartItems = cookieData['cartItems']
    	order = cookieData['order']
    	items = cookieData['items']

    return {'items':items, 'order':order, 'cartItems':cartItems}


def guessOrder(request, data):
    print('User is not logged in...')
    print('COOKIES:',request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['product_id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order


def product_price_range(ProductVariation):
    min_prc = ProductVariation.objects.filter(product=product_id).aggregate(Min('price'))
    max_prc = ProductVariation.objects.filter(product=product_id).aggregate(Max('price'))

    return min_prc, max_prc
