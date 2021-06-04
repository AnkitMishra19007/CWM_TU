from django.shortcuts import render

# Create your views here.


def dump(request):
    return render(request, 'dumpyards.html')


def stat(request):
    return render(request, 'stats.html')


def contact(request):
    return render(request, 'contacts.html')
