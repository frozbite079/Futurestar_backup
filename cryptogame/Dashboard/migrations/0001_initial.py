# Generated by Django 5.0.6 on 2024-08-03 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MetaUser',
            fields=[
                ('address', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('nickname', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'db_table': 'MetaUser',
            },
        ),
    ]