# Generated by Django 5.1.1 on 2024-10-16 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_answer_remove_question_question_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='text',
        ),
        migrations.AddField(
            model_name='question',
            name='question_text',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
