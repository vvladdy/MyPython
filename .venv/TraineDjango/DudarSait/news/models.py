from django.db import models

class Articles(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100)
    anons = models.CharField(verbose_name='Анонс', max_length=250)
    full_text = models.TextField(verbose_name='Статья')
    date = models.DateTimeField(verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    # для изменения новости update нужен метод
    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

