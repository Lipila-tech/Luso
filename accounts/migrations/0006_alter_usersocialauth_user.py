# Generated by Django 5.0.1 on 2024-09-27 13:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_usersocialauth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersocialauth',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
