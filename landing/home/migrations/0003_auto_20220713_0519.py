# Generated by Django 3.2.12 on 2022-07-13 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('home', '0002_create_surveys_and_remove_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='landingpage',
            name='search_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Search image'),
        ),
        migrations.AddField(
            model_name='surveyspage',
            name='search_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Search image'),
        ),
    ]
