from django.contrib.auth import authenticate
from django.shortcuts import render, HttpResponseRedirect
from .forms import SignupForm, Ewastes, RFPAuthForm
from .models import Ewaste
from django.contrib.auth import authenticate, login, logout
import datetime
# Create your views here.


def ewastes(request):
    if request.user.is_superuser:
        data = Ewaste.objects.all()
        print(data.values)
        return render(request, 'ewastes.html', {'data': data})
    else:
        if request.method == 'POST':
            form = Ewastes(request.POST, request.FILES)
            print(form.errors)
            if form.is_valid():
                a = datetime.date.today()
                nm = form.cleaned_data['name']
                em = form.cleaned_data['email']
                mo = form.cleaned_data['mobile']
                ad = form.cleaned_data['address']
                it = form.cleaned_data['item_name']
                id = form.cleaned_data['item_description']
                ii = form.cleaned_data['item_image']
                print(nm, em, mo)
                reg = Ewaste(name=nm, email=em, mobile=mo, address=ad,
                             item_name=it, item_description=id, item_image=ii, date=a)
                reg.save()
                form = Ewastes()
        else:
            form = Ewastes()
        return render(request, 'ewastes.html', {'form': form})


def logins(request):
    if request.method == 'POST':
        fm = RFPAuthForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/logwaste/profile/")
    else:
        fm = RFPAuthForm()
    return render(request, 'login.html', {'form': fm})


def signup(request):

    if request.method == 'POST':
        fm = SignupForm(request.POST)
        if fm.is_valid():
            fm.save()
            username = fm.cleaned_data['email']
            upass = fm.cleaned_data['password1']
            user = authenticate(username=username, password=upass)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/logwaste/profile/")
    else:
        fm = SignupForm()
    return render(request, 'signup.html', {'form': fm})


def profile(request):
    if request.user.is_authenticated:
        ew = request.user
        return render(request, 'profile.html', {'ew': ew})
    else:
        return HttpResponseRedirect('/logwaste/logins/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/logwaste/logins/')
