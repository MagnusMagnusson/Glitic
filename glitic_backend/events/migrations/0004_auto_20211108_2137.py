# Generated by Django 3.2.9 on 2021-11-08 21:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20211108_1628'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventcounter',
            options={'verbose_name': 'Event Group', 'verbose_name_plural': 'Event Groups'},
        ),
        migrations.AlterModelOptions(
            name='eventnote',
            options={'verbose_name': 'Event Counter', 'verbose_name_plural': 'Event Counters'},
        ),
        migrations.AlterModelOptions(
            name='eventregister',
            options={'verbose_name': 'Event Log', 'verbose_name_plural': 'Event Logs'},
        ),
    ]
