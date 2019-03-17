# Generated by Django 2.1.5 on 2019-02-14 23:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attr_name', models.CharField(max_length=100)),
                ('attr_value', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='attribute',
            name='label_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neo_nodes_v2.Label'),
        ),
    ]
