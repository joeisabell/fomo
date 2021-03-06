# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 03:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('codename', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_token', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('charge', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('brand', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subdir', models.TextField()),
                ('alttext', models.TextField(null=True)),
                ('mimetype', models.TextField(null=True)),
                ('is_primary', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_date', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SaleLineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_item_type', models.CharField(default='PRODUCT', max_length=50)),
                ('quantity', models.IntegerField(default=0, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField(default=1)),
                ('qty_updated_date', models.DateTimeField(auto_now=True)),
                ('purchase_date', models.DateTimeField(null=True)),
                ('remove_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ViewHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_date', models.DateTimeField(auto_now_add=True)),
                ('added_to_cart', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BulkProduct',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='catalog.Product')),
                ('quantity', models.IntegerField(default=0, null=True)),
                ('reorder_point', models.IntegerField(default=0, null=True)),
                ('reorder_quantity', models.IntegerField(default=0, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('catalog.product',),
        ),
        migrations.CreateModel(
            name='RentalProduct',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='catalog.Product')),
                ('serial_number', models.TextField(blank=True, null=True)),
                ('sold', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('catalog.product',),
        ),
        migrations.CreateModel(
            name='UniqueProduct',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='catalog.Product')),
                ('serial_number', models.TextField(blank=True, null=True)),
                ('sold', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('catalog.product',),
        ),
        migrations.AddField(
            model_name='viewhistory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='view_history', to='catalog.Product'),
        ),
        migrations.AddField(
            model_name='viewhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='view_history', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shoppingcartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Product'),
        ),
        migrations.AddField(
            model_name='shoppingcartitem',
            name='shopping_cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='catalog.ShoppingCart'),
        ),
        migrations.AddField(
            model_name='salelineitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Product'),
        ),
        migrations.AddField(
            model_name='salelineitem',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='line_items', to='catalog.Sale'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalog.Product'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_catalog.product_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='payment',
            name='sale',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='catalog.Sale'),
        ),
    ]
