# Generated by Django 4.1.7 on 2023-04-04 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addDatabase', '0005_alter_database_schema'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='database',
            name='host',
        ),
        migrations.RemoveField(
            model_name='database',
            name='service',
        ),
        migrations.AddField(
            model_name='database',
            name='dsn',
            field=models.CharField(default=None, max_length=150),
        ),
    ]