# Generated by Django 3.2.12 on 2022-08-12 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0017_set_phone_fields_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidatepage',
            name='charge_changed',
            field=models.BooleanField(default=False, help_text='Charge changed from parlametria api to TSE 2022 csv data'),
        ),
        migrations.AddField(
            model_name='candidatepage',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'MASCULINO'), ('F', 'FEMININO')], max_length=1, null=True),
        ),
    ]