# Generated by Django 2.2.2 on 2020-04-17 12:44

from django.db import migrations, models
import django.db.models.deletion
import image_cropping.fields
import main.models
import main.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Main',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(blank=True, default='', upload_to=main.models.Main.user_directory_path, validators=[main.validators.validate_image], verbose_name='Баннер')),
                ('logo', models.ImageField(blank=True, default='', upload_to=main.models.Main.user_directory_path, validators=[main.validators.validate_image], verbose_name='Лого')),
                ('copyright', models.TextField(default='', max_length=300, verbose_name='Копирайт')),
            ],
            options={
                'verbose_name_plural': 'Главные',
                'verbose_name': 'Главная',
            },
        ),
        migrations.CreateModel(
            name='SocialNet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vk', models.CharField(default='', max_length=101, verbose_name='Вконтакте')),
                ('instagram', models.CharField(default='', max_length=101, verbose_name='Instagram')),
                ('youtube', models.CharField(default='', max_length=101, verbose_name='YouTube')),
                ('facebook', models.CharField(default='', max_length=101, verbose_name='Facebook')),
                ('id_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='socialnets', to='main.Main')),
            ],
            options={
                'verbose_name_plural': 'Социальные сети',
                'verbose_name': 'Социальные сети',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default='', max_length=101, verbose_name='Ссылка')),
                ('customOrder', models.PositiveIntegerField(default=0, verbose_name='Перетащите на нужное место')),
                ('imageOld', models.ImageField(blank=True, default='', upload_to=main.models.Partner.user_directory_path, validators=[main.validators.validate_image], verbose_name='Картинка')),
                ('image', image_cropping.fields.ImageRatioField('imageOld', '50x50', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text='Выберите область для отображения картинки', hide_image_field=False, size_warning=True, verbose_name='Отображение картинки')),
                ('id_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partners', to='main.Main')),
            ],
            options={
                'ordering': ['customOrder'],
                'verbose_name_plural': 'Партнеры',
                'verbose_name': 'Партнер',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=30, verbose_name='Название элемента меню')),
                ('path', models.CharField(default='', max_length=101, verbose_name='Путь')),
                ('id_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu', to='main.Main')),
            ],
            options={
                'verbose_name_plural': 'Меню',
                'verbose_name': 'Меню',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=51, verbose_name='Заголовок')),
                ('phone', models.CharField(default='', max_length=20, verbose_name='Телефон')),
                ('email', models.CharField(default='', max_length=101, verbose_name='Почта')),
                ('address', models.CharField(default='', max_length=301, verbose_name='Адрес')),
                ('map', models.CharField(blank=True, default='', max_length=1501, verbose_name='Ссылка на яндекс-карту')),
                ('id_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='main.Main')),
            ],
            options={
                'verbose_name_plural': 'Контакты',
                'verbose_name': 'Контакт',
            },
        ),
    ]
