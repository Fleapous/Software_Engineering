# Generated by Django 4.2.11 on 2024-04-13 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space_booking', '0004_alter_rating_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='comment',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='score',
            new_name='rating',
        ),
    ]
