# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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


class Categories(models.Model):
    id_category = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'Categories'


class Types(models.Model):
    id_types = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'Types'


class Computers(models.Model):
    id_computer = models.AutoField(primary_key=True)
    serial = models.CharField(max_length=45)
    manufacturer = models.CharField(max_length=45, blank=True, null=True)
    model = models.CharField(max_length=45, blank=True, null=True)
    cpu = models.CharField(max_length=45, blank=True, null=True)
    ram = models.CharField(max_length=45, blank=True, null=True)
    gpu = models.CharField(max_length=45, blank=True, null=True)
    hdd = models.CharField(max_length=45, blank=True, null=True)
    diagonal = models.CharField(max_length=10, blank=True, null=True)
    license = models.CharField(max_length=3, blank=True, null=True)
    camera = models.CharField(max_length=3, blank=True, null=True)
    cover = models.CharField(max_length=45, blank=True, null=True)
    display = models.CharField(max_length=45, blank=True, null=True)
    bezel = models.CharField(max_length=45, blank=True, null=True)
    keyboard = models.CharField(max_length=45, blank=True, null=True)
    mouse = models.CharField(max_length=45, blank=True, null=True)
    sound = models.CharField(max_length=45, blank=True, null=True)
    cdrom = models.CharField(max_length=45, blank=True, null=True)
    # battery = models.CharField(max_length=45, blank=True, null=True)
    hdd_cover = models.CharField(max_length=45, blank=True, null=True)
    ram_cover = models.CharField(max_length=45, blank=True, null=True)
    other = models.CharField(max_length=300, blank=True, null=True)
    tester = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    bios = models.CharField(max_length=45, blank=True, null=True)
    computer_type = models.CharField(max_length=45, blank=True, null=True)
    motherboard_serial = models.CharField(max_length=45, blank=True, null=True)
    hdd_serial1 = models.CharField(max_length=45, blank=True, null=True)
    hdd_serial2 = models.CharField(max_length=45, blank=True, null=True)
    hdd_serial3 = models.CharField(max_length=45, blank=True, null=True)
    ram_serial1 = models.CharField(max_length=45, blank=True, null=True)
    ram_serial2 = models.CharField(max_length=45, blank=True, null=True)
    ram_serial3 = models.CharField(max_length=45, blank=True, null=True)
    ram_serial4 = models.CharField(max_length=45, blank=True, null=True)
    ram_serial5 = models.CharField(max_length=45, blank=True, null=True)
    ram_serial6 = models.CharField(max_length=45, blank=True, null=True)
    bat1_wear_out = models.CharField(max_length=45, blank=True, null=True)
    bat1_expected_time = models.CharField(max_length=45, blank=True, null=True)
    bat1_serial = models.CharField(max_length=45, blank=True, null=True)
    bat2_wear_out = models.CharField(max_length=45, blank=True, null=True)
    bat2_expected_time = models.CharField(max_length=45, blank=True, null=True)
    bat2_serial = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'website'
        db_table = 'computers'

    def getDate(self):
        return self.date.strftime('%Y-%m-%d %H:%M:%S')

    def to_string(self):
        text = "id_computer: " + str(self.id_computer) + "\r\nserial" + str(self.serial) + "\r\nmanufacturer: " + str(self.manufacturer) + "\r\nmodel: " + str(self.model) + "\r\ncpu: " + str(self.cpu) + "\r\nram: " + str(self.ram) + "\r\ngpu: " + str(self.gpu) + "\r\nhdd: " + str(self.hdd) + "\r\ndiagonal: " + str(self.diagonal) + "\r\nlicense: " + str(self.license) + "\r\ncamera: " + str(self.camera) + "\r\ncover: " + str(self.cover) + "\r\ndisplay: " + str(self.display) + "\r\nbezel: " + str(self.bezel) + "\r\nkeyboard: " + str(self.keyboard) + "\r\nmouse: " + str(self.mouse) + "\r\nsound: " + str(self.sound) + "\r\ncdrom: " + str(self.cdrom) + "\r\nbattery: " + str(self.battery) + "\r\nhdd_cover: " + str(self.hdd_cover) + "\r\nram_cover: " + str(self.ram_cover) + "\r\nother: " + str(self.other) + "\r\ntester: " + str(self.tester) + "\r\ndate: " + str(self.date) + "\r\nbios: " + str(self.bios)

        return text


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
