# Generated by Django 4.2.3 on 2023-11-11 04:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_ordercart_order_date_remove_ordercart_phone_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordercartitem',
            name='dish',
        ),
        migrations.RemoveField(
            model_name='ordercartitem',
            name='ordercart',
        ),
        migrations.DeleteModel(
            name='OrderCart',
        ),
        migrations.DeleteModel(
            name='OrderCartItem',
        ),
    ]