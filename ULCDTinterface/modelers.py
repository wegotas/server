# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bioses(models.Model):
    id_bios = models.AutoField(primary_key=True)
    bios_text = models.CharField(max_length=45)

    def __repr__(self):
        return f'id_bios: {self.id_bios}, bios_text: {self.bios_text}'

    class Meta:
        managed = True
        db_table = 'BIOSes'


class Batteries(models.Model):
    id_battery = models.AutoField(primary_key=True)
    serial = models.CharField(max_length=45)
    wear_out = models.CharField(max_length=45)
    expected_time = models.CharField(max_length=45)
    model = models.CharField(max_length=45, blank=True, null=True)
    maximum_wh = models.CharField(max_length=45, blank=True, null=True)
    factory_wh = models.CharField(max_length=45, blank=True, null=True)

    def __repr__(self):
        return f'id_battery: {self.id_battery}, serial: {self.serial}, wear_out: {self.wear_out}, expected_time: {self.expected_time}, model: {self.model}, maximum_wh: {self.maximum_wh}, factory_wh: {self.factory_wh}'

    class Meta:
        managed = True
        db_table = 'Batteries'


class CameraOptions(models.Model):
    id_camera_options = models.AutoField(db_column='id_ camera_options', primary_key=True)  # Field renamed to remove unsuitable characters.
    option_name = models.CharField(max_length=20)

    def __repr__(self):
        return f'id_camera_options: {self.id_camera_options}, option_name: {self.option_name}'

    class Meta:
        managed = True
        db_table = 'Camera_options'


class Categories(models.Model):
    id_category = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=45)
    permanent = models.IntegerField(blank=True, null=True)

    def __repr__(self):
        return f'id_category: {self.id_category}, category_name: {self.category_name}, permanent: {self.permanent}'

    class Meta:
        managed = True
        db_table = 'Categories'


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

    def __repr__(self):
        return f'charger_category_id: {self.charger_category_id}, f_manufacturer: {self.f_manufacturer}, watts: {self.watts}, originality_status: {self.originality_status}, used_status" {self.used_status}'

    def is_original(self):
        return bool(self.originality_status)

    def is_used(self):
        return bool(self.used_status)

    class Meta:
        managed = True
        db_table = 'Charger_categories'


class Chargers(models.Model):
    charger_id = models.AutoField(primary_key=True)
    charger_serial = models.CharField(max_length=45, blank=True, null=True)
    f_charger_category = models.ForeignKey(ChargerCategories, models.DO_NOTHING, blank=True, null=True)

    def __repr__(self):
        return f'charger_id: {self.charger_id}, charger_serial: {self.charger_serial}, f_charger_category: {self.f_charger_category}'

    class Meta:
        managed = True
        db_table = 'Chargers'


class Clients(models.Model):
    id_client = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=45)

    def __repr__(self):
        return f'id_client: {self.id_client}, client_name: {self.client_name}'

    class Meta:
        managed = True
        db_table = 'Clients'


class CompOrd(models.Model):
    id_comp_ord = models.AutoField(db_column='id_comp/ord', primary_key=True)  # Field renamed to remove unsuitable characters.
    is_ready = models.IntegerField()
    f_order_id_to_order = models.ForeignKey('Orders', models.DO_NOTHING, db_column='f_order_id_to_order')

    def __repr__(self):
        return f'id_comp_ord: {self.id_comp_ord}, is_ready: {self.is_ready}, f_order_id_to_order: {self.f_order_id_to_order}'

    class Meta:
        managed = True
        db_table = 'Comp/Ord'

    def get_status(self):
        if self.is_ready:
            return "Ready"
        return "In-Preperation"


class Resolutioncategories(models.Model):
    id_resolution_category = models.AutoField(primary_key=True)
    resolution_category_name = models.CharField(max_length=20)

    def __repr__(self):
        return f'id_resolution_category: {self.id_resolution_category}, resolution_category_name: {self.resolution_category_name}'

    class Meta:
        managed = True
        db_table = 'ResolutionCategories'


