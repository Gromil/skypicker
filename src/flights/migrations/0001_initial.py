# Generated by Django 3.1.4 on 2022-04-05 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fly_from', models.CharField(max_length=3)),
                ('fly_to', models.CharField(max_length=3)),
                ('fly_date', models.DateField()),
                ('min_price', models.IntegerField()),
                ('booking_token', models.CharField(max_length=1024)),
                ('valid', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]