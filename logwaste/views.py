from django.contrib.auth import authenticate
from django.shortcuts import render, HttpResponseRedirect
from .forms import SignupForm, Ewastes, RFPAuthForm, EditForm
from .models import Bills, Ewaste, MyUser
from django.contrib.auth import authenticate, login, logout
import datetime
from django.db import connection
from django.contrib import messages
# Create your views here.


def ewastes(request):
    if request.user.is_superuser:
        data = Ewaste.objects.filter(picked=False)
        return render(request, 'ewastes.html', {'data': data})
    else:
        if request.method == 'POST':
            form = Ewastes(request.POST, request.FILES)
            if form.is_valid():
                a = datetime.date.today()
                nm = form.cleaned_data['name']
                em = form.cleaned_data['email']
                mo = form.cleaned_data['mobile']
                ad = form.cleaned_data['address']
                it = form.cleaned_data['item_name']
                id = form.cleaned_data['item_description']
                ii = form.cleaned_data['item_image']
                reg = Ewaste(name=nm, email=em, mobile=mo, address=ad,
                             item_name=it, item_description=id, item_image=ii, date=a, picked=False, picked_date=a)
                reg.save()
                form = Ewastes()
                messages.add_message(
                    request, messages.SUCCESS, "The form has been successfully submitted, You will be contacted soon!")
        else:
            form = Ewastes()
        return render(request, 'ewastes.html', {'form': form})


def ewaste_handle(request, id):
    # Reject
    if request.method == 'POST':
        d = Ewaste.objects.get(pk=id)
        d.delete()
        messages.add_message(
            request, messages.INFO, "The selected E-waste has been rejected. The related user will be notified about it!")
        return HttpResponseRedirect('/logwaste/ewastes/')
    # Pickup
    else:
        d = Ewaste.objects.get(pk=id)
        a = datetime.date.today()
        d.picked = True
        d.picked_date = a
        d.save()
        messages.add_message(
            request, messages.SUCCESS, "The selecetd E-waste has been successfully picked and will be sent to process soon!")
        return HttpResponseRedirect('/logwaste/ewastes/')


def picked(request):
    data = Ewaste.objects.filter(picked=True)
    return render(request, 'picked.html', {'data': data})


def logins(request):
    print(request.session.get_expire_at_browser_close())
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


def edit(request):
    print("Called Edit")
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = MyUser.objects.get(pk=request.user.id)
            fm = EditForm(request.POST, instance=pi)
            if fm.is_valid():
                fm.save()
                return HttpResponseRedirect("/logwaste/profile/")
        else:
            pi = MyUser.objects.get(pk=request.user.id)
            fm = EditForm(instance=pi)
        return render(request, 'edit.html', {'fm': fm})
    else:
        return HttpResponseRedirect('/logwaste/logins/')


def delete_id(request):
    if request.method == 'POST':
        d = MyUser.objects.get(pk=request.user.id)
        d.delete()
        messages.add_message(
            request, messages.INFO, "Your ID has been successfully deleted. Signup again to access more features!")
        return HttpResponseRedirect('/logwaste/logins/')


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def profile(request):
    print("Called profile")
    if request.user.is_superuser:
        # how many users are there
        d1 = MyUser.objects.all().filter(is_superuser=False)
        # below we are joining two tables by writing pure SQL query. We use dictfetchall for our help
        cursor = connection.cursor()
        cursor.execute(
            "SELECT logwaste_myuser.id,logwaste_myuser.full_name, logwaste_bills.bill_amount, logwaste_bills.bill_month, logwaste_bills.bill_date FROM logwaste_myuser JOIN logwaste_bills ON logwaste_myuser.id=logwaste_bills.bill_id")
        data = dictfetchall(cursor)
        ew = request.user
        return render(request, 'profile.html', {'ew': ew, 'data': data, 'd1': d1})

    # Not superuser
    elif request.user.is_authenticated:
        # fetching bills data
        data = Bills.objects.filter(bill_id=request.user.id)
        if request.method == 'POST':
            month = request.POST['month']
            amount = request.POST['amount']
            b_id = request.user.id
            a = datetime.date.today()
            #saving in database
            reg = Bills(bill_id=b_id, bill_amount=amount,
                        bill_month=month, bill_date=a)
            reg.save()
            # updating bills data
            data = Bills.objects.filter(bill_id=request.user.id)
        ew = request.user
        return render(request, 'profile.html', {'ew': ew, 'data': data})
    else:
        return HttpResponseRedirect('/logwaste/logins/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/logwaste/logins/')
