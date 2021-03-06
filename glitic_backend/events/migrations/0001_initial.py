# Generated by Django 3.2.9 on 2021-11-07 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=64)),
                ('cumulative', models.BooleanField(default=True)),
                ('time_split', models.BooleanField(default=True)),
                ('exact', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Eventcounter',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now=True)),
                ('count', models.IntegerField(default=0)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
