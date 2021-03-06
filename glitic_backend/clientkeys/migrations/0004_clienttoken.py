# Generated by Django 3.2.9 on 2021-11-16 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientkeys', '0003_auto_20211113_0244'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=16)),
                ('last_active', models.DateTimeField(auto_now=True)),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientkeys.clientkey')),
            ],
        ),
    ]
