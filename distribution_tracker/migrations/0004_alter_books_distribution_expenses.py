# Generated by Django 4.2.9 on 2024-06-04 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distribution_tracker', '0003_books_book_auth_name_books_book_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='distribution_expenses',
            field=models.IntegerField(),
        ),
    ]
