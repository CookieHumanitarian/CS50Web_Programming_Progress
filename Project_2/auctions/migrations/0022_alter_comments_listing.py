# Generated by Django 5.0.6 on 2024-08-02 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_rename_title_comments_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='listing',
            field=models.TextField(),
        ),
    ]
