from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail

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

        if User.objects.filter(username=username):
            messages.warning(request, 'User name alrady exist')
            return redirect('signup')
        
        if User.objects.filter(email=email):
            messages.warning(request, 'using this email you have alrady created an account!')
            return redirect('signup')
        
        if len(username) > 10:
            messages.warning(request, 'username must be under 10 charecter!')
            return redirect('signup')
        
        if password1 != password2: 
            messages.warning(request, "Password dosen't match! ")
            return redirect('signup')
        
        # if not username.isalnum():
        #     messages.warning(request, "Username must be Alpha-Numeric! ")
        #     return redirect('signup')
        

        my_user = User.objects.create_user(username, email, password1)
        my_user.first_name = first_name
        my_user.last_name = last_name

        my_user.save()

        messages.success(request, 'you have succesfully create an account. please cheak you mail and confirm you account  ')


        # Welcome Email 
        subject = 'Welcome to GFG- Django Login!!'
        message = 'Hello ' + my_user.first_name + ' Welcome to GFG. Thank you for visiting our website. you will got another mail for confirm your account. please cheak it and confirm it'
        from_email = settings.EMAIL_HOST_USER
        to_list = [my_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


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