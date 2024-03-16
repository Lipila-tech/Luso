from django.shortcuts import render

def index(request):
    return render(request, 'patrons/index.html')

def contribute(request, user):
    return render(request, 'patrons/contribute.html')