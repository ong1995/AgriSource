# Generated by Django 2.0.2 on 2018-08-25 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MineCrop_app', '0005_auto_20180826_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
