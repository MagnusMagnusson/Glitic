# Generated by Django 3.2.9 on 2021-11-07 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='exact',
        ),
        migrations.RemoveField(
            model_name='eventcounter',
            name='count',
        ),
        migrations.AddField(
            model_name='event',
            name='randsamp',
            field=models.IntegerField(default=1),
        ),
        migrations.CreateModel(
            name='Eventregister',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('note', models.CharField(blank=True, default='', max_length=64)),
                ('info', models.TextField(max_length=1024)),
                ('counter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventcounter')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Eventnote',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('note', models.CharField(blank=True, default='', max_length=64)),
                ('value', models.IntegerField(default=0)),
                ('counter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventcounter')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
