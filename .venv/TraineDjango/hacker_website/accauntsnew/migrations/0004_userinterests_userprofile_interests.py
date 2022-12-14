# Generated by Django 4.1.1 on 2022-11-29 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accauntsnew', '0003_alter_userpersona_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInterests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('normalized_name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='interests',
            field=models.ManyToManyField(blank=True, to='accauntsnew.userinterests'),
        ),
    ]
