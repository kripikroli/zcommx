# Generated by Django 3.2.1 on 2021-05-11 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_producttag'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.IntegerField(choices=[(1, 'BUY'), (2, 'SELL'), (3, 'SETUP')], default=1)),
                ('transaction_product_count', models.IntegerField(default=1)),
                ('transaction_description', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_transactions', to='products.product')),
            ],
        ),
    ]
