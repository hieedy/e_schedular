# Generated by Django 4.1 on 2022-09-03 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminuser',
            name='profile_picture_url',
        ),
        migrations.AddField(
            model_name='adminuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='adminuser',
            name='password',
            field=models.CharField(default=123, max_length=20),
            preserve_default=False,
        ),
    ]
