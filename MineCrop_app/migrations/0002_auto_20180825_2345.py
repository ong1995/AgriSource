# Generated by Django 2.0.2 on 2018-08-25 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MineCrop_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='minedtweet',
            old_name='name',
            new_name='username',
        ),
    ]
