# Generated by Django 4.1.2 on 2023-11-01 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chemlogs', '0015_delete_transactionedit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('T', 'TRANSACT'), ('N', 'NEW')], default='T', max_length=1),
        ),
    ]
