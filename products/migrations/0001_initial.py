# Generated by Django 3.2.1 on 2021-05-05 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('thumbnail', models.ImageField(default='no_image.png', upload_to='category_thumbnails')),
                ('description', models.TextField(default='description here...')),
                ('is_active', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('short_description', models.TextField(default='description here...')),
                ('long_description', models.TextField(default='description here...')),
                ('brand', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.FloatField(help_text='in US dollars $')),
                ('is_active', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('merchant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='profiles.merchantuser')),
            ],
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('thumbnail', models.ImageField(default='no_image.png', upload_to='category_thumbnails')),
                ('description', models.TextField(default='description here...')),
                ('is_active', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='products.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductVariantItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_variant_items', to='products.product')),
                ('product_variant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='products.productvariant')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='products')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('details', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_details', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAbout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('details', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_abouts', to='products.product')),
            ],
        ),
    ]
