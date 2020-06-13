# Generated by Django 2.2.2 on 2020-06-10 19:43

import directions.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrendsDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=300, verbose_name='Заголовок')),
                ('file', models.FileField(blank=True, default='', upload_to='trends/', validators=[directions.validators.validate_documents], verbose_name='Файл')),
                ('customOrder', models.PositiveIntegerField(default=0, verbose_name='Перетащите на нужное место')),
                ('id_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directions.Trend')),
            ],
            options={
                'verbose_name_plural': 'Документы',
                'verbose_name': 'Документ',
                'ordering': ['customOrder'],
            },
        ),
    ]
