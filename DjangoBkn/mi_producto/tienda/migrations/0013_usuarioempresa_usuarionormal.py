# Generated by Django 5.2.1 on 2025-06-15 01:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0012_producto_categoria_repuesto_categoria'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('nombre_empresa', models.CharField(max_length=255)),
                ('rut_empresa', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator('^\\d{7,8}-[0-9kK]$', 'Ingrese un RUT válido.')])),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                
            ],
        ),
        migrations.CreateModel(
            name='UsuarioNormal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('rut', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator('^\\d{7,8}-[0-9kK]$', 'Ingrese un RUT válido.')])),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                
            ],
        ),
    ]
