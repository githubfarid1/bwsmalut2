from django.shortcuts import render, redirect
from django.contrib.auth import login,  logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .forms import UserLoginForm, UserRegistrationForm 
from django.http import HttpResponse, Http404
from django.contrib import messages

# Create your views here.


# ALTERNATIVE 1


def updatePasswordRequest(request):
    if not request.user.is_authenticated:
        return redirect('front_page')
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.info(request, 'Ubah Password sukses, Silahkan login lagi!!')
            logout(request)
            return redirect('front_page')
        else:
            messages.info(request, 'Berikan password yang benar sesuai format..!!')
            return redirect('update_password')
    else:
        form = PasswordChangeForm(user=request.user)
        
    context = {'form' : form}
    return render(request, 'update_password.html', context)
    

def home(request):
    if not request.user.is_authenticated:
        return redirect("/")
    return render(request,'homePage.html')

def front_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request,'front_page.html')

def landingPage(request):
    return render(request, 'landingPage.html')


def UserRegistrationRequest(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    context = {'form' : form}
    return render(request, 'registerUser.html', context)



def UserLoginRequest(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    context = {'form' : form}
    return render(request, 'loginUser.html', context)


def UserLogoutRequest(request):
    logout(request)
    return redirect('front_page')


# ALTERNATIVE 2

# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})


# def log_in(request):
#     if request.method == "POST":
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request,user)
#             return redirect('home')
#     else:
#         form = AuthenticationForm()
#     return render(request,'login.html', {"form":form})

# def log_out(request):
#     logout(request)
#     return redirect('front_page')

