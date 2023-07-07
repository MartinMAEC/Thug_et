# Generated by Django 4.2.2 on 2023-06-25 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('rut', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('edad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artista', models.CharField(default='Desconocido', max_length=50)),
                ('nombreprod', models.CharField(max_length=50)),
                ('precio', models.IntegerField()),
                ('descripcion', models.TextField()),
                ('imagen', models.ImageField(null=True, upload_to='productos')),
            ],
        ),
    ]
