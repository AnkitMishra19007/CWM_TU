# Generated by Django 3.2.3 on 2021-06-18 10:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('logwaste', '0011_delete_pickedewaste'),
    ]

    operations = [
        migrations.AddField(
            model_name='ewaste',
            name='picked',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ewaste',
            name='picked_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
