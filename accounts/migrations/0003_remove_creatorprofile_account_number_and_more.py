# Generated by Django 5.0.1 on 2024-08-17 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_user_payoutaccount_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creatorprofile',
            name='account_number',
        ),
        migrations.AlterField(
            model_name='payoutaccount',
            name='account_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
