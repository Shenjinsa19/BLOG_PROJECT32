# Generated by Django 5.2 on 2025-05-12 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_alter_post_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dislike',
            options={'verbose_name': 'Dislike', 'verbose_name_plural': 'Dislikes'},
        ),
    ]
