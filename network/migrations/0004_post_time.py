# Generated by Django 4.1.7 on 2023-06-05 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_social_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
