# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import FileExtensionValidator


class Bioses(models.Model):
    id_bios = models.AutoField(primary_key=True)
    bios_text = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'BIOSes'


class Batteries(models.Model):
    id_battery = models.AutoField(primary_key=True)
    serial = models.CharField(max_length=45)
    wear_out = models.CharField(max_length=45)
    expected_time = models.CharField(max_length=45)
    model = models.CharField(max_length=45, blank=True, null=True)
    current_wh = models.CharField(max_length=45, blank=True, null=True)
    maximum_wh = models.CharField(max_length=45, blank=True, null=True)
    factory_wh = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Batteries'


class Cpus(models.Model):
    id_cpu = models.AutoField(primary_key=True)
    cpu_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'CPUs'


class CameraOptions(models.Model):
    id_camera_options = models.AutoField(db_column='id_ camera_options', primary_key=True)  # Field renamed to remove unsuitable characters.
    option_name = models.CharField(max_length=6)

    class Meta:
        managed = True
        db_table = 'Camera_options'


class Categories(models.Model):
    id_category = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=45)
    permanent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Categories'

    def get_values():
        categories = Categories.objects.all()
        cat_dict = dict()
        for category in categories:
            cat_dict[category.id_category] = category.category_name
        return cat_dict


class ChargerCategories(models.Model):
    charger_category_id = models.AutoField(primary_key=True)
    watts = models.IntegerField(blank=True, null=True)
    acinvoltsmin = models.DecimalField(db_column='ACinVoltsMin', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    acinvoltsmax = models.DecimalField(db_column='ACinVoltsMax', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    acinampers = models.DecimalField(db_column='ACinAmpers', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    acinhzmin = models.IntegerField(db_column='ACinHzMin', blank=True, null=True)  # Field name made lowercase.
    acinhzmax = models.IntegerField(db_column='ACinHzMax', blank=True, null=True)  # Field name made lowercase.
    dcoutvoltsmin = models.DecimalField(db_column='DCoutVoltsMin', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    dcoutvoltsmax = models.DecimalField(db_column='DCoutVoltsMax', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    dcoutampers = models.DecimalField(db_column='DCoutAmpers', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    connector_inner_diameter = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    connector_outer_diameter = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    connector_contacts_qty = models.IntegerField(blank=True, null=True)
    originality_status = models.IntegerField(blank=True, null=True, default=False)
    used_status = models.IntegerField(blank=True, null=True, default=True)
    connector_type = models.CharField(max_length=45, blank=True, null=True)
    f_manufacturer = models.ForeignKey('Manufacturers', models.DO_NOTHING, blank=True, null=True)

    def is_original(self):
        return bool(self.originality_status)

    def is_used(self):
        return bool(self.used_status)

    class Meta:
        managed = False
        db_table = 'Charger_categories'


class Chargers(models.Model):
    charger_id = models.AutoField(primary_key=True)
    charger_serial = models.CharField(max_length=45, blank=True, null=True)
    f_charger_category = models.ForeignKey(ChargerCategories, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Chargers'


class Clients(models.Model):
    id_client = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'Clients'


class CompOrd(models.Model):
    id_comp_ord = models.AutoField(db_column='id_comp/ord', primary_key=True)  # Field renamed to remove unsuitable characters.
    is_ready = models.IntegerField()
    f_order_id_to_order = models.ForeignKey('Orders', models.DO_NOTHING, db_column='f_order_id_to_order')

    class Meta:
        managed = True
        db_table = 'Comp/Ord'


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
    cover = models.CharField(max_length=125, blank=True, null=True)
    display = models.CharField(max_length=125, blank=True, null=True)
    bezel = models.CharField(max_length=125, blank=True, null=True)
    keyboard = models.CharField(max_length=125, blank=True, null=True)
    mouse = models.CharField(max_length=125, blank=True, null=True)
    sound = models.CharField(max_length=125, blank=True, null=True)
    cdrom = models.CharField(max_length=125, blank=True, null=True)
    hdd_cover = models.CharField(max_length=125, blank=True, null=True)
    ram_cover = models.CharField(max_length=125, blank=True, null=True)
    other = models.CharField(max_length=300, blank=True, null=True)
    f_tester = models.ForeignKey('Testers', models.DO_NOTHING, blank=True, null=True)
    date = models.DateField() # models.DateTimeField(blank=True, null=True)
    f_bios = models.ForeignKey(Bioses, models.DO_NOTHING, blank=True, null=True)
    f_sale = models.ForeignKey('Sales', models.DO_NOTHING, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    f_id_comp_ord = models.ForeignKey(CompOrd, models.DO_NOTHING, db_column='f_id_comp/ord', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    f_id_resolution = models.ForeignKey('Resolutions', models.DO_NOTHING, db_column='f_id_resolution', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Computers'

    def getDate(self):
        if self.date is None:
            return "N/A"
        else:
            return self.date.strftime('%Y-%m-%d')

    def getOther2lines(self):
        if '\n' in self.other:
            otherList = self.other.split('\n')
            return otherList[0]+'\n' + otherList[1]
        return self.other


class Diagonals(models.Model):
    id_diagonal = models.AutoField(primary_key=True)
    diagonal_text = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'Diagonals'


class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    document = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['tar', 'txt'])])
    uploaded_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'Document'


class FormFactor(models.Model):
    form_factor_id = models.AutoField(primary_key=True)
    form_factor_name = models.CharField(db_column='Form_factor_name', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Form_factor'


class Gpus(models.Model):
    id_gpu = models.AutoField(primary_key=True)
    gpu_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'GPUs'


class HddModels(models.Model):
    hdd_models_id = models.AutoField(primary_key=True)
    hdd_models_name = models.CharField(max_length=60)

    class Meta:
        managed = True
        db_table = 'Hdd_models'


class HddOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_name = models.CharField(max_length=45)
    date_of_order = models.DateField(blank=True, null=True)
    f_order_status = models.ForeignKey('OrderStatus', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Hdd_order'


class HddSerials(models.Model):
    id_hdd = models.AutoField(primary_key=True)
    hdd_serial = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'Hdd_serials'


class HddSizes(models.Model):
    hdd_sizes_id = models.AutoField(primary_key=True)
    hdd_sizes_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'Hdd_sizes'


class Hdds(models.Model):
    hdd_id = models.AutoField(primary_key=True)
    hdd_serial = models.CharField(max_length=45, blank=True, null=True)
    health = models.IntegerField(blank=True, null=True)
    days_on = models.IntegerField(blank=True, null=True)
    tar_member_name = models.CharField(max_length=200, blank=True, null=True)
    f_lot = models.ForeignKey('Lots', models.DO_NOTHING, blank=True, null=True)
    f_hdd_models = models.ForeignKey(HddModels, models.DO_NOTHING, blank=True, null=True)
    f_hdd_sizes = models.ForeignKey(HddSizes, models.DO_NOTHING, blank=True, null=True)
    f_lock_state = models.ForeignKey('LockState', models.DO_NOTHING, blank=True, null=True)
    f_speed = models.ForeignKey('Speed', models.DO_NOTHING, blank=True, null=True)
    f_form_factor = models.ForeignKey(FormFactor, models.DO_NOTHING, blank=True, null=True)
    f_hdd_order = models.ForeignKey(HddOrder, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Hdds'


class Licenses(models.Model):
    id_license = models.AutoField(primary_key=True)
    license_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'Licenses'


class LockState(models.Model):
    lock_state_id = models.AutoField(primary_key=True)
    lock_state_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'Lock_state'


class Lots(models.Model):
    lot_id = models.AutoField(primary_key=True)
    lot_name = models.CharField(max_length=45)
    date_of_lot = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Lots'


class Manufacturers(models.Model):
    id_manufacturer = models.AutoField(primary_key=True)
    manufacturer_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'Manufacturers'


class Models(models.Model):
    id_model = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'Models'


class OrdTes(models.Model):
    id_ord_tes = models.AutoField(db_column='id_ord/tes', primary_key=True)  # Field renamed to remove unsuitable characters.
    f_order = models.ForeignKey('Orders', models.DO_NOTHING)
    f_id_tester = models.ForeignKey('Testers', models.DO_NOTHING, db_column='f_id_tester')

    class Meta:
        managed = True
        db_table = 'Ord/Tes'


class OrderStatus(models.Model):
    order_status_id = models.AutoField(primary_key=True)
    order_status_name = models.CharField(max_length=500)
    is_shown = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'Order_status'


class Orders(models.Model):
    id_order = models.AutoField(primary_key=True)
    order_name = models.CharField(max_length=45)
    is_sent = models.IntegerField()
    creation_date = models.DateField()
    f_id_client = models.ForeignKey(Clients, models.DO_NOTHING, db_column='f_id_client')

    class Meta:
        managed = True
        db_table = 'Orders'


class RamSizes(models.Model):
    id_ram_size = models.AutoField(primary_key=True)
    ram_size_text = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'RAM_sizes'


class Rams(models.Model):
    id_ram = models.AutoField(primary_key=True)
    ram_serial = models.CharField(max_length=45)
    capacity = models.CharField(max_length=10, blank=True, null=True)
    clock = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'RAMs'


class Resolutions(models.Model):
    id_resolution = models.AutoField(primary_key=True)
    resolution_text = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Resolutions'


class Sales(models.Model):
    id_sale = models.AutoField(primary_key=True)
    date_of_sale = models.DateField()
    f_id_client = models.ForeignKey(Clients, models.DO_NOTHING, db_column='f_id_client')

    class Meta:
        managed = True
        db_table = 'Sales'

    def getDate(self):
        if self.date_of_sale is None:
            return "N/A"
        else:
            return self.date_of_sale.strftime('%Y-%m-%d')


class Speed(models.Model):
    speed_id = models.AutoField(primary_key=True)
    speed_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'Speed'


class Testers(models.Model):
    id_tester = models.AutoField(primary_key=True)
    tester_name = models.CharField(max_length=45)

    class Meta:
        managed = True
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
        managed = True
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
        managed = True
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = True
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
        managed = True
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BatToComp(models.Model):
    id_bat_to_comp = models.AutoField(primary_key=True)
    f_id_computer_bat_to_com = models.ForeignKey(Computers, models.DO_NOTHING, db_column='f_id_computer_bat_to_com', blank=True, null=True)
    f_bat_bat_to_com = models.ForeignKey(Batteries, models.DO_NOTHING, db_column='f_bat_bat_to_com', blank=True, null=True)

    class Meta:
        managed = True
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
        managed = True
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'django_session'


class HddToComp(models.Model):
    id_hdd_to_comp = models.AutoField(primary_key=True)
    f_id_computer_hdd_to_com = models.ForeignKey(Computers, models.DO_NOTHING, db_column='f_id_computer_hdd_to_com', blank=True, null=True)
    f_id_hdd_hdd_to_com = models.ForeignKey(HddSerials, models.DO_NOTHING, db_column='f_id_hdd_hdd_to_com', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'hdd_to_comp'


class RamToComp(models.Model):
    id_ram_to_comp = models.AutoField(primary_key=True)
    f_id_computer_ram_to_com = models.ForeignKey(Computers, models.DO_NOTHING, db_column='f_id_computer_ram_to_com', blank=True, null=True)
    f_id_ram_ram_to_com = models.ForeignKey(Rams, models.DO_NOTHING, db_column='f_id_ram_ram_to_com', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ram_to_comp'


class GpuTypes(models.Model):
    id_gpu_type = models.AutoField(primary_key=True)
    gpu_type_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GPU_types'


class Computergpus(models.Model):
    id_computergpu = models.AutoField(primary_key=True)
    f_id_computer = models.ForeignKey('Computers', models.DO_NOTHING, db_column='f_id_computer', blank=True, null=True)
    f_id_gpu = models.ForeignKey('Gpus', models.DO_NOTHING, db_column='f_id_gpu', blank=True, null=True)
    f_id_gpu_type = models.ForeignKey('GpuTypes', models.DO_NOTHING, db_column='f_id_gpu_type', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ComputerGPUS'
