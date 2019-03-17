# Generated by Django 2.1.5 on 2019-02-24 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neo_nodes_v6', '0004_auto_20190224_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='name',
            field=models.CharField(choices=[('Foreign Exchange', 'Foreign Exchange'), ('Fixed Income', 'Fixed Income'), ('Derivatives', 'Derivatives'), ('Equities', 'Equities')], max_length=266),
        ),
        migrations.AlterField(
            model_name='label',
            name='label',
            field=models.CharField(choices=[('System', 'System'), ('Region', 'Region'), ('RecordSet', 'RecordSet')], max_length=266),
        ),
        migrations.AlterField(
            model_name='recordset',
            name='name',
            field=models.CharField(blank=True, choices=[('Trades', 'Trades'), ('Settlements', 'Settlements'), ('Customer Details', 'Customer Details'), ('Orders', 'Orders')], max_length=266, null=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(choices=[('APAC', 'APAC'), ('AMER', 'AMER'), ('EMEA', 'EMEA')], max_length=266),
        ),
    ]