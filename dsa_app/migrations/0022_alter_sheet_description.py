# Generated by Django 4.1 on 2022-08-25 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsa_app', '0021_question_is_solved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheet',
            name='description',
            field=models.TextField(max_length=200),
        ),
    ]
