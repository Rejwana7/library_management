# Generated by Django 5.0.1 on 2024-01-18 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_remove_comment_email_remove_comment_name_and_more'),
        ('transaction', '0002_alter_transaction_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book.book'),
        ),
    ]
