# Generated by Django 5.0.6 on 2024-07-29 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_bids_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='amount',
            field=models.IntegerField(default='0'),
        ),
    ]
