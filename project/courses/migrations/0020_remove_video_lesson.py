# Generated by Django 5.1.1 on 2024-10-18 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0019_course_product_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='lesson',
        ),
    ]
