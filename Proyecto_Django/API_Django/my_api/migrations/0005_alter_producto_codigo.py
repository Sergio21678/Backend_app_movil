# Generated by Django 5.1.2 on 2025-01-14 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_api', '0004_alter_movimiento_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='codigo',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
