# Generated by Django 2.1.5 on 2019-02-23 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Fixed Income', 'Fixed Income'), ('Equities', 'Equities'), ('Foreign Exchange', 'Foreign Exchange'), ('Derivatives', 'Derivatives')], max_length=266)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(choices=[('Region', 'Region'), ('RecordSet', 'RecordSet'), ('System', 'System')], max_length=266)),
            ],
        ),
        migrations.CreateModel(
            name='RecordSet',
            fields=[
                ('name', models.CharField(blank=True, choices=[('Orders', 'Orders'), ('Settlements', 'Settlements'), ('Customer Details', 'Customer Details'), ('Trades', 'Trades')], max_length=266, null=True)),
                ('id', models.CharField(max_length=266, primary_key=True, serialize=False)),
                ('dataContactEmail', models.EmailField(blank=True, max_length=254, null=True)),
                ('dataContactName', models.CharField(blank=True, max_length=266, null=True)),
                ('format', models.CharField(blank=True, choices=[('Archive record', 'Archive record'), ('Database record', 'Database record')], max_length=266, null=True)),
                ('availableFrom', models.CharField(blank=True, max_length=266, null=True)),
                ('availableTo', models.CharField(blank=True, max_length=266, null=True)),
                ('businessContactPhone', models.CharField(max_length=266)),
                ('EpochFrom', models.CharField(blank=True, max_length=266, null=True)),
                ('EpochTo', models.CharField(blank=True, max_length=266, null=True)),
                ('businessContactEmail', models.EmailField(blank=True, max_length=254, null=True)),
                ('dataContactPhone', models.CharField(blank=True, max_length=266, null=True)),
                ('businessContactName', models.CharField(blank=True, max_length=266)),
                ('extractionSLA', models.CharField(blank=True, max_length=266)),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neo_nodes_v6.Label')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('name', models.CharField(choices=[('AMER', 'AMER'), ('EMEA', 'EMEA'), ('APAC', 'APAC')], max_length=266)),
                ('id', models.CharField(max_length=266, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Relationships',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node1_id', models.CharField(max_length=266)),
                ('node2_id', models.CharField(max_length=266)),
                ('rel', models.CharField(max_length=266)),
                ('one_two_direction', models.BooleanField(default=False)),
                ('rel_properties', models.CharField(max_length=266)),
            ],
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('name', models.CharField(max_length=266)),
                ('ownerPhoneNumber', models.CharField(blank=True, max_length=266)),
                ('regions', models.CharField(max_length=266)),
                ('ownerName', models.CharField(blank=True, max_length=266)),
                ('id', models.CharField(max_length=266, primary_key=True, serialize=False)),
                ('businesses', models.CharField(max_length=266)),
                ('ownerEmail', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
    ]
