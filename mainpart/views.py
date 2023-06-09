from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    records = Record.objects.all()

    #check to see if loggin in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('dashboard')
        else:
            messages.success(request, "Incorrect username or password, Please try again.")
            return redirect('home_crm')
    else:
        return render(request, 'home.html', {'records':records})

# def login_user(request):
    

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out..")
    return redirect('home_crm')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user= authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered! welcome!")
            return redirect('home_crm')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})


def customer_record(request, pk):
    #if logged in
    if request.user.is_authenticated:
        #check the record
        customer_record = Record.objects.get(id=pk)
        return render(request, 'records.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You must log in to view that page.")
        return redirect('home_crm')

def delete_record(request, pk):
    if request.user.is_authenticated:    
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record deleted successfully!!")
        return redirect('home_crm')
    else:
        messages.success(request, "You must log in to do that.")
        return redirect('home_crm')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:    
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "New record added successfully!!")
                return redirect('home_crm')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to add new records.")
        return redirect('home_crm')

def update_record(request, pk):
    if request.user.is_authenticated:    
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully!!")
            return redirect('home_crm')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to update records.")
        return redirect('home_crm')