# Generated by Django 5.1.1 on 2024-10-14 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_usercourse_payment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
