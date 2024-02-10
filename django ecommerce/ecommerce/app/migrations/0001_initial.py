# Generated by Django 5.0 on 2024-01-23 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('selling_price', models.FloatField()),
                ('discount_price', models.FloatField()),
                ('description', models.TextField(max_length=250)),
                ('composition', models.TextField(default='')),
                ('prodapp', models.TextField(default='')),
                ('category', models.CharField(choices=[('tshirt', 'tshirt'), ('wintertshirt', 'wintertshirt'), ('summertshirt', 'summertshirt'), ('winterjacket', 'winterjacket'), ('dailyshoes', 'dailyshoes'), ('jeans', 'jeans')], max_length=20)),
                ('product_image', models.ImageField(upload_to='product')),
            ],
        ),
    ]
