# Generated by Django 4.1 on 2022-08-24 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsa_app', '0010_remove_question_is_solved_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='similar1',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='similar2',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]