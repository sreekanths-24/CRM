from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.db.models import Q


def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	if 'qp' in request.GET:
		qp = request.GET['qp']
		products = Product.objects.filter(Q(name__icontains=qp) | Q(description__icontains=qp))
	else:
		products = Product.objects.all()
	context = {
		'products':products, 
		'cartItems':cartItems
	}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		country=data['shipping']['country'],
		phone=data['shipping']['phone'],
		)

	return JsonResponse('Order submitted..', safe=False)

def previous_order(request):
    if 'q1' in request.GET:
        q1 = request.GET['q1']
        emailid = OrderItem.objects.filter(order__customer__email__icontains=q1)
        return render(request, 'store/previous_purchase.html', {'emailid': emailid, 'q1':q1})
    else:
        return render(request, 'store/previous_purchase.html')


# def previous_order(request):
# 	if 'q1' in request.GET:
# 		q1 = request.GET['q1']
# 		multiq= Q(Q(customer__email__icontains=q1))
# 		emailid = ShippingAddress.objects.filter(multiq)
# 		return render(request, 'store/previous_purchase.html', {'emailid':emailid})
# 	elif 'q2' in request.GET:
# 		q2 = request.GET['q2']
# 		orderid = OrderItem.objects.filter(order__id__icontains=q2)
# 		return render(request, 'store/previous_purchase.html', {'orderid':orderid})
# 	else:
# 		return render(request, 'store/previous_purchase.html')
