# Generated by Django 4.1.2 on 2023-04-26 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chemlogs', '0011_transactionedit'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.CharField(default='stippett', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionedit',
            name='user',
            field=models.CharField(default='stippett', max_length=50),
            preserve_default=False,
        ),
    ]
