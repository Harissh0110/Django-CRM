from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.db.models import Q


def home(request):
    query = request.GET.get('q')
    if query:
        records = Record.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(email__icontains=query) | 
            Q(phone__icontains=query) | 
            Q(address__icontains=query) | 
            Q(city__icontains=query) | 
            Q(state__icontains=query) | 
            Q(zipcode__icontains=query)
        )
    else:
        records = Record.objects.all()
    return render(request, 'home.html', {'records': records, 'query': query})




def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You Have Been Logged In Successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'You Have Been Logged Out')
    return redirect('login')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
            #Look up for record
            customer_record = Record.objects.get(id=pk)
            return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You Must Loggen in To view This page")
        return redirect('home')

def delete_record(request, pk):
     if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully")
        return redirect('home')
     else:
          messages.success(request, "You Must Loggen in To view This page")
          return redirect('home')
     
def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In")
		return redirect('home')
      

def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In")
		return redirect('home')
      

