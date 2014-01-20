from django.shortcuts import render

def index(request):
    return render(request, 'about/index.html', {})

def cv(request):
    return render(request, 'about/cv.html', {})
