# Generated by Django 4.2.3 on 2023-11-11 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_ordercart_ordercartitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordercart',
            old_name='order_date',
            new_name='date',
        ),
    ]
