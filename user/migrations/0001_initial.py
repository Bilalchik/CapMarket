# Generated by Django 5.0.4 on 2024-05-12 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone_number', models.CharField(max_length=123, unique=True)),
                ('username', models.CharField(max_length=123)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='media/user_cover')),
                ('address', models.CharField(blank=True, max_length=223, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
