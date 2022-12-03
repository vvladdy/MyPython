from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')
#
# def contact(request):
#     return render(request, 'contact.html')
