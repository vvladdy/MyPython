from django.shortcuts import render

def index(request):
    context = {
        'title': 'Главная страница',
        'values': ['maining', 'button', '123'],
        'obj': {
            'car': 'BMW',
            'age': 18,
            'hobby': 'football'
        }
    }
    return render(request, 'main/index.html', context)

def about(request):
    return render(request, 'main/about.html')




# from django.http import HttpResponse
# def about(request):
#     return HttpResponse('<h2>Page ABOUT</h2>')