# Generated by Django 2.1.5 on 2019-02-14 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neo_nodes_v4', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodeid',
            name='node_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
