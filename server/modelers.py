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

    def get_values():
        categories = Categories.objects.all()
        cat_dict = dict()
        for category in categories:
            cat_dict[category.id_category] = category.category_name
        return cat_dict


class Clients(models.Model):
    id_client = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Clients'


class Computers(models.Model):
    id_computer = models.AutoField(primary_key=True)
    computer_serial = models.CharField(max_length=45)
    motherboard_serial = models.CharField(max_length=45, blank=True, null=True)
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
    f_sale = models.ForeignKey('Sales', models.DO_NOTHING, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Computers'

    def getDate(self):
        if self.date is None:
            return "N/A"
        else:
            return self.date.strftime('%Y-%m-%d %H:%M:%S')


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


class RamSizes(models.Model):
    id_ram_size = models.AutoField(primary_key=True)
    ram_size_text = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'RAM_sizes'


class Rams(models.Model):
    id_ram = models.AutoField(primary_key=True)
    ram_serial = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'RAMs'


class Sales(models.Model):
    id_sale = models.AutoField(primary_key=True)
    date_of_sale = models.DateField()
    f_id_client = models.ForeignKey(Clients, models.DO_NOTHING, db_column='f_id_client')

    class Meta:
        managed = False
        db_table = 'Sales'


class Testers(models.Model):
    id_tester = models.AutoField(primary_key=True)
    tester_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Testers'

    def get_values():
        testers = Testers.objects.all()
        tes_dict = dict()
        for tester in testers:
            tes_dict[tester.id_tester] = tester.tester_name
        return tes_dict


class Types(models.Model):
    id_type = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Types'

    def get_values():
        types = Types.objects.all()
        typ_dict = dict()
        for type in types:
            typ_dict[type.id_type] = type.type_name
        return typ_dict


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BatToComp(models.Model):
    id_bat_to_comp = models.AutoField(primary_key=True)
    f_id_computer_bat_to_com = models.ForeignKey(Computers, models.DO_NOTHING, db_column='f_id_computer_bat_to_com', blank=True, null=True)
    f_bat_bat_to_com = models.ForeignKey(Batteries, models.DO_NOTHING, db_column='f_bat_bat_to_com', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bat_to_comp'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class HddToComp(models.Model):
    id_hdd_to_comp = models.AutoField(primary_key=True)
    f_id_computer_hdd_to_com = models.ForeignKey(Computers, models.DO_NOTHING, db_column='f_id_computer_hdd_to_com', blank=True, null=True)
    f_id_hdd_hdd_to_com = models.ForeignKey(Hdds, models.DO_NOTHING, db_column='f_id_hdd_hdd_to_com', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hdd_to_comp'


class RamToComp(models.Model):
    id_ram_to_comp = models.AutoField(primary_key=True)
    f_id_computer_ram_to_com = models.ForeignKey(Computers, models.DO_NOTHING, db_column='f_id_computer_ram_to_com', blank=True, null=True)
    f_id_ram_ram_to_com = models.ForeignKey(Rams, models.DO_NOTHING, db_column='f_id_ram_ram_to_com', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ram_to_comp'
