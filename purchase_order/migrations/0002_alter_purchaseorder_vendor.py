# Generated by Django 5.0.4 on 2024-05-02 11:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0001_initial'),
        ('vendor_management', '0003_alter_historicalperformance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_orders', to='vendor_management.vendor'),
        ),
    ]