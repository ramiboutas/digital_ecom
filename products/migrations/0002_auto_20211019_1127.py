# Generated by Django 3.2.8 on 2021-10-19 11:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(help_text='Unique value for product page URL, created from name.', unique=True)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('meta_keywords', models.CharField(help_text='Comma-delimited set of SEO keywords for meta tag', max_length=255, verbose_name='Meta Keywords')),
                ('meta_description', models.CharField(help_text='Content for description meta tag', max_length=255, verbose_name='Meta Description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='type',
        ),
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_description',
            field=models.CharField(default=django.utils.timezone.now, help_text='Content for description meta tag', max_length=255, verbose_name='Meta Description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='meta_keywords',
            field=models.CharField(default=django.utils.timezone.now, help_text='Comma-delimited set of SEO keywords for meta tag', max_length=255, verbose_name='Meta Keywords'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='old_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(related_name='products', to='products.Category'),
        ),
    ]