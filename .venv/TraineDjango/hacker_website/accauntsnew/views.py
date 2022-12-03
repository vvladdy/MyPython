from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# для отображение новой страницы, разрешенной только регистрированным
# пользователям

class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = 'accounts/profile.html'