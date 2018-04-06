# Generated by Django 2.0.3 on 2018-04-04 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Computers',
            fields=[
                ('id_computer', models.AutoField(primary_key=True, serialize=False)),
                ('serial', models.CharField(max_length=45)),
                ('manufacturer', models.CharField(blank=True, max_length=45, null=True)),
                ('model', models.CharField(blank=True, max_length=45, null=True)),
                ('cpu', models.CharField(blank=True, max_length=45, null=True)),
                ('ram', models.CharField(blank=True, max_length=45, null=True)),
                ('gpu', models.CharField(blank=True, max_length=45, null=True)),
                ('hdd', models.CharField(blank=True, max_length=45, null=True)),
                ('diagonal', models.CharField(blank=True, max_length=10, null=True)),
                ('license', models.CharField(blank=True, max_length=3, null=True)),
                ('camera', models.CharField(blank=True, max_length=3, null=True)),
                ('cover', models.CharField(blank=True, max_length=45, null=True)),
                ('display', models.CharField(blank=True, max_length=45, null=True)),
                ('bezel', models.CharField(blank=True, max_length=45, null=True)),
                ('keyboard', models.CharField(blank=True, max_length=45, null=True)),
                ('mouse', models.CharField(blank=True, max_length=45, null=True)),
                ('sound', models.CharField(blank=True, max_length=45, null=True)),
                ('cdrom', models.CharField(blank=True, max_length=45, null=True)),
                ('battery', models.CharField(blank=True, max_length=45, null=True)),
                ('hdd_cover', models.CharField(blank=True, max_length=45, null=True)),
                ('ram_cover', models.CharField(blank=True, max_length=45, null=True)),
                ('other', models.CharField(blank=True, max_length=300, null=True)),
                ('tester', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('bios', models.CharField(blank=True, max_length=45, null=True)),
                ('computer_type', models.CharField(blank=True, max_length=45, null=True)),
                ('motherboard_serial', models.CharField(blank=True, max_length=45, null=True)),
                ('hdd_serial1', models.CharField(blank=True, max_length=45, null=True)),
                ('hdd_serial2', models.CharField(blank=True, max_length=45, null=True)),
                ('hdd_serial3', models.CharField(blank=True, max_length=45, null=True)),
                ('ram_serial1', models.CharField(blank=True, max_length=45, null=True)),
                ('ram_serial2', models.CharField(blank=True, max_length=45, null=True)),
                ('ram_serial3', models.CharField(blank=True, max_length=45, null=True)),
                ('ram_serial4', models.CharField(blank=True, max_length=45, null=True)),
                ('ram_serial5', models.CharField(blank=True, max_length=45, null=True)),
                ('ram_serial6', models.CharField(blank=True, max_length=45, null=True)),
                ('bat1_wear_out', models.CharField(blank=True, max_length=45, null=True)),
                ('bat1_expected_time', models.CharField(blank=True, max_length=45, null=True)),
                ('bat1_serial', models.CharField(blank=True, max_length=45, null=True)),
                ('bat2_wear_out', models.CharField(blank=True, max_length=45, null=True)),
                ('bat2_expected_time', models.CharField(blank=True, max_length=45, null=True)),
                ('bat2_serial', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'computers',
            },
        ),
    ]
