# Generated by Django 4.1.7 on 2023-03-28 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dab', '0002_traitementtable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='traitement',
            name='tables',
        ),
    ]
