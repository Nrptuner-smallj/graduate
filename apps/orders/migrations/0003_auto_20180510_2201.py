# Generated by Django 2.0.2 on 2018-05-10 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_deliveryorder_add_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryorder',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='收货信息'),
        ),
    ]
