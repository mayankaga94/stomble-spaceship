# Generated by Django 3.1.5 on 2021-01-19 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
                ('planet', models.CharField(max_length=255)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Spaceship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('model_name', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[('decomissioned', 'decomissioned'), ('maintenance', 'maintenance'), ('operational', 'operational')], default='operational', max_length=13)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.location')),
            ],
        ),
        migrations.AddConstraint(
            model_name='location',
            constraint=models.UniqueConstraint(fields=('city', 'planet'), name='unique_location'),
        ),
    ]
