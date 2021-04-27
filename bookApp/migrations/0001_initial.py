# Generated by Django 3.2 on 2021-04-23 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='Photos/%Y/%d')),
                ('info', models.TextField(null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Authors',
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Genres',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('ISBN', models.CharField(max_length=37, primary_key=True, serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=50)),
                ('published', models.DateField(blank=True, null=True)),
                ('pages', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to='photos')),
                ('pdf', models.FileField(upload_to='PDF')),
                ('book_excerpt', models.TextField(blank=True, null=True)),
                ('authors', models.ManyToManyField(blank=True, related_name='book', to='bookApp.Author')),
                ('genres', models.ManyToManyField(related_name='book', to='bookApp.Genre')),
            ],
            options={
                'verbose_name_plural': 'Books',
                'ordering': ['title'],
            },
        ),
    ]
