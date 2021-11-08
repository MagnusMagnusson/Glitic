# Generated by Django 3.2.9 on 2021-11-05 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Simpletable',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('ascending_primary', models.BooleanField(default=True)),
                ('ascending_secondary', models.BooleanField(default=True)),
                ('user_unique', models.BooleanField(default=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game')),
            ],
        ),
        migrations.CreateModel(
            name='Simplescore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary', models.FloatField()),
                ('secondary', models.FloatField()),
                ('label', models.CharField(max_length=16)),
                ('date', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(max_length=128)),
                ('userid', models.CharField(max_length=128)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='highscores.simpletable')),
            ],
        ),
    ]
