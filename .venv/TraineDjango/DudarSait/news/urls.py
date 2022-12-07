from django.urls import path
from . import views

urlpatterns = [
    # '' говорит, что мы на ссылке news
    path('', views.news, name='news'),
    path('create', views.news_create, name='create'), # news/create,
    # без news, так как прописано в config/url.py 'news'

    # В <> задается динамический параметр, после : указывается что именно. У
    # нас это pk - primary key
    # ТО есть мы указали, на такой url: /news/1,2...
    path('<int:pk>', views.NewsDetailView.as_view(), name='news-detail'),
    path('<int:pk>/update', views.NewsUpdateView.as_view(), name='news-update'),
    path('<int:pk>/delete', views.NewsDeleteView.as_view(), name='news-delete'),

]