from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    return render(request, 'authentication/index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        my_user = User.objects.create_user(username, email, password1)
        my_user.first_name = first_name
        my_user.last_name = last_name

        my_user.save()

        messages.success(request, 'you have succesfully create an account ')
        return redirect('signin')
        
    return render(request, 'authentication/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            first_name = user.first_name
            messages.success(request, 'Logged in successfully')
            return render(request,  'authentication/index.html', {'first_name' : first_name})
        
            
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('signin')


    return render(request, 'authentication/signin.html')

def signout(request):
    logout(request) 
    messages.warning(request, 'You are Successfully Logout!')
    return redirect('home') 