class Computerresolutions(models.Model):
    id_computer_resolutions = models.AutoField(primary_key=True)
    f_id_resolution = models.ForeignKey('Resolutions', models.DO_NOTHING, db_column='f_id_resolution')
    f_id_resolution_category = models.ForeignKey('Resolutioncategories', models.DO_NOTHING, db_column='f_id_resolution_category')

    def __repr__(self):
        return f'id_computer_resolutions: {self.id_computer_resolutions}, f_id_resolution: {self.f_id_resolution}, ' \
            f'f_id_resolution_category: {self.f_id_resolution_category}'

    class Meta:
        managed = True
        db_table = 'ComputerResolutions'


class ComputerFormFactors(models.Model):
    id_computer_form_factor = models.AutoField(primary_key=True)
    form_factor_name = models.CharField(max_length=45)

    def __repr__(self):
        return f'id_computer_form_factor: {self.id_computer_form_factor}, form_factor_name: {self.form_factor_name}'

    class Meta:
        managed = False
        db_table = 'Computer_form_factors'


class Receivedbatches(models.Model):
    id_received_batch = models.AutoField(primary_key=True)
    received_batch_name = models.CharField(max_length=45, blank=True, null=True)

    def __repr__(self):
        return f'id_received_batch: {self.id_received_batch}, received_batch_name: {self.received_batch_name}'

    class Meta:
        managed = False
        db_table = 'ReceivedBatches'


