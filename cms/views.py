from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm


def cms_logout_view(request):
    logout(request)
    return redirect('cms:cms_login_view')

def cms_login_view(request):
    error_message = None
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('cms:cms_home')

        else:
            error_message = 'Oppsss... something went wrong'

    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'cms/login.html', context)

@login_required(login_url="/cms/")
def home_view(request):
    return render(request, 'cms/home.html')
