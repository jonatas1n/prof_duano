# Generated by Django 3.2.25 on 2024-06-04 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('wagtailredirects', '0007_add_autocreate_fields'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('questions', '0002_questionlist'),
    ]

    operations = [
        migrations.DeleteModel(
            name='QuestionsIndex',
        ),
    ]
