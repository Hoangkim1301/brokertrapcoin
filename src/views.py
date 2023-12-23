#create a log in page
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

# Create your views here.

def dashboard(request):
    return render(request, 'dashboard.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard upon successful login
    else:
        form = AuthenticationForm()
    return render(request, 'webHost/web/templates/login.html', {'form': form})
        
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard upon successful registration
    else:
        form = UserCreationForm()
    return render(request, 'webHost/web/website/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout