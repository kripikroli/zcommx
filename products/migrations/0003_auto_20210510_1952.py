# Generated by Django 3.2.1 on 2021-05-10 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_merchantuser_company_name'),
        ('products', '0002_productmedia'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subcategory_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products_subcategory', to='products.subcategory'),
        ),
        migrations.AlterField(
            model_name='product',
            name='merchant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_merchant', to='profiles.merchantuser'),
        ),
    ]
