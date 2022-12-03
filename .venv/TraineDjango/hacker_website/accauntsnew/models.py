from django.db import models
from django.contrib.auth.models import User

class UserInterests(models.Model):
    name = models.CharField(max_length=64, unique=True)
    normalized_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    # class Meta:
    #     verbose_name = 'Интересы'
    #     verbose_name_plural = 'Интересы'


class UserPersona(models.Model):
    name = models.CharField(max_length=64, unique=True)
    normalized_name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'


# Create your models here.
class UserProfile(models.Model):
    # owner
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile')
    # settings
    is_full_name_displayed = models.BooleanField(default=True)

    # details
    bio = models.CharField(max_length=500, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    persona = models.ForeignKey(UserPersona,
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True)
    interests = models.ManyToManyField(UserInterests, blank=True)

    # interests = request.user.profile.interests.all() - таким образом для
    # html-файла формируется запрос на вывод инф-ции на странику DjangoORm