class Computers(models.Model):
    id_computer = models.AutoField(primary_key=True)
    computer_serial = models.CharField(max_length=45)
    motherboard_serial = models.CharField(max_length=45, blank=True, null=True)
    f_type = models.ForeignKey('Types', models.DO_NOTHING, blank=True, null=True)
    f_category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    f_manufacturer = models.ForeignKey('Manufacturers', models.DO_NOTHING, blank=True, null=True)
    f_model = models.ForeignKey('Models', models.DO_NOTHING, blank=True, null=True)
    f_ram_size = models.ForeignKey('RamSizes', models.DO_NOTHING, blank=True, null=True)
    f_diagonal = models.ForeignKey('Diagonals', models.DO_NOTHING, blank=True, null=True)
    f_license = models.ForeignKey('Licenses', models.DO_NOTHING, blank=True, null=True)
    f_camera = models.ForeignKey(CameraOptions, models.DO_NOTHING, blank=True, null=True)
    other = models.CharField(max_length=300, blank=True, null=True)
    f_tester = models.ForeignKey('Testers', models.DO_NOTHING, blank=True, null=True)
    date = models.DateField()  # models.DateTimeField(blank=True, null=True)
    f_bios = models.ForeignKey(Bioses, models.DO_NOTHING, blank=True, null=True)
    f_sale = models.ForeignKey('Sales', models.DO_NOTHING, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    f_id_comp_ord = models.ForeignKey(CompOrd, models.DO_NOTHING, db_column='f_id_comp/ord', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    f_id_matrix = models.ForeignKey('Matrixes', models.DO_NOTHING, db_column='f_id_matrix', blank=True, null=True)
    f_id_computer_resolutions = models.ForeignKey(Computerresolutions, models.DO_NOTHING,
                                                  db_column='f_id_computer_resolutions', blank=True, null=True)
    f_id_received_batches = models.ForeignKey('Receivedbatches', models.DO_NOTHING, db_column='f_id_received_batches',
                                              blank=True, null=True)
    box_number = models.IntegerField(blank=True, null=True)
    f_id_computer_form_factor = models.ForeignKey(ComputerFormFactors, models.DO_NOTHING,
                                                  db_column='f_id_computer_form_factor', blank=True, null=True)

    def __repr__(self):
        return f'id_computer: {self.id_computer}, computer_serial: {self.computer_serial}, f_type: {self.f_type}, ' \
            f'f_category: {self.f_category}, f_model: {self.f_model}, f_tester: {self.f_tester}, ' \
            f'f_id_comp_ord: {self.f_id_comp_ord}, f_id_received_batches: {self.f_id_received_batches}, ' \
            f'box_number: {self.box_number}, f_id_computer_form_factor: {self.f_id_computer_form_factor}'

    class Meta:
        managed = True
        db_table = 'Computers'

    def get_box_number(self):
        if not self.box_number:
            return ''
        return self.box_number

    def getDate(self):
        if self.date is None:
            return "N/A"
        else:
            return self.date.strftime('%Y-%m-%d')

    def getOther2lines(self):
        if '\n' in self.get_other():
            otherList = self.get_other().split('\n')
            return otherList[0]+'\n' + otherList[1]
        return self.get_other()

    def get_cpu(self):
        comp_cpus = Computerprocessors.objects.filter(f_id_computer=self)
        if comp_cpus.count() > 0:
            return ', '.join(comp_cpus.values_list("f_id_processor__model_name", flat=True))
        return ''

    def get_gpu(self):
        comp_gpus = Computergpus.objects.filter(f_id_computer=self)
        if comp_gpus.count() > 0:
            return ', '.join(comp_gpus.values_list("f_id_gpu__gpu_name", flat=True))
        return ''

    def get_other(self):
        comp_observ = Computerobservations.objects.filter(f_id_computer=self)
        return "\n".join(comp_observ.values_list("f_id_observation__full_name", flat=True)) + '\n' + self.other

    def get_status_color(self):
        if self.f_sale:
            return "red"
        elif self.f_id_comp_ord:
            return 'orange'
        return "green"

    def get_status(self):
        if self.f_sale:
            return "Sold"
        elif self.f_id_comp_ord:
            return 'Ordered'
        return "No status"


class Diagonals(models.Model):
    id_diagonal = models.AutoField(primary_key=True)
    diagonal_text = models.CharField(max_length=45)

    def __repr__(self):
        return f'id_diagonal: {self.id_diagonal}, diagonal_text: {self.diagonal_text}'

    class Meta:
        managed = True
        db_table = 'Diagonals'


class FormFactor(models.Model):
    form_factor_id = models.AutoField(primary_key=True)
    form_factor_name = models.CharField(db_column='Form_factor_name', max_length=45)  # Field name made lowercase.

    def __repr__(self):
        return f'form_factor_id: {self.form_factor_id}, form_factor_name: {self.form_factor_name}'

    class Meta:
        managed = True
        db_table = 'Form_factor'


class Gpus(models.Model):
    id_gpu = models.AutoField(primary_key=True)
    gpu_name = models.CharField(max_length=150)
    f_id_manufacturer = models.ForeignKey('Manufacturers', models.DO_NOTHING, db_column='f_id_manufacturer', blank=True,
                                          null=True)

    def __repr__(self):
        return f'id_gpu: {self.id_gpu}, gpu_name: {self.gpu_name}, f_id_manufacturer: {self.f_id_manufacturer}'

    class Meta:
        managed = True
        db_table = 'GPUs'


class HddModels(models.Model):
    hdd_models_id = models.AutoField(primary_key=True)
    hdd_models_name = models.CharField(max_length=60)

    def __repr__(self):
        return f'hdd_models_id: {self.hdd_models_id}, hdd_models_name: {self.hdd_models_name}'

    class Meta:
        managed = True
        db_table = 'Hdd_models'


class HddOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_name = models.CharField(max_length=45)
    date_of_order = models.DateField(blank=True, null=True)
    f_order_status = models.ForeignKey('OrderStatus', models.DO_NOTHING, blank=True, null=True)

    def __repr__(self):
        return f'order_id: {self.order_id}, order_name: {self.order_name}, date_of_order: {self.date_of_order}, ' \
            f'f_order_status: {self.f_order_status}'

    class Meta:
        managed = True
        db_table = 'Hdd_order'


class HddSizes(models.Model):
    hdd_sizes_id = models.AutoField(primary_key=True)
    hdd_sizes_name = models.CharField(max_length=45)

    def __repr__(self):
        return f'hdd_sizes_id: {self.hdd_sizes_id}, hdd_sizes_name: {self.hdd_sizes_name}'

    class Meta:
        managed = True
        db_table = 'Hdd_sizes'


class DriveFamily(models.Model):
    family_id = models.AutoField(primary_key=True)
    family_name = models.CharField(max_length=50, blank=True, null=True)

    def __repr__(self):
        return f'family_id: {self.family_id}, family_name: {self.family_name}'

    class Meta:
        managed = False
        db_table = 'Drive_family'


class DriveHeight(models.Model):
    height_id = models.AutoField(primary_key=True)
    height_name = models.CharField(max_length=10, blank=True, null=True)

    def __repr__(self):
        return f'height_id: {self.height_id}, height_name: {self.height_name}'

    class Meta:
        managed = False
        db_table = 'Drive_height'


class DriveLength(models.Model):
    length_id = models.AutoField(primary_key=True)
    length_name = models.CharField(max_length=10, blank=True, null=True)

    def __repr__(self):
        return f'length_id: {self.length_id}, length_name: {self.length_name}'

    class Meta:
        managed = False
        db_table = 'Drive_length'


class DriveNotes(models.Model):
    note_id = models.AutoField(primary_key=True)
    note_text = models.CharField(max_length=50, blank=True, null=True)

    def __repr__(self):
        return f'note_id: {self.note_id}, note_text: {self.note_text}'

    class Meta:
        managed = False
        db_table = 'Drive_notes'


class DrivePowerIdle(models.Model):
    power_idle_id = models.AutoField(primary_key=True)
    power_idle_name = models.CharField(max_length=10, blank=True, null=True)

    def __repr__(self):
        return f'power_idle_id: {self.power_idle_id}, power_idle_name: {self.power_idle_name}'

    class Meta:
        managed = False
        db_table = 'Drive_power_idle'


class DrivePowerSeek(models.Model):
    power_seek_id = models.AutoField(primary_key=True)
    power_seek_name = models.CharField(max_length=10, blank=True, null=True)

    def __repr__(self):
        return f'power_seek_id: {self.power_seek_id}, power_seek_name: {self.power_seek_name}'

    class Meta:
        managed = False
        db_table = 'Drive_power_seek'


class DrivePowerSpin(models.Model):
    power_spin_id = models.AutoField(primary_key=True)
    power_spin_name = models.CharField(max_length=10, blank=True, null=True)

    def __repr__(self):
        return f'power_spin_id: {self.power_spin_id}, power_spin_name: {self.power_spin_name}'

    class Meta:
        managed = False
        db_table = 'Drive_power_spin'


class DrivePowerStandby(models.Model):
    power_standby_id = models.AutoField(primary_key=True)
    power_standby_name = models.CharField(max_length=10, blank=True, null=True)

    def __repr__(self):
        return f'power_standby_id: {self.power_standby_id}, power_standby_name: {self.power_standby_name}'

    class Meta:
        managed = False
        db_table = 'Drive_power_standby'


class DriveTypes(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=10, blank=True, null=True)

    def __repr__(self):
        return f'type_id: {self.type_id}, type_name: {self.type_name}'

    class Meta:
        managed = False
        db_table = 'Drive_types'


class DriveWeight(models.Model):
    weight_id = models.AutoField(primary_key=True)
    weight_name = models.CharField(max_length=10, blank=True, null=True)

    def __repr__(self):
        return f'weight_id: {self.weight_id}, weight_name: {self.weight_name}'

    class Meta:
        managed = False
        db_table = 'Drive_weight'


class DriveWidth(models.Model):
    width_id = models.AutoField(primary_key=True)
    width_name = models.CharField(max_length=10, blank=True, null=True)

    def __repr__(self):
        return f'width_id: {self.width_id}, width_name: {self.width_name}'

    class Meta:
        managed = False
        db_table = 'Drive_width'


class Drives(models.Model):
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
    f_manufacturer = models.ForeignKey('Manufacturers', models.DO_NOTHING, db_column='f_manufacturer', blank=True,
                                       null=True)
    f_interface = models.ForeignKey('PhysicalInterfaces', models.DO_NOTHING, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    f_type = models.ForeignKey(DriveTypes, models.DO_NOTHING, blank=True, null=True)
    f_note = models.ForeignKey(DriveNotes, models.DO_NOTHING, blank=True, null=True)
    f_family = models.ForeignKey(DriveFamily, models.DO_NOTHING, blank=True, null=True)
    f_width = models.ForeignKey(DriveWidth, models.DO_NOTHING, blank=True, null=True)
    f_height = models.ForeignKey(DriveHeight, models.DO_NOTHING, blank=True, null=True)
    f_length = models.ForeignKey(DriveLength, models.DO_NOTHING, blank=True, null=True)
    f_weight = models.ForeignKey(DriveWeight, models.DO_NOTHING, blank=True, null=True)
    f_power_spin = models.ForeignKey(DrivePowerSpin, models.DO_NOTHING, blank=True, null=True)
    f_power_seek = models.ForeignKey(DrivePowerSeek, models.DO_NOTHING, blank=True, null=True)
    f_power_idle = models.ForeignKey(DrivePowerIdle, models.DO_NOTHING, blank=True, null=True)
    f_power_standby = models.ForeignKey(DrivePowerStandby, models.DO_NOTHING, blank=True, null=True)
    total_writes = models.CharField(max_length=25, blank=True, null=True)
    f_origin = models.ForeignKey('Origins', models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateField()

    def __repr__(self):
        return f'hdd_serial: {self.hdd_serial}, health: {self.health}, days_on: {self.days_on}, ' \
            f'tar_member_name: {self.tar_member_name}, f_lot: {self.f_lot}, f_hdd_models: {self.f_hdd_models}, ' \
            f'f_lock_state: {self.f_lock_state}, f_speed: {self.f_speed}, f_form_factor: {self.f_form_factor}, ' \
            f'f_hdd_order: {self.f_hdd_order}'

    class Meta:
        managed = True
        db_table = 'Drives'


class Origins(models.Model):
    origin_id = models.AutoField(primary_key=True)
    origin_name = models.CharField(max_length=100, blank=True, null=True)

    def __repr__(self):
        return f'origin_id: {self.origin_id}, origin_name: {self.origin_name}'

    class Meta:
        managed = False
        db_table = 'Origins'


class PhysicalInterfaces(models.Model):
    interface_id = models.AutoField(primary_key=True)
    interface_name = models.CharField(max_length=20, blank=True, null=True)

    def __repr__(self):
        return f'interface_id: {self.interface_id}, interface_name: {self.interface_name}'

    class Meta:
        managed = False
        db_table = 'Physical_interfaces'


class Licenses(models.Model):
    id_license = models.AutoField(primary_key=True)
    license_name = models.CharField(max_length=45)

    def __repr__(self):
        return f'id_license: {self.id_license}, license_name: {self.license_name}'

    class Meta:
        managed = True
        db_table = 'Licenses'


class LockState(models.Model):
    lock_state_id = models.AutoField(primary_key=True)
    lock_state_name = models.CharField(max_length=45)

    def __repr__(self):
        return f'lock_state_id: {self.lock_state_id}, lock_state_name: {self.lock_state_name}'

    class Meta:
        managed = True
        db_table = 'Lock_state'


class Lots(models.Model):
    lot_id = models.AutoField(primary_key=True)
    lot_name = models.CharField(max_length=45)
    date_of_lot = models.DateField(blank=True, null=True)

    def __repr__(self):
        return f'lot_id: {self.lot_id}, lot_name: {self.lot_name}, date_of_lot: {self.date_of_lot}'

    class Meta:
        managed = True
        db_table = 'Lots'


class Manufacturers(models.Model):
    id_manufacturer = models.AutoField(primary_key=True)
    manufacturer_name = models.CharField(max_length=45)

    def __repr__(self):
        return f'id_manufacturer: {self.id_manufacturer}, manufacturer_name: {self.manufacturer_name}'

    class Meta:
        managed = True
        db_table = 'Manufacturers'


class Models(models.Model):
    id_model = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=100)

    def __repr__(self):
        return f'id_model: {self.id_model}, model_name: {self.model_name}'

    class Meta:
        managed = True
        db_table = 'Models'


class OrdTes(models.Model):
    id_ord_tes = models.AutoField(db_column='id_ord/tes', primary_key=True)  # Field renamed to remove unsuitable characters.
    f_order = models.ForeignKey('Orders', models.DO_NOTHING)
    f_id_tester = models.ForeignKey('Testers', models.DO_NOTHING, db_column='f_id_tester')

    def __repr__(self):
        return f'id_ord_tes: {self.id_ord_tes}, f_order: {self.f_order}, f_id_tester: {self.f_id_tester}'

    class Meta:
        managed = True
        db_table = 'Ord/Tes'


class OrderStatus(models.Model):
    order_status_id = models.AutoField(primary_key=True)
    order_status_name = models.CharField(max_length=500)
    is_shown = models.IntegerField()

    def __repr__(self):
        return f'order_status_id: {self.order_status_id}, order_status_name: {self.order_status_name}, ' \
            f'is_shown: {self.is_shown}'

    class Meta:
        managed = True
        db_table = 'Order_status'


class Orders(models.Model):
    id_order = models.AutoField(primary_key=True)
    order_name = models.CharField(max_length=45)
    is_sent = models.IntegerField()
    creation_date = models.DateField()
    f_id_client = models.ForeignKey(Clients, models.DO_NOTHING, db_column='f_id_client')

    def __repr__(self):
        return f'id_order: {self.id_order}, order_name: {self.order_name}, is_sent: {self.is_sent}, ' \
            f'creation_date: {self.creation_date}, f_id_client: {self.f_id_client}'

    class Meta:
        managed = True
        db_table = 'Orders'


class RamSizes(models.Model):
    id_ram_size = models.AutoField(primary_key=True)
    ram_size_text = models.CharField(max_length=45)

    def __repr__(self):
        return f'id_ram_size: {self.id_ram_size}, ram_size_text: {self.ram_size_text}'

    class Meta:
        managed = True
        db_table = 'RAM_sizes'


class Rams(models.Model):
    id_ram = models.AutoField(primary_key=True)
    ram_serial = models.CharField(max_length=45)
    capacity = models.CharField(max_length=10, blank=True, null=True)
    clock = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)

    def __repr__(self):
        return f'id_ram: {self.id_ram}, ram_serial: {self.ram_serial}, capacity: {self.capacity}, ' \
            f'clock: {self.clock}, type: {self.type}'

    class Meta:
        managed = True
        db_table = 'RAMs'


class Resolutions(models.Model):
    id_resolution = models.AutoField(primary_key=True)
    resolution_text = models.CharField(max_length=45)

    def __repr__(self):
        return f'id_resolution: {self.id_resolution}, resolution_text: {self.resolution_text}'

    class Meta:
        managed = True
        db_table = 'Resolutions'


class Sales(models.Model):
    id_sale = models.AutoField(primary_key=True)
    date_of_sale = models.DateField()
    f_id_client = models.ForeignKey(Clients, models.DO_NOTHING, db_column='f_id_client')

    def __repr__(self):
        return f'id_sale: {self.id_sale}, date_of_sale: {self.date_of_sale}, f_id_client: {self.f_id_client}'

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

    def __repr__(self):
        return f'speed_id: {self.speed_id}, speed_name: {self.speed_name}'

    class Meta:
        managed = True
        db_table = 'Speed'


class Testers(models.Model):
    id_tester = models.AutoField(primary_key=True)
    tester_name = models.CharField(max_length=45)

    def __repr__(self):
        return f'id_tester: {self.id_tester}, tester_name: {self.tester_name}'

    class Meta:
        managed = True
        db_table = 'Testers'


class Types(models.Model):
    id_type = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=45)

    def __repr__(self):
        return f'id_type: {self.id_type}, type_name: {self.type_name}'

    class Meta:
        managed = True
        db_table = 'Types'

'''
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
'''

class BatToComp(models.Model):
    id_bat_to_comp = models.AutoField(primary_key=True)
    f_id_computer_bat_to_com = models.ForeignKey(Computers, models.DO_NOTHING, db_column='f_id_computer_bat_to_com', blank=True, null=True)
    f_bat_bat_to_com = models.ForeignKey(Batteries, models.DO_NOTHING, db_column='f_bat_bat_to_com', blank=True, null=True)

    def __repr__(self):
        return f'id_bat_to_comp: {self.id_bat_to_comp}, f_id_computer_bat_to_com: {self.f_id_computer_bat_to_com}, ' \
            f'f_bat_bat_to_com: {self.f_bat_bat_to_com}'

    class Meta:
        managed = True
        db_table = 'bat_to_comp'

'''
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
'''


class RamToComp(models.Model):
    id_ram_to_comp = models.AutoField(primary_key=True)
    f_id_computer_ram_to_com = models.ForeignKey(Computers, models.DO_NOTHING, db_column='f_id_computer_ram_to_com', blank=True, null=True)
    f_id_ram_ram_to_com = models.ForeignKey(Rams, models.DO_NOTHING, db_column='f_id_ram_ram_to_com', blank=True, null=True)

    def __repr__(self):
        return f'id_ram_to_comp: {self.id_ram_to_comp}, f_id_computer_ram_to_com: {self.f_id_computer_ram_to_com}, ' \
            f'f_id_ram_ram_to_com: {self.f_id_ram_ram_to_com}'

    class Meta:
        managed = True
        db_table = 'ram_to_comp'


class Processors(models.Model):
    id_processor = models.AutoField(primary_key=True)
    f_manufacturer = models.ForeignKey(Manufacturers, models.DO_NOTHING, db_column='f_manufacturer')
    model_name = models.CharField(max_length=45)
    stock_clock = models.CharField(max_length=10)
    max_clock = models.CharField(max_length=10)
    cores = models.IntegerField()
    threads = models.IntegerField()

    def __repr__(self):
        return f"id_processor: {self.id_processor}, f_manufacturer: {self.f_manufacturer}, " \
            f"model_name: {self.model_name}, stock_clock: {self.stock_clock}, max_clock: {self.max_clock}, " \
            f"cores: {self.cores}, threads: {self.threads}"

    class Meta:
        managed = True
        db_table = 'Processors'


class Computerprocessors(models.Model):
    id_computers_processors = models.AutoField(primary_key=True)
    f_id_computer = models.ForeignKey('Computers', models.DO_NOTHING, db_column='f_id_computer')
    f_id_processor = models.ForeignKey('Processors', models.DO_NOTHING, db_column='f_id_processor')

    def __repr__(self):
        return f"id_computers_processors: {self.id_computers_processors}, f_id_computer: {self.f_id_computer}, " \
            f"f_id_processor: {self.f_id_processor}"

    class Meta:
        managed = True
        db_table = 'ComputerProcessors'


class Cabletypes(models.Model):
    id_cable_types = models.AutoField(primary_key=True)
    cable_type_name = models.CharField(max_length=20)

    def __repr__(self):
        return f"id_cable_types: {self.id_cable_types}, cable_type_name: {self.cable_type_name}"

    class Meta:
        managed = True
        db_table = 'CableTypes'


class Matrixes(models.Model):
    id_matrix = models.AutoField(primary_key=True)
    f_id_cable_type = models.ForeignKey(Cabletypes, models.DO_NOTHING, db_column='f_id_cable_type')

    def __repr__(self):
        return f"id_matrix: {self.id_matrix}, f_id_cable_type: {self.f_id_cable_type}"

    class Meta:
        managed = True
        db_table = 'Matrixes'


class Computerdrives(models.Model):
    id_computer_drive = models.AutoField(primary_key=True)
    f_id_computer = models.ForeignKey('Computers', models.DO_NOTHING, db_column='f_id_computer')
    f_drive = models.ForeignKey('Drives', models.DO_NOTHING)

    def __repr__(self):
        return f"id_computer_drive: {self.id_computer_drive}, f_id_computer: {self.f_id_computer}, " \
            f"f_drive: {self.f_drive}"

    class Meta:
        managed = True
        db_table = 'ComputerDrives'


class Computergpus(models.Model):
    id_computergpus = models.AutoField(primary_key=True)
    f_id_gpu = models.ForeignKey('Gpus', models.DO_NOTHING, db_column='f_id_gpu')
    f_id_computer = models.ForeignKey('Computers', models.DO_NOTHING, db_column='f_id_computer')

    def __repr__(self):
        return f"id_computergpus: {self.id_computergpus}, f_id_gpu: {self.f_id_gpu}, " \
            f"f_id_computer: {self.f_id_computer}"

    class Meta:
        managed = True
        db_table = 'Computergpus'


class Observationcategory(models.Model):
    id_observation_category = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=45, blank=True, null=True)

    def __repr__(self):
        return f"id_observation_category: {self.id_observation_category}, category_name: {self.category_name}"

    class Meta:
        managed = True
        db_table = 'ObservationCategory'


