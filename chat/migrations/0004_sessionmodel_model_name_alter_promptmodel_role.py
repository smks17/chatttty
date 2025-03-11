# Generated by Django 4.2.9 on 2025-03-11 19:50

from django.db import migrations, models
import lib.llm.models.mistral_api


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_sessionmodel_updated_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionmodel',
            name='model_name',
            field=models.CharField(choices=[(lib.llm.models.mistral_api.MistralAPI, 'Mistral')], default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='promptmodel',
            name='role',
            field=models.CharField(choices=[('system', 'System'), ('user', 'User'), ('assistant', 'Assistant')], max_length=20),
        ),
    ]
