from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView

#
# def index(request):
#     template = loader.get_template('index.html')
#     return HttpResponse(template.render({}, request))

#
# from django.shortcuts import render
# from django.http import HttpRequest, HttpResponse
# from django.views.generic.base import TemplateView
# from django.contrib.auth.mixins import LoginRequiredMixin
#
# def index(request: HttpRequest) -> HttpResponse:
#     return render(request, 'index.html')
#
# def about(request):
#     return render(request, 'about.html')
#
# def contact(request):
#     return render(request, 'contact.html')
#
# # для отображение новой страницы, разрешенной только регистрированным
# # пользователям
#
# class ProfileView(LoginRequiredMixin, TemplateView):
#
#     template_name = 'accounts/profile.html'