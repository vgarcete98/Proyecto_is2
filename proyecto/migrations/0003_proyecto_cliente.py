# Generated by Django 2.0.6 on 2019-05-26 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
        ('proyecto', '0002_teammember_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='clientes.Cliente'),
        ),
    ]
