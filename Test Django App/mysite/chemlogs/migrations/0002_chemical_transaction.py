# Generated by Django 4.1.2 on 2022-10-20 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chemlogs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chemical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cas_num', models.CharField(max_length=12)),
                ('formula', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('safety', models.TextField()),
                ('barcode', models.BinaryField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('time', models.DateTimeField()),
                ('chemical', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chemlogs.chemical')),
            ],
        ),
    ]
