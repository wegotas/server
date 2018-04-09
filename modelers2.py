# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bioses(models.Model):
    id_bios = models.AutoField(primary_key=True)
    bios_text = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'BIOSes'


class Batteries(models.Model):
    id_battery = models.AutoField(primary_key=True)
    serial = models.CharField(max_length=45)
    wear_out = models.CharField(max_length=45)
    expected_time = models.CharField(max_length=45)
    f_id_computer_battery = models.ForeignKey('Computers', models.DO_NOTHING, db_column='f_id_computer_battery', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Batteries'


class Cpus(models.Model):
    id_cpu = models.AutoField(primary_key=True)
    cpu_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'CPUs'


class CameraOptions(models.Model):
    id_camera_options = models.AutoField(db_column='id_ camera_options', primary_key=True)  # Field renamed to remove unsuitable characters.
    option_name = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'Camera_options'


class Categories(models.Model):
    id_category = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Categories'


class Computers(models.Model):
    id_computer = models.AutoField(primary_key=True)
    computer_serial = models.CharField(max_length=45)
    f_type = models.ForeignKey('Types', models.DO_NOTHING, blank=True, null=True)
    f_category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    f_manufacturer = models.ForeignKey('Manufacturers', models.DO_NOTHING, blank=True, null=True)
    f_model = models.ForeignKey('Models', models.DO_NOTHING, blank=True, null=True)
    f_cpu = models.ForeignKey(Cpus, models.DO_NOTHING, blank=True, null=True)
    f_gpu = models.ForeignKey('Gpus', models.DO_NOTHING, blank=True, null=True)
    f_ram_size = models.ForeignKey('RamSizes', models.DO_NOTHING, blank=True, null=True)
    f_hdd_size = models.ForeignKey('HddSizes', models.DO_NOTHING, blank=True, null=True)
    f_diagonal = models.ForeignKey('Diagonals', models.DO_NOTHING, blank=True, null=True)
    f_license = models.ForeignKey('Licenses', models.DO_NOTHING, blank=True, null=True)
    f_camera = models.ForeignKey(CameraOptions, models.DO_NOTHING, blank=True, null=True)
    cover = models.CharField(max_length=45, blank=True, null=True)
    display = models.CharField(max_length=45, blank=True, null=True)
    bezel = models.CharField(max_length=45, blank=True, null=True)
    keyboard = models.CharField(max_length=45, blank=True, null=True)
    mouse = models.CharField(max_length=45, blank=True, null=True)
    sound = models.CharField(max_length=45, blank=True, null=True)
    cdrom = models.CharField(max_length=45, blank=True, null=True)
    hdd_cover = models.CharField(max_length=45, blank=True, null=True)
    ram_cover = models.CharField(max_length=45, blank=True, null=True)
    other = models.CharField(max_length=300, blank=True, null=True)
    f_tester = models.ForeignKey('Testers', models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    f_bios = models.ForeignKey(Bioses, models.DO_NOTHING, blank=True, null=True)
    f_motherboard = models.ForeignKey('Motherboards', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Computers'


class Diagonals(models.Model):
    id_diagonal = models.AutoField(primary_key=True)
    diagonal_text = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Diagonals'


class Gpus(models.Model):
    id_gpu = models.AutoField(primary_key=True)
    gpu_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'GPUs'


class HddSizes(models.Model):
    id_hdd_sizes = models.AutoField(primary_key=True)
    hdd_size_text = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'HDD_sizes'


class Hdds(models.Model):
    id_hdd = models.AutoField(primary_key=True)
    hdd_serial = models.CharField(max_length=45)
    f_id_computer_hdd = models.ForeignKey(Computers, models.DO_NOTHING, db_column='f_id_computer_hdd', blank=True, null=True)
    f_id_computer = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HDDs'


class Licenses(models.Model):
    id_license = models.AutoField(primary_key=True)
    license_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Licenses'


class Manufacturers(models.Model):
    id_manufacturer = models.AutoField(primary_key=True)
    manufacturer_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Manufacturers'


class Models(models.Model):
    id_model = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Models'


class Motherboards(models.Model):
    id_motherboard = models.AutoField(primary_key=True)
    motherboard_serial = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Motherboards'


class RamSizes(models.Model):
    id_ram_size = models.AutoField(primary_key=True)
    ram_size_text = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'RAM_sizes'


class Rams(models.Model):
    id_ram = models.AutoField(primary_key=True)
    ram_serial = models.CharField(max_length=45)
    f_id_computer_ram = models.ForeignKey(Computers, models.DO_NOTHING, db_column='f_id_computer_ram', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RAMs'


class Testers(models.Model):
    id_tester = models.AutoField(primary_key=True)
    tester_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Testers'


class Types(models.Model):
    id_type = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Types'
