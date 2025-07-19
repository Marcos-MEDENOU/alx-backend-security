from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ratelimit.decorators import ratelimit
from django.contrib.auth.forms import AuthenticationForm

@ratelimit(key='ip', rate='5/m', method=['POST'], group='login')
@ratelimit(key='ip', rate='10/m', method=['POST'], group='login', authenticated=True)
def login_view(request):
    if request.method == 'POST':
        if getattr(request, 'limited', False):
            return HttpResponse(
                'Too many login attempts. Please try again later.',
                status=429
            )
        
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})