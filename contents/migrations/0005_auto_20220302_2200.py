# Generated by Django 3.0.5 on 2022-03-02 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0004_comment_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='letter',
            old_name='created_at',
            new_name='published_at',
        ),
        migrations.RemoveField(
            model_name='letter',
            name='is_hot',
        ),
        migrations.AddField(
            model_name='letter',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='letter'),
        ),
    ]
