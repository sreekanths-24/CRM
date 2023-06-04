from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from mainpart.models import Record
from store.models import *
from django.db.models import Q
from .forms import AddSupplierRecord
from django.db.models import Sum

# Create your views here.
def sendfeedback(request):
	if request.method == "POST":
		name = request.POST["yourname"]
		email = request.POST["youremail"]
		feedback = request.POST["userfeedbacktake"]
		#print(f'name = {name} email = {email} feedback = {feedback}')
		obj = FeedbackTable(name=name, email=email, feedback=feedback)
		obj.save()
		# messages.success(request, "feedback submitted sucessfully")
		return redirect('store')
	return render(request, 'give_feedback.html')

def viewfeedback(request):
    feedback_list = FeedbackTable.objects.order_by('-created_at')
    return render(request, 'see_feedback.html', {'feedback_list': feedback_list})
    
def searchdata(request):
	if request.method == "POST":
		searcheddata = request.POST['searcheddata']
		# recordresults = Record.objects.filter(first_name__icontains=searcheddata)
		multi_q = Q(Q(first_name__icontains=searcheddata) | Q(last_name__icontains=searcheddata)| Q(email__icontains=searcheddata)| Q(phone__icontains=searcheddata)| Q(address__icontains=searcheddata)| Q(city__icontains=searcheddata)| Q(state__icontains=searcheddata)| Q(zipcode__icontains=searcheddata)| Q(product__icontains=searcheddata))
		recordresults = Record.objects.filter(multi_q)
		return render(request, 'searchdata.html', {'searcheddata':searcheddata, 'recordresults':recordresults})
	else:
		return render(request, 'searchdata.html', {})

def searchorder(request):
	if request.method == "POST":
		searchedorder = request.POST['searchedorder']
		multi_q = Q(Q(order__id__icontains=searchedorder) |
	      Q(customer__name__icontains=searchedorder) |
            Q(address__icontains=searchedorder) |
            Q(city__icontains=searchedorder) |
            Q(state__icontains=searchedorder))

		recordresults = ShippingAddress.objects.filter(multi_q)
		return render(request, 'searchorder.html', {'searchedorder':searchedorder, 'recordresults':recordresults})
	else:
		return render(request, 'searchorder.html', {})	

def searchid(request):
	if request.method == "POST":
		searchedid = request.POST['searchedid']
		multi_q = Q(Q(order__id__icontains=searchedid) |
            Q(product__name__icontains=searchedid))		
		recordresults = OrderItem.objects.filter(multi_q)
		return render(request, 'searchid.html', {'searchedid':searchedid, 'recordresults':recordresults})
	else:
		return render(request, 'searchid.html', {})	
	
def ecommdata(request):
	ecommshippingdata = ShippingAddress.objects.order_by('-date_added')
	return render(request, 'ecommdata.html', { 'ecommshippingdata':ecommshippingdata})

def ecommorderdata(request):
	ecommorders = OrderItem.objects.order_by('-date_added')
	return render(request, 'ecommorder.html', {'ecommorders':ecommorders})

def supplierrecords(request):
	supplier_list = SupplierRecord.objects.order_by('-created_at')

	return render(request, 'supplier_record.html', {'supplier_list':supplier_list})

def supplier(request, pk):
	if request.user.is_authenticated:
		supplier_record = SupplierRecord.objects.get(id=pk)
		return render(request, 'single_supplier_record.html', {'supplier_record':supplier_record})
	else:
		messages.success(request, "You must me logged in to view this record.")
		return redirect('home_crm')

def delete_supplier(request, pk):
	if request.user.is_authenticated:
		delete_it = SupplierRecord.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Supplier record deleted sucessfully.")
		return redirect('supplierrecords')
	else:
		messages.success(request, "You must me logged in to view this record.")
		return redirect('home_crm')

def add_supplier_record(request):
	form = AddSupplierRecord(request.POST or None)
	if request.user.is_authenticated:
		if request.method == 'POST':
			if form.is_valid():
				add_supplier_record = form.save()
				messages.success(request, "New supplier record added")
				return redirect('supplierrecords')
		return render(request, 'add_supplier_record.html', {'form':form})
	else:
		messages.success(request, "You need to login first")
		return redirect('home_crm')
		
def update_supplier(request, pk):
	if request.user.is_authenticated:
		current_record = SupplierRecord.objects.get(id=pk)
		form = AddSupplierRecord(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Supplier record updated")
			return redirect('supplierrecords')
		return render(request, 'update_supplier_record.html', {'form':form})
	else:
		messages.success(request, "You need to login first")
		return redirect('home_crm')
	
def dashboard(request):
	totalfeedbacks = FeedbackTable.objects.all()
	totalcustomers = ShippingAddress.objects.all()
	totalproducts = Product.objects.all()
	totalsuppliers = SupplierRecord.objects.all()

	order_items = OrderItem.objects.values('product__name').annotate(total_quantity=Sum('quantity'))
	product_quantities = {item['product__name']: item['total_quantity'] for item in order_items}
    
	product_names = list(product_quantities.keys())
	product_totals = list(product_quantities.values())

	context = {
		'totalfeedbacks':totalfeedbacks,
		'totalcustomers':totalcustomers,
		'totalproducts':totalproducts,
		'totalsuppliers':totalsuppliers,
		'product_names': product_names,
        'product_totals': product_totals,
	}
	return render(request, 'dashboard.html', context)


		