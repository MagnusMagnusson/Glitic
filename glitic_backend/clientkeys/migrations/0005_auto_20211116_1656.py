# Generated by Django 3.2.9 on 2021-11-16 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientkeys', '0004_clienttoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clienttoken',
            name='id',
        ),
        migrations.AlterField(
            model_name='clienttoken',
            name='token',
            field=models.CharField(max_length=16, primary_key=True, serialize=False),
        ),
    ]