# Generated by Django 3.2.5 on 2021-07-02 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя пользователя')),
                ('phone', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('address', models.CharField(max_length=100, verbose_name='Адрес')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.product', verbose_name='Продукт')),
            ],
        ),
    ]
