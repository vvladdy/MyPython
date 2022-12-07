from django.shortcuts import render, redirect
from .models import Articles
from .forms import ArticlesForm
from django.views.generic import DetailView, UpdateView, DeleteView

# создаем класс для динамической страницы

class NewsDetailView(DetailView):
    model = Articles # обрщение к таблице в БД
    template_name = 'news/details_view.html'
    context_object_name = 'article' # ключ, по которому мы передаем объект
    # внутрь шаблона html

class NewsUpdateView(UpdateView):
    model = Articles
    template_name = 'news/create.html'
    form_class = ArticlesForm

class NewsDeleteView(DeleteView):
    model = Articles
    success_url = '/news'
    template_name = 'news/news-delete.html'
    context_object_name = 'article'


def news(request):
    # получаем все записи из базы данных из таблицы Articles
    # news = Articles.objects.all()

    # Получим из быза данных элементы отсортированные по заданному полю
    # 'data' сортировка по дате старые -> новые
    # '-data' сортировка по дате  новые -> старые
    news = Articles.objects.order_by('date')

    context = {
        'news': news,
    }
    return render(request, 'news/news.html', context)

def news_create(request):
    # делаем проверку, если метод передачи данных post, указано в create.html
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            # можно так без else и error
            # title = form.cleaned_data['title']
            # anons = form.cleaned_data['anons']
            # text = form.cleaned_data['full_text']
            # date = form.cleaned_data['date']
            form.save()
            # если все корректно, то переадрессация на 'news'
            return redirect('news')
        else:
            error = 'Форма заполнена не верно'
    form = ArticlesForm()

    context = {
        'form': form,
        'error': error
    }
    return render(request, 'news/create.html', context)
    #
    # from haker_website
    # if request.method == 'GET':
    #     form = ContactForm()
    # elif request.method == 'POST':
    #     form = ContactForm(request.POST)
    #     if form.is_valid():
    #         name = form.cleaned_data['name']
    #         email = form.cleaned_data['email']
    #         message = form.cleaned_data['message']
    #         send_mail(f'{name} sent email', message, email, 'hackerwebsite@gmail.com')
    #         return render(request, 'contact.html', {'form': form, 'success':
    #             True})
    # else:
    #     raise NotImplementedError