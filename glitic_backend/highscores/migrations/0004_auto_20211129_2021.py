# Generated by Django 3.2.9 on 2021-11-29 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('highscores', '0003_auto_20211108_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='simplescore',
            name='clientid',
            field=models.CharField(default='N/A', max_length=16),
        ),
        migrations.AddField(
            model_name='simplescore',
            name='debug',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='simplescore',
            name='ip',
            field=models.GenericIPAddressField(default='127.0.0.1'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='simplescore',
            name='label',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