class Observationsubcategory(models.Model):
    id_observation_subcategory = models.AutoField(primary_key=True)
    subcategory_name = models.CharField(max_length=45, blank=True, null=True)

    def __repr__(self):
        return f"id_observation_subcategory: {self.id_observation_subcategory}, " \
            f"subcategory_name: {self.subcategory_name}"

    class Meta:
        managed = True
        db_table = 'ObservationSubCategory'


class Observations(models.Model):
    id_observation = models.AutoField(primary_key=True)
    shortcode = models.CharField(unique=True, max_length=6, blank=True, null=True)
    full_name = models.CharField(max_length=45, blank=True, null=True)
    f_id_observation_category = models.ForeignKey(Observationcategory, models.DO_NOTHING, db_column='f_id_observation_category', blank=True, null=True)
    f_id_observation_subcategory = models.ForeignKey(Observationsubcategory, models.DO_NOTHING, db_column='f_id_observation_subcategory', blank=True, null=True)

    def __repr__(self):
        return f"id_observation: {self.id_observation}, shortcode: {self.shortcode}, full_name: {self.full_name}, " \
            f"f_id_observation_category: {self.f_id_observation_category}, " \
            f"f_id_observation_subcategory: {self.f_id_observation_subcategory}"

    class Meta:
        managed = True
        db_table = 'Observations'


class Computerobservations(models.Model):
    id_computer_observations = models.AutoField(primary_key=True)
    f_id_computer = models.ForeignKey('Computers', models.DO_NOTHING, db_column='f_id_computer', blank=True, null=True)
    f_id_observation = models.ForeignKey('Observations', models.DO_NOTHING, db_column='f_id_observation', blank=True, null=True)

    def __repr__(self):
        return f"id_computer_observations: {self.id_computer_observations}, f_id_computer: {self.f_id_computer}, " \
            f"f_id_observation: {self.f_id_observation}"

    class Meta:
        managed = True
        db_table = 'ComputerObservations'
