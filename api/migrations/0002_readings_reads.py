# Generated by Django 2.0.1 on 2018-01-31 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='readings',
            name='reads',
            field=models.TextField(blank=True, null=True),
        ),
    ]