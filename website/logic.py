from ULCDTinterface.modelers import Computers, Bioses, Batteries, Cpus, CameraOptions, Categories, Computers, Clients, Sales, Diagonals, Gpus, HddSizes, Hdds, Licenses, Manufacturers, Models, RamSizes, Rams, Testers, Types, BatToComp, RamToComp, HddToComp, CompOrd, OrdTes, Orders
import xlsxwriter
import io
from django.utils import timezone
import re
from django.db.models import Q


class Bat_holder():
    def __init__(self, index=1, id=0, serial="N/A", wear="N/A", time="N/A"):
        self.index = index
        self.id = id
        self.serial = serial
        self.wear = wear
        self.time = time


def get_batteries(computer_id):
    batteries = BatToComp.objects.filter(f_id_computer_bat_to_com=computer_id)
    bat_list = []
    if batteries:
        i = 0
        for battery in batteries.iterator():
            i += 1
            if battery.f_bat_bat_to_com.serial != "N/A" and battery.f_bat_bat_to_com.wear_out != "N/A" and battery.f_bat_bat_to_com.expected_time != "N/A":
                bat = Bat_holder(
                    index=i,
                    id=battery.id_bat_to_comp,
                    serial=battery.f_bat_bat_to_com.serial,
                    wear=battery.f_bat_bat_to_com.wear_out,
                    time=battery.f_bat_bat_to_com.expected_time
                )
                bat_list.append(bat)
        if len(bat_list) == 0:
            bat = Bat_holder()
            bat_list.append(bat)
    else:
        print("Batteries asociated with this computer do not exist")
    return bat_list

class Ram_Hdd_holder():
    def __init__(self, index=1, id=0, serial="N/A"):
        self.index = index
        self.id = id
        self.serial = serial


def get_rams(computer_id):
    rams = RamToComp.objects.filter(f_id_computer_ram_to_com=computer_id)
    ram_list = []
    if rams:
        i = 0
        for ram in rams.iterator():
            i += 1
            if ram.f_id_ram_ram_to_com.ram_serial != "N/A":
                ram = Ram_Hdd_holder(
                    index=i,
                    id=ram.id_ram_to_comp,
                    serial=ram.f_id_ram_ram_to_com.ram_serial
                )
                ram_list.append(ram)
        if len(ram_list) == 0:
            first_ram = rams.first()
            ram = Ram_Hdd_holder(
                id=first_ram.id_ram_to_comp,
                serial=first_ram.f_id_ram_ram_to_com.ram_serial
            )
            ram_list.append(ram)
    else:
        print("Rams asociated with this computer do not exist")
    return ram_list

def get_hdds(computer_id):
    hdds = HddToComp.objects.filter(f_id_computer_hdd_to_com=computer_id)
    hdd_list = []
    if hdds:
        i = 0
        for hdd in hdds.iterator():
            i += 1
            if hdd.f_id_hdd_hdd_to_com.hdd_serial != "N/A":
                hdd = Ram_Hdd_holder(
                    index=i,
                    id=hdd.id_hdd_to_comp,
                    serial=hdd.f_id_hdd_hdd_to_com.hdd_serial
                )
                hdd_list.append(hdd)
        if len(hdd_list) == 0:
            first_hdd = hdds.first()
            hdd = Ram_Hdd_holder(
                id=first_hdd.id_hdd_to_comp,
                serial=first_hdd.f_id_hdd_hdd_to_com.hdd_serial
            )
            hdd_list.append(hdd)
    else:
        print("Hdds asociated with this computer do not exist")
    return hdd_list

class Edit_computer_record():

    def __init__(self, data_dict):
        self.data_dict = data_dict
        self.data_dict.pop("edit", "")
        self.data_dict.pop("edit.x", "")
        self.data_dict.pop("edit.y", "")
        # self.data_dict.pop("motherboard_serial", "")


        self._type_save(self.data_dict.pop("type_name", "")[0])
        self._category_save(self.data_dict.pop("category_name", "")[0])
        self._tester_save(self.data_dict.pop("tester_name", "")[0])
        self._bios_save(self.data_dict.pop("bios_text", "")[0])
        self._cpu_save(self.data_dict.pop("cpu_name", "")[0])
        self._camera_option_save(self.data_dict.pop("option_name", "")[0])
        self._diagonal_save(self.data_dict.pop("diagonal_text", "")[0])
        self._gpu_save(self.data_dict.pop("gpu_name", "")[0])
        self._hddsize_save(self.data_dict.pop("hdd_sizes_name", "")[0])
        self._license_save(self.data_dict.pop("license_name", "")[0])
        self._manufacturer_save(self.data_dict.pop("manufacturer_name", "")[0])
        self._model_save(self.data_dict.pop("model_name", "")[0])
        self.motherboard = self.data_dict.pop("motherboard_serial", "")[0]
        self._ramsize_save(self.data_dict.pop("ram_size_text", "")[0])
        if "client_name" in data_dict:
            self._client_save(self.data_dict.pop("client_name", "")[0])
            self._sale_save(self.data_dict.pop("date_of_sale", "")[0])
            self._computer_sold_save()
            self._process_ram_and_hdd_serials()
            self._process_batteries()
        else:
            self._computer_save()

    def _process_batteries(self):
        while len(self.data_dict) > 2:
            key = next(iter(self.data_dict))
            dbindex = self.get_dbindex(key)
            serial = self.data_dict.pop("bat_serial_" + dbindex)[0]
            wear = self.data_dict.pop("bat_wear_" + dbindex)[0]
            time = self.data_dict.pop("bat_time_" + dbindex)[0]
            battery = Batteries.objects.get_or_create(
                serial=serial,
                wear_out=wear,
                expected_time=time
            )[0]
            battery.save()

            old_battocomp = BatToComp.objects.get(id_bat_to_comp=dbindex)
            new_battocomp = BatToComp(
                id_bat_to_comp=old_battocomp.id_bat_to_comp,
                f_id_computer_bat_to_com=self.computer,
                f_bat_bat_to_com=battery
            )
            new_battocomp.save()

    def _process_ram_and_hdd_serials(self):
        processed_key_list = []
        for key, value in self.data_dict.items():
            if "bat" in key:
                continue
            elif "ram" in key:
                dbindex = self.get_dbindex(key)
                ram = Rams.objects.get_or_create(ram_serial=value)[0]
                old_ramtocomp = RamToComp.objects.get(id_ram_to_comp=dbindex)
                new_ramtocomp = RamToComp(
                    id_ram_to_comp=old_ramtocomp.id_ram_to_comp,
                    f_id_computer_ram_to_com=self.computer,
                    f_id_ram_ram_to_com=ram
                )
                new_ramtocomp.save()
                processed_key_list.append(key)
            elif "hdd" in key:
                dbindex = self.get_dbindex(key)
                hdd = Hdds.objects.get_or_create(hdd_serial=value)[0]
                old_hddtocomp = HddToComp.objects.get(id_hdd_to_comp=dbindex)
                new_hddtocomp = HddToComp(
                    id_hdd_to_comp=old_hddtocomp.id_hdd_to_comp,
                    f_id_computer_hdd_to_com=self.computer,
                    f_id_hdd_hdd_to_com=hdd
                )
                new_hddtocomp.save()
                processed_key_list.append(key)
        for key in processed_key_list:
            self.data_dict.pop(key)

    def get_dbindex(self, key):
        return key.split("_")[2]

    def _computer_save(self):
        self.computer = Computers(
            id_computer=self.data_dict.pop("id_computer", "")[0],
            computer_serial=self.data_dict.pop("serial", "")[0],
            f_type=self.type,
            f_category=self.category,
            f_manufacturer=self.manufacturer,
            f_model=self.model,
            f_cpu=self.cpu,
            f_gpu=self.gpu,
            f_ram_size=self.ramsize,
            f_hdd_size=self.hddsize,
            f_diagonal=self.diagonal,
            f_license=self.license,
            f_camera=self.camera_option,
            cover=self.data_dict.pop("cover", "")[0],
            display=self.data_dict.pop("display", "")[0],
            bezel=self.data_dict.pop("bezel", "")[0],
            keyboard=self.data_dict.pop("keyboard", "")[0],
            mouse=self.data_dict.pop("mouse", "")[0],
            sound=self.data_dict.pop("sound", "")[0],
            cdrom=self.data_dict.pop("cdrom", "")[0],
            hdd_cover=self.data_dict.pop("hdd_cover", "")[0],
            ram_cover=self.data_dict.pop("ram_cover", "")[0],
            other=self.data_dict.pop("other", "")[0],
            f_tester=self.tester,
            date=self.data_dict.pop("date", "")[0],
            f_bios=self.bios,
            motherboard_serial=self.motherboard
        )
        self.computer.save()

    def _computer_sold_save(self):
        self.computer = Computers(
            id_computer=self.data_dict.pop("id_computer", "")[0],
            computer_serial=self.data_dict.pop("serial", "")[0],
            f_type=self.type,
            f_category=self.category,
            f_manufacturer=self.manufacturer,
            f_model=self.model,
            f_cpu=self.cpu,
            f_gpu=self.gpu,
            f_ram_size=self.ramsize,
            f_hdd_size=self.hddsize,
            f_diagonal=self.diagonal,
            f_license=self.license,
            f_camera=self.camera_option,
            cover=self.data_dict.pop("cover", "")[0],
            display=self.data_dict.pop("display", "")[0],
            bezel=self.data_dict.pop("bezel", "")[0],
            keyboard=self.data_dict.pop("keyboard", "")[0],
            mouse=self.data_dict.pop("mouse", "")[0],
            sound=self.data_dict.pop("sound", "")[0],
            cdrom=self.data_dict.pop("cdrom", "")[0],
            hdd_cover=self.data_dict.pop("hdd_cover", "")[0],
            ram_cover=self.data_dict.pop("ram_cover", "")[0],
            other=self.data_dict.pop("other", "")[0],
            f_tester=self.tester,
            date=self.data_dict.pop("date", "")[0],
            f_bios=self.bios,
            f_sale=self.sale,
            price=self.data_dict.pop("price", "")[0],
            motherboard_serial=self.motherboard
        )
        self.computer.save()

    def _client_save(self, client_name):
        self.client = Clients.objects.get_or_create(client_name=client_name)[0]
        # self.client.save()

    def _sale_save(self, date_of_sale):
        self.sale = Sales.objects.get_or_create(
            date_of_sale=date_of_sale,
            f_id_client=self.client
        )[0]

    def _type_save(self, value):
        self.type = Types.objects.get_or_create(type_name=value)[0]

    def _tester_save(self, value):
        self.tester = Testers.objects.get_or_create(tester_name=value)[0]

    def _category_save(self, value):
        self.category = Categories.objects.get_or_create(category_name=value)[0]

    def _bios_save(self, value):
        self.bios = Bioses.objects.get_or_create(bios_text=value)[0]

    def _cpu_save(self, value):
        self.cpu = Cpus.objects.get_or_create(cpu_name=value)[0]

    def _camera_option_save(self, value):
        self.camera_option = CameraOptions.objects.get_or_create(option_name=value)[0]

    def _diagonal_save(self, value):
        self.diagonal = Diagonals.objects.get_or_create(diagonal_text=value)[0]

    def _gpu_save(self, value):
        self.gpu = Gpus.objects.get_or_create(gpu_name=value)[0]

    def _hddsize_save(self, value):
        self.hddsize = HddSizes.objects.get_or_create(hdd_sizes_name=value)[0]

    def _license_save(self, value):
        self.license = Licenses.objects.get_or_create(license_name=value)[0]

    def _manufacturer_save(self, value):
        self.manufacturer = Manufacturers.objects.get_or_create(manufacturer_name=value)[0]

    def _model_save(self, value):
        self.model = Models.objects.get_or_create(model_name=value)[0]

    def _ramsize_save(self, value):
        self.ramsize = RamSizes.objects.get_or_create(ram_size_text=value)[0]


def edit_post(data_dict):
    data_dict.pop("edit", "")
    id_computer = data_dict.pop("id_computer", "")[0]
    serial = data_dict.pop("serial", "")[0]
    type_name = data_dict.pop("type_name", "")[0]
    category_name = data_dict.pop("category_name", "")[0]
    manufacturer = data_dict.pop("manufacturer_name", "")[0]
    model = data_dict.pop("model_name", "")[0]
    cpu = data_dict.pop("cpu_name", "")[0]
    gpu = data_dict.pop("gpu_name", "")[0]
    ram_size = data_dict.pop("ram_size_text", "")[0]
    hdd_size = data_dict.pop("hdd_sizes_name", "")[0]
    diagonal = data_dict.pop("diagonal_text", "")[0]
    license_name = data_dict.pop("license_name", "")[0]
    option_name = data_dict.pop("option_name", "")[0]
    cover = data_dict.pop("cover", "")[0]
    display = data_dict.pop("display", "")[0]
    bezel = data_dict.pop("bezel", "")[0]
    keyboard = data_dict.pop("keyboard", "")[0]
    mouse = data_dict.pop("mouse", "")[0]
    sound = data_dict.pop("sound", "")[0]
    cdrom = data_dict.pop("cdrom", "")[0]
    hdd_cover = data_dict.pop("hdd_cover", "")[0]
    ram_cover = data_dict.pop("ram_cover", "")[0]
    other = data_dict.pop("other", "")[0]
    tester_name = data_dict.pop("tester_name", "")[0]
    date = data_dict.pop("date", "")[0]
    bios_text = data_dict.pop("bios_text", "")[0]
    motherboard = data_dict.pop("motherboard_serial", "")[0]
    bat_list = []
    ram_list = []
    hdd_list = []
    for key, value in data_dict.items():
        if "bat" in key:
            continue
        elif "ram" in key:
            classname, attribute, dbindex = get_key_tupple(key)
            ram = Ram_Hdd_holder(
                id=dbindex,
                serial=value
            )
            ram_list.append(ram)
        elif "hdd" in key:
            classname, attribute, dbindex = get_key_tupple(key)
            hdd = Ram_Hdd_holder(
                id=dbindex,
                serial=value
            )
            hdd_list.append(hdd)
    for ram in ram_list:
        data_dict.pop("ram_serial_" + ram.id)
    for hdd in hdd_list:
        data_dict.pop("hdd_serial_" + hdd.id)
    while len(data_dict) > 2:
        key = next(iter(data_dict))
        classname, attribute, dbindex = get_key_tupple(key)
        serial = data_dict.pop("bat_serial_" + dbindex)[0]
        wear = data_dict.pop("bat_wear_" + dbindex)[0]
        time = data_dict.pop("bat_time_" + dbindex)[0]
        battery = Bat_holder(
            id=dbindex,
            serial=serial,
            wear=wear,
            time=time
        )
        bat_list.append(battery)

def get_key_tupple(key):
    return tuple(key.split("_"))

class Counter:
    count = 0

    def increment(self):
        self.count += 1
        return ''

class QtySelect:
    qty = 0
    state10 = ""
    state20 = ""
    state50 = ""
    state100 = ""
    state200 = ""

    def setDefaultSelect(self, qty):
        self.qty=qty
        if qty==10:
            self.state10 = "selected"
        elif qty==20:
            self.state20 = "selected"
        elif qty==50:
            self.state50 = "selected"
        elif qty==100:
            self.state100 = "selected"
        elif qty==200:
            self.state200 = "selected"
        elif qty==1000:
            self.state1000 = "selected"


class AutoFilters:

    def __init__(self):
        self.getSerials()
        self.getManufacturers()
        self.getModels()
        self.getCpus()
        self.getRams()
        self.getGpus()
        self.getScreens()
        self.getOther()

    def getSerials(self):
        serials = Computers.objects.values('computer_serial').distinct()
        self.serials = [a['computer_serial'] for a in serials]

    def getManufacturers(self):
        manufacturers = Manufacturers.objects.values('manufacturer_name').distinct()
        self.manufacturers = [a['manufacturer_name'] for a in manufacturers]

    def getModels(self):
        models = Models.objects.values('model_name').distinct()
        self.models = [a['model_name'] for a in models]

    def getCpus(self):
        cpus = Cpus.objects.values('cpu_name').distinct()
        self.cpus = [a['cpu_name'] for a in cpus]

    def getRams(self):
        rams = RamSizes.objects.values('ram_size_text').distinct()
        self.rams = [a['ram_size_text'] for a in rams]

    def getGpus(self):
        gpus = Gpus.objects.values('gpu_name').distinct()
        self.gpus = [a['gpu_name'] for a in gpus]

    def getScreens(self):
        screens = Diagonals.objects.values('diagonal_text').distinct()
        self.screens = [a['diagonal_text'] for a in screens]

    def getOther(self):
        others = Computers.objects.values('other').distinct()
        self.others = [a['other'] for a in others]


class AutoFiltersFromComputers:

    def __init__(self, computers):
        self.computers = computers
        self._get_serials()
        self._get_manufacturers()
        self._getModels()
        self._getCpus()
        self._getRams()
        self._getGpus()
        self._getScreens()
        self._getOther()

    def _get_serials(self):
        serials = self.computers.values('computer_serial').distinct()
        self.serials = [a['computer_serial'] for a in serials]
        self.serials.sort()

    def _get_manufacturers(self):
        manufacturers = self.computers.values('f_manufacturer').distinct()
        manufacturers_id = [a['f_manufacturer'] for a in manufacturers]
        self.manufacturers = []
        for id in manufacturers_id:
            man = Manufacturers.objects.get(id_manufacturer=id)
            self.manufacturers.append(man.manufacturer_name)
        self.manufacturers.sort()

    def _getModels(self):
        models = self.computers.values('f_model').distinct()
        models_id = [a['f_model'] for a in models]
        self.models = []
        for id in models_id:
            mod = Models.objects.get(id_model=id)
            self.models.append(mod.model_name)
        self.models.sort()

    def _getCpus(self):
        cpus = self.computers.values('f_cpu').distinct()
        cpus_id = [a['f_cpu'] for a in cpus]
        self.cpus = []
        for id in cpus_id:
            if id is None:
                self.cpus.append("")
            else:
                cpu = Cpus.objects.get(id_cpu=id)
                self.cpus.append(cpu.cpu_name)
        self.cpus.sort()

    def _getRams(self):
        rams = self.computers.values('f_ram_size').distinct()
        rams_id = [a['f_ram_size'] for a in rams]
        self.rams = []
        for id in rams_id:
            if id is None:
                self.rams.append("")
            else:
                ram = RamSizes.objects.get(id_ram_size=id)
                self.rams.append(ram.ram_size_text)
        self.rams.sort()

    def _getGpus(self):
        gpus = self.computers.values('f_gpu').distinct()
        gpus_id = [a['f_gpu'] for a in gpus]
        self.gpus = []
        for id in gpus_id:
            if id is None:
                self.gpus.append("")
            else:
                gpu = Gpus.objects.get(id_gpu=id)
                self.gpus.append(gpu.gpu_name)
        self.gpus.sort()

    def _getScreens(self):
        screens = self.computers.values("f_diagonal").distinct()
        screens_id = [a['f_diagonal'] for a in screens]
        self.screens = []
        for id in screens_id:
            if id is None:
                self.screens.append("")
            else:
                screen = Diagonals.objects.get(id_diagonal=id)
                self.screens.append(screen.diagonal_text)
        self.screens.sort()

    def _getOther(self):
        others = self.computers.values("other").distinct()
        self.others = [a['other'] for a in others]
        self.others.sort()


class AutoFiltersFromSoldComputers(AutoFiltersFromComputers):

    def __init__(self, computers):
        self.computers = computers
        self._getPrice()
        self._getDateOfSale()
        self._getClients()
        super(AutoFiltersFromSoldComputers, self).__init__(computers)

    def _getPrice(self):
        """
        def toStr(objct):
            if objct is None:
                return ''
            else:
                return str(objct)

        prices = self.computers.values("price").distinct()
        self.prices = [toStr(a['price']) for a in prices]
        """
        prices = self.computers.values("price").distinct()
        self.prices = [str(a['price']) for a in prices]
        self.prices.sort()

    def _getDateOfSale(self):
        sales = self.computers.values("f_sale").distinct()
        sales_id = [a['f_sale'] for a in sales]
        self.dates = []
        for id in sales_id:
            if id is None:
                self.dates.append("")
            else:
                sale = Sales.objects.get(id_sale=id)
                self.dates.append(sale.getDate())
        self.dates = list(set(self.dates))
        self.dates.sort()

    def _getClients(self):
        sales = self.computers.values("f_sale").distinct()
        sales_id = [a['f_sale'] for a in sales]
        self.clients = []
        for id in sales_id:
            if id is None:
                self.dates.append("")
            else:
                sale = Sales.objects.get(id_sale=id)
                self.clients.append(sale.f_id_client.client_name)
        self.clients = list(set(self.clients))
        self.clients.sort()


class CatTyp:

    def __init__(self):
        self.innerList = []
        query = """select distinct tp.id_type, tp.type_name, cat.category_name from sopena_computers.Types as tp
join sopena_computers.Computers as comp on comp.f_type_id = tp.id_type
join sopena_computers.Categories as cat on cat.id_category = comp.f_category_id
where comp.f_sale_id is NULL and comp.`f_id_comp/ord` is Null"""
        for output in Types.objects.raw(query):
            inserted = False
            for member in self.innerList:
                if member.type == output.type_name:
                    member.add_category(output.category_name)
                    inserted = True
            if not inserted:
                cattypholder = CatTypHolder(output.type_name, output.category_name)
                self.innerList.append(cattypholder)


class CatTypHolder:

    def __init__(self, type_name, category_name):
        self.innerList = []
        self.type = type_name
        self.innerList.append(category_name)

    def add_category(self, category_name):
        self.innerList.append(category_name)


def getIsSold(request):
    if request.GET.get('sold') is None:
        return False
    else:
        if request.GET.get('sold') == "True":
            return True
        else:
            return False


def getIsOrder(request):
    if request.GET.get('orders') is None:
        return False
    else:
        if request.GET.get('orders') == "True":
            return True
        else:
            return False


def getQty(data_dict):
    if data_dict.get('qty') is None:
        return 10
    else:
        return int(data_dict.pop('qty')[0])


def getPage(data_dict):
    if data_dict.get('page') is None:
        return 1
    else:
        return int(data_dict.pop('page')[0])


def getType(data_dict):
    if data_dict.get('type') is None:
        return None
    else:
        return data_dict.pop('type')[0]


def getCat(data_dict):
    if data_dict.get('cat') is None:
        return None
    else:
        return data_dict.pop('cat')[0]


def getKeyword(data_dict):
    if data_dict.get('keyword') is None or data_dict.get('keyword') == "":
        return None
    else:
        return data_dict.pop('keyword')[0]


def removeSold(data_dict):
    if "sold" in data_dict:
        data_dict.pop("sold")


def recordDeleteByIndex(int_index):
    bats_to_comp = BatToComp.objects.filter(f_id_computer_bat_to_com=int_index)
    for bat_to_comp in bats_to_comp:
        bat_to_comp.delete()
    hdds_to_comp = HddToComp.objects.filter(f_id_computer_hdd_to_com=int_index)
    for hdd_to_comp in hdds_to_comp:
        hdd_to_comp.delete()
    rams_to_comp = RamToComp.objects.filter(f_id_computer_ram_to_com=int_index)
    for ram_to_comp in rams_to_comp:
        ram_to_comp.delete()
    existing_computer = Computers.objects.get(id_computer=int_index)

    cpu = existing_computer.f_cpu
    diagonal = existing_computer.f_diagonal
    hdd_size = existing_computer.f_hdd_size
    ram_size = existing_computer.f_ram_size
    gpu = existing_computer.f_gpu
    model = existing_computer.f_model
    manufacturer = existing_computer.f_manufacturer

    existing_computer.delete()
    cpu_deletion_if_exists(cpu)
    diagonal_deletion_if_exists(diagonal)
    hdd_size_deletion_if_exists(hdd_size)
    ram_size_deletion_if_exists(ram_size)
    gpu_deletion_if_exists(gpu)
    model_deletion_if_exists(model)
    manufacturer_deletion_if_exists(manufacturer)


def motherboard_deletion_if_exists(motherboard):
    if motherboard is not None:
        motherboard.delete()


def cpu_deletion_if_exists(cpu):
    if cpu is not None:
        if not Computers.objects.filter(f_cpu=cpu.id_cpu).exists():
            cpu.delete()


def diagonal_deletion_if_exists(diagonal):
    if diagonal is not None:
        if not Computers.objects.filter(f_diagonal=diagonal.id_diagonal).exists():
            diagonal.delete()


def hdd_size_deletion_if_exists(hdd_size):
    if hdd_size is not None:
        if not Computers.objects.filter(f_hdd_size=hdd_size.id_hdd_sizes).exists():
            hdd_size.delete()


def ram_size_deletion_if_exists(ram_size):
    if ram_size is not None:
        if not Computers.objects.filter(f_ram_size=ram_size.id_ram_size).exists():
            ram_size.delete()


def gpu_deletion_if_exists(gpu):
    if gpu is not None:
        if not Computers.objects.filter(f_gpu=gpu.id_gpu).exists():
            gpu.delete()


def model_deletion_if_exists(model):
    if model is not None:
        if not Computers.objects.filter(f_model=model.id_model).exists():
            model.delete()


def manufacturer_deletion_if_exists(manufacturer):
    if manufacturer is not None:
        if not Computers.objects.filter(f_manufacturer=manufacturer.id_manufacturer).exists():
            manufacturer.delete()


def changeCategoriesUsingDict(dict):
    category_name = next(iter(dict))
    indexes = dict[category_name]
    category = Categories.objects.get(category_name=category_name)
    for ind in indexes:
        computer = Computers.objects.get(id_computer=ind)
        computer.f_category = category
        computer.save()


def createExcelFile(indexes):
    unwantedCommentsParts = ('ok', '\t', '-', '0k', 'Ok,' 'ok;', 'Ok;', 'oik', 'oko', 'ok,', '\n', '+', 'ook', '\nok', '0k', 'n;', 'n,', 'n ', 'other', )
    unwantedComments = ('o', 'n', 'k', 'NULL', 'None', 'ko')

    memfile = io.BytesIO()
    workbook = xlsxwriter.Workbook(memfile)
    worksheet = workbook.add_worksheet()
    bold_bordered = workbook.add_format({"bold": True, "border": 1})
    bordered = workbook.add_format({"border": 1})

    worksheet.write("A1", "S/N", bold_bordered)
    worksheet.write("B1", "Manufacturer", bold_bordered)
    worksheet.write("C1", "Model", bold_bordered)
    worksheet.write("D1", "CPU", bold_bordered)
    worksheet.write("E1", "RAM", bold_bordered)
    worksheet.write("F1", "GPU", bold_bordered)
    worksheet.write("G1", "HDD", bold_bordered)
    worksheet.write("H1", "Batteries", bold_bordered)
    worksheet.write("I1", "LCD", bold_bordered)
    worksheet.write("J1", "Optical", bold_bordered)
    worksheet.write("K1", "COA", bold_bordered)
    worksheet.write("L1", "Cam", bold_bordered)
    worksheet.write("M1", "Comment", bold_bordered)
    worksheet.write("N1", "Price", bold_bordered)
    row = 1
    col = 0
    for int_index in indexes:
        computer = Computers.objects.get(id_computer=int_index)
        worksheet.write(row, col, _get_serial(computer), bordered)
        worksheet.write(row, col + 1, _get_manufacturer(computer), bordered)
        worksheet.write(row, col + 2, _get_model(computer), bordered)
        worksheet.write(row, col + 3, _get_cpu_name(computer), bordered)
        worksheet.write(row, col + 4, _get_ram_size(computer), bordered)
        worksheet.write(row, col + 5, _get_gpu_name(computer), bordered)
        worksheet.write(row, col + 6, _get_hdd_size(computer), bordered)
        worksheet.write(row, col + 7, _get_battery_time(int_index), bordered)
        worksheet.write(row, col + 8, _get_diagonal(computer), bordered)
        worksheet.write(row, col + 9, _get_cdrom(computer), bordered)
        worksheet.write(row, col + 10, _get_license(computer), bordered)
        worksheet.write(row, col + 11, _get_camera_option(computer), bordered)
        worksheet.write(row, col + 12, str(computer.other), bordered)
        row += 1
    workbook.close()
    return memfile


def _get_serial(computer):
    serial = ""
    try:
        serial = computer.computer_serial
    except:
        serial = "N/A"
    return serial


def _get_manufacturer(computer):
    manufacturer = ""
    try:
        manufacturer = computer.f_manufacturer.manufacturer_name
    except:
        manufacturer = "N/A"
    return manufacturer


def _get_model(computer):
    model = ""
    try:
        model = computer.f_model.model_name
    except:
        model = "N/A"
    return model


def _get_cpu_name(computer):
    cpu_name = ""
    try:
        cpu_name = computer.f_cpu.cpu_name
    except:
        cpu_name = "N/A"
    return cpu_name


def _get_ram_size(computer):
    ram_size = ""
    try:
        ram_size = computer.f_ram_size.ram_size_text
    except:
        ram_size = "N/A"
    return ram_size


def _get_gpu_name(computer):
    gpu_name = ""
    try:
        gpu_name = computer.f_gpu.gpu_name
    except:
        gpu_name = "N/A"
    return gpu_name


def _get_hdd_size(computer):
    hdd_size = ""
    try:
        hdd_size = computer.f_hdd_size.hdd_sizes_name
    except:
        hdd_size = "N/A"
    return hdd_size


def _get_battery_time(int_index):
    bat_to_comps = BatToComp.objects.filter(f_id_computer_bat_to_com=int_index)
    for con in bat_to_comps:
        print(con.f_bat_bat_to_com.expected_time)
    if len(bat_to_comps) > 2:
        return "~1h."
    elif len(bat_to_comps) < 1:
        return "No"
    else:
        return str(bat_to_comps[0].f_bat_bat_to_com.expected_time)


def _get_diagonal(computer):
    diagonal = ""
    try:
        diagonal = computer.f_diagonal.diagonal_text
    except:
        diagonal = "N/A"
    return diagonal


def _get_cdrom(computer):
    cdrom = ""
    try:
        cdrom = computer.cdrom
    except:
        cdrom = "N/A"
    return cdrom


def _get_license(computer):
    license_name = ""
    try:
        license_name = computer.f_license.license_name
    except:
        license_name = "N/A"
    return license_name


def _get_camera_option(computer):
    camera_option = ""
    try:
        camera_option = computer.f_camera.option_name
    except:
        camera_option = "N/A"
    return camera_option

class item:

    def __init__(self, item_id, item_name, permanence=0):
        self.id = item_id
        self.name = item_name
        self.permanence = bool(permanence)

def get_categories_list():
    cats = Categories.objects.all()
    catlist = []
    for cat in cats:
        newItem = item(cat.id_category, cat.category_name, cat.permanent)
        catlist.append(newItem)
    return catlist


def save_category(name):
    if name != "":
        Categories.objects.get_or_create(category_name=name)


def edit_category(data):
    cat = Categories.objects.get(id_category=data["ItemId"])
    if cat.permanent != 1:
        cat.category_name = data["ItemName"]
        cat.save()


def deleteCategory(index):
    cat = Categories.objects.get(id_category=index)
    if cat.permanent != 1:
        cat.delete()


def get_types_list():
    types = Types.objects.all()
    typeslist = []
    for typie in types:
        newItem = item(typie.id_type, typie.type_name)
        typeslist.append(newItem)
    return typeslist


def save_type(name):
    if name != "":
        Types.objects.get_or_create(type_name=name)


def edit_type(data):
    typ = Types.objects.get(id_type=data["ItemId"])
    typ.type_name = data["ItemName"]
    typ.save()


def deleteType(index):
    typ = Types.objects.get(id_type=index)
    typ.delete()


def get_testers_list():
    testers = Testers.objects.all()
    testerslist = []
    for tester in testers:
        newItem = item(tester.id_tester, tester.tester_name)
        testerslist.append(newItem)
    return testerslist


def save_tester(name):
    if name != "":
        Testers.objects.get_or_create(tester_name=name)


def edit_tester(data):
    tes = Testers.objects.get(id_tester=data["ItemId"])
    tes.tester_name = data["ItemName"]
    tes.save()


def deleteTester(index):
    tes = Testers.objects.get(id_tester=index)
    tes.delete()


class record_to_add():

    def __init__(self, data_dict):
        self.data = data_dict
        print(self.data)
        self.error_list = []

    def get_error_message(self):
        return "\r\n".join(self.error_list)

    def save(self):
        print("rta save start")
        self._validate()
        if len(self.error_list) == 0:
            self._save_and_get_type()
            self._save_and_get_category()
            self._save_and_get_manufacturer()
            self._save_and_get_model()
            self._save_and_get_cpu()
            self._save_and_get_gpu()
            self._save_and_get_ramsize()
            self._save_and_get_hdd_size()
            self._save_and_get_diagonal()
            self._save_and_get_license()
            self._save_and_get_tester()
            self.timenow = timezone.now()
            self._save_computer()
            print("rta save end")
        else:
            print("rta save FAILED")

    def isSaved(self):
        if len(self.error_list) == 0:
            return True
        else:
            return False

    def _validate(self):
        fieldnames = (
            "serial",
            "type_name",
            "category_name",
            "manufacturer_name",
            "model_name",
            "diagonal_text",
            "license_name",
            "cover",
            "bezel",
            "hdd_cover",
            "ram_cover",
            "other",
            "tester_name"
        )

        error_messages = (
            "Serial was not set",
            "Type was not set",
            "Category was not set",
            "Manufacturer was not set",
            "Model was not set",
            "Diagonal was not set",
            "License was not set",
            "Cover was not set",
            "Bezel was not set",
            "HDD cover was not set",
            "RAM cover was not set",
            "Other was not set",
            "Tester was not set"
        )

        for i in range(len(fieldnames)):
            if self.data.get(fieldnames[i]) == "" or self.data.get(fieldnames[i]) is None:
                self.error_list.append(error_messages[i])


    def _save_and_get_type(self):
        self.typ = Types.objects.get_or_create(type_name=self.data.get("type_name"))[0]

    def _save_and_get_category(self):
        self.cat = Categories.objects.get_or_create(category_name=self.data.get("category_name"))[0]

    def _save_and_get_manufacturer(self):
        self.man = Manufacturers.objects.get_or_create(manufacturer_name=self.data.get("manufacturer_name"))[0]

    def _save_and_get_model(self):
        self.model = Models.objects.get_or_create(model_name=self.data.get("model_name"))[0]

    def _save_and_get_cpu(self):
        self.cpu = Cpus.objects.get_or_create(cpu_name=self.data.get("cpu_name"))[0]

    def _save_and_get_gpu(self):
        self.gpu = Gpus.objects.get_or_create(gpu_name=self.data.get("gpu_name"))[0]

    def _save_and_get_ramsize(self):
        self.ramsize = RamSizes.objects.get_or_create(ram_size_text=self.data.get("ram_size_text"))[0]

    def _save_and_get_hdd_size(self):
        self.hddsize = HddSizes.objects.get_or_create(hdd_sizes_name=self.data.get("hdd_sizes_name"))[0]

    def _save_and_get_diagonal(self):
        self.diagonal = Diagonals.objects.get_or_create(diagonal_text=self.data.get("diagonal_text"))[0]

    def _save_and_get_license(self):
        self.lic = Licenses.objects.get_or_create(license_name=self.data.get("license_name"))[0]

    def _save_and_get_tester(self):
        self.tester = Testers.objects.get_or_create(tester_name=self.data.get("tester_name"))[0]

    def _save_computer(self):
        computer = Computers(
            computer_serial=self.data.get("serial"),
            f_type=self.typ,
            f_category=self.cat,
            f_manufacturer=self.man,
            f_model=self.model,
            f_cpu=self.cpu,
            f_gpu=self.gpu,
            f_ram_size=self.ramsize,
            f_hdd_size=self.hddsize,
            f_diagonal=self.diagonal,
            f_license=self.lic,
            cover=self.data.get("cover"),
            display=self.data.get("display"),
            bezel=self.data.get("bezel"),
            hdd_cover=self.data.get("hdd_cover"),
            ram_cover=self.data.get("ram_cover"),
            other=self.data.get("other"),
            f_tester=self.tester,
            date=self.timenow
        )
        computer.save()


class RecordChoices:

    def __init__(self):
        self._set_types()
        self._set_categories()
        self._set_manufacturers()
        self._set_models()
        self._set_cpu()
        self._set_gpu()
        self._set_rams()
        self._set_hdds()
        self._set_diagonals()
        self._set_licenses()
        self._set_cameras()
        self._set_tester()

    def _set_types(self):
        self.types = [record[0] for record in Types.objects.values_list("type_name")]

    def _set_categories(self):
        self.categories = [record[0] for record in Categories.objects.values_list("category_name")]

    def _set_manufacturers(self):
        self.manufacturers = [record[0] for record in Manufacturers.objects.values_list("manufacturer_name")]

    def _set_models(self):
        self.models = [record[0] for record in Models.objects.values_list("model_name")]

    def _set_cpu(self):
        self.cpus = [record[0] for record in Cpus.objects.values_list("cpu_name")]

    def _set_gpu(self):
        self.gpus = [record[0] for record in Gpus.objects.values_list("gpu_name")]

    def _set_rams(self):
        self.rams = [record[0] for record in RamSizes.objects.values_list("ram_size_text")]

    def _set_hdds(self):
        self.hdds = [record[0] for record in HddSizes.objects.values_list("hdd_sizes_name")]

    def _set_diagonals(self):
        self.diagonals = [record[0] for record in Diagonals.objects.values_list("diagonal_text")]

    def _set_licenses(self):
        self.licenses = [record[0] for record in Licenses.objects.values_list("license_name")]

    def _set_cameras(self):
        self.cameras = [record[0] for record in CameraOptions.objects.values_list("option_name")]

    def _set_tester(self):
        self.testers = [record[0] for record in Testers.objects.values_list("tester_name")]


class AutoFilter():

    keys = ('man-af', 'sr-af', 'scr-af', 'ram-af', 'gpu-af', 'mod-af', 'cpu-af', 'oth-af', 'cli-af', 'dos-af', 'pri-af')

    def __init__(self, data_dict):
        self.filter_dict = {}
        for key in self.keys:
            if key in data_dict:
                self.filter_dict[key] = data_dict.pop(key)

    def filter(self, computers):
        for key, value in self.filter_dict.items():
            if key == 'man-af':
                computers = computers.filter(f_manufacturer__manufacturer_name__in=value)
            elif key == 'sr-af':
                computers = computers.filter(computer_serial__in=value)
            elif key == 'scr-af':
                computers = computers.filter(f_diagonal__diagonal_text__in=value)
            elif key == 'ram-af':
                computers = computers.filter(f_ram_size__ram_size_text__in=value)
            elif key == 'gpu-af':
                computers = computers.filter(f_gpu__gpu_name__in=value)
            elif key == 'mod-af':
                computers = computers.filter(f_model__model_name__in=value)
            elif key == 'cpu-af':
                computers = computers.filter(f_cpu__cpu_name__in=value)
            elif key == 'oth-af':
                computers = computers.filter(other__in=value)
            elif key == 'cli-af':
                computers = computers.filter(f_sale__f_id_client__client_name__in=value)
            elif key == 'dos-af':
                computers = computers.filter(f_sale__date_of_sale__in=value)
            elif key == 'pri-af':
                '''
                for idx in range(len(value)):
                    if value[idx] == '':
                        value[idx] = None
                '''
                computers = computers.filter(price__in=value)
        return computers


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace('', (str(t[0]) or str(t[1])).strip()) for t in findterms(query_string)]


def get_query(query_string):
    searchfields = (
        'computer_serial',
        'other',
        'f_manufacturer__manufacturer_name',
        'f_diagonal__diagonal_text',
        'f_ram_size__ram_size_text',
        'f_gpu__gpu_name',
        'f_model__model_name',
        'f_cpu__cpu_name',
        'f_sale__f_id_client__client_name',
        'f_sale__date_of_sale',
        'price'
    )
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in searchfields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search(keyword, computers):
    entry_query = get_query(keyword)
    computers = computers.filter(entry_query)
    return computers


def removeKeyword(request):
    if request.GET.get('keyword') is not None:
        request.GET.pop('keyword')


def computersForCatToSold(data_dict):
    ids = data_dict.pop('id')
    computers = Computers.objects.filter(id_computer__in=ids)
    return computers


class ExecutorOfCatToSold:

    def __init__(self, data_dict):
        self.error_list = []
        self.idPrices = {}
        for key, value in data_dict.items():
            if "client" in key:
                self._validate_client(value)
            if "price" in key:
                if self._validate_price(value):
                    self.idPrices[self._getId(key)] = value
        self.validated = len(self.error_list) == 0

    def write_to_database(self):
        dbClient = Clients.objects.get_or_create(client_name=self.client)[0]
        dbClient.save()
        sale = Sales(date_of_sale=timezone.now(), f_id_client=dbClient)
        sale.save()
        for key, value in self.idPrices.items():
            computer = Computers.objects.get(id_computer=key)
            # computer(price=value, f_sale=sale)
            computer.price = value.replace(",", ".")
            computer.f_sale = sale
            computer.save()

    def _validate_client(self, client):
        if client == "":
            self.error_list.append("No client was specified")
        else:
            self.client = client

    def _validate_price(self, price):
        isValidated = True
        empty_price_error = "Not all computers have prices set"
        if price == "":
            if empty_price_error in self.error_list:
                pass
            else:
                self.error_list.append("Not all computers have prices set")
                isValidated = False
        else:
            # min 0.01, max 10000 pagal mariu
            if not re.match(r'^[0-9]+[\.\,]{0,1}[0-9]{0,2}$', price):
                self.error_list.append('Price "'+price+'" is not a valid price')
                isValidated = False
        return isValidated

    def _getId(self, key):
        return key.split("_")[1]

    def get_error_message(self):
        return "\r\n".join(self.error_list)


class NewOrderChoices:

    def __init__(self):
        self._set_clients()
        self._set_testers()

    def _set_clients(self):
        self.clients = [record[0] for record in Clients.objects.values_list("client_name")]

    def _set_testers(self):
        self.testers = [record[0] for record in Testers.objects.values_list("tester_name")]


class NewOrder:

    def __init__(self, data_dict):
        self.data = data_dict
        self.error_list = []

    def save(self):
        print("New order save start")
        self._validate()
        if len(self.error_list) == 0:
            order = self._save_and_get_order()
            tester_names = self.data.pop('tes')
            for tester_name in tester_names:
                tester = Testers.objects.get(tester_name=tester_name)
                ord_tes = OrdTes(
                    f_order=order,
                    f_id_tester=tester
                )
                ord_tes.save()
            print("New order save end")
        else:
            print("New order creation has FAILED")

    def isSaved(self):
        return len(self.error_list) == 0

    def get_error_message(self):
        return "\r\n".join(self.error_list)

    def _validate(self):
        fieldnames = (
            'order_name',
            'client_name',
            'tes'
        )

        error_messages = (
            "Order name was not set",
            "Client was not set",
            "No testers were assigned to the order"
        )

        if self.data.get('order_name') != "" and self.data.get('order_name') is not None:
            if Orders.objects.filter(order_name=self.data.get('order_name')).exists():
                self.error_list.append("Order with such name allready exists")

        for i in range(len(fieldnames)):
            if self.data.get(fieldnames[i]) == "" or self.data.get(fieldnames[i]) is None:
                self.error_list.append(error_messages[i])

    def _save_and_get_order(self):
        client = self._get_or_save_client()
        order = Orders(
            order_name=self.data.pop('order_name')[0],
            is_sent=0,
            creation_date=timezone.now(),
            f_id_client=client
        )
        order.save()
        return order

    def _get_or_save_client(self):
        client = Clients.objects.get_or_create(client_name=self.data.pop('client_name')[0])[0]
        return client


class Order:

    def __init__(self, order_object):
        self.id = order_object.id_order
        self.name = order_object.order_name
        self.isReady = self.get_isReady()
        self.isSent = bool(order_object.is_sent)
        self.date = order_object.creation_date
        self.client = order_object.f_id_client.client_name
        self._set_computer_count()
        self._set_testers()


    def get_isReady(self):
        count = CompOrd.objects.filter(f_order_id_to_order=self.id, is_ready=0).count()
        return not count >= 1

    def _set_computer_count(self):
        self.count = CompOrd.objects.filter(f_order_id_to_order=self.id).count()

    def _set_testers(self):
        self.testers = []
        variables = OrdTes.objects.filter(f_order=self.id)
        for variable in variables:
            self.testers.append(variable.f_id_tester.tester_name)

    def get_testers(self):
        stringToReturn = ""
        try:
            stringToReturn = ", ".join(self.testers)
        except:
            pass
        return stringToReturn

    def get_status(self):
        statuses = ("In-Preperation", "Ready", "Sent", "Empty")
        if self.count == 0:
            return statuses[3]
        elif self.isSent:
            return statuses[2]
        elif self.isReady:
            return statuses[1]
        else:
            return statuses[0]


class OrdersClassAutoFilter:

    def __init__(self, orders):
        self.names = []
        self.clients = []
        self.qtys = []
        self.dates = []
        self.testers = []
        self.statuses = []
        for order in orders:
            self.names.append(order.name)
            self.clients.append(order.client)
            self.qtys.append(order.count)
            self.dates.append(order.date)
            self.testers.extend(order.testers)
            self.statuses.append(order.get_status())
        self.names = self.removeDuplicatesAndSort(self.names)
        self.clients = self.removeDuplicatesAndSort(self.clients)
        self.qtys = self.removeDuplicatesAndSort(self.qtys)
        self.dates = self.removeDuplicatesAndSort(self.dates)
        self.testers = self.removeDuplicatesAndSort(self.testers)
        self.statuses = self.removeDuplicatesAndSort(self.statuses)

    def removeDuplicatesAndSort(self, lst):
        lst = list(set(lst))
        lst.sort()
        return lst


class OrdersClass:

    def __init__(self):
        self.order_list = []
        self._set_orders()
        self.autoFilters = OrdersClassAutoFilter(self.order_list)

    def _set_orders(self):
        orders = Orders.objects.all()
        for ord in orders:
            order = Order(ord)
            self.order_list.append(order)

    def filter(self, data_dict):
        keys = ('ord-af', 'clt-af', 'qty-af', 'dat-af', 'tes-af', 'sta-af')
        new_dict = {}
        if 'orders' in data_dict:
            data_dict.pop('orders')
        for key in keys:
            if key in data_dict:
                new_dict[key] = data_dict.pop(key)
        for key, value in new_dict.items():
            if key == 'ord-af':
                print('ord-af')
                for order in self.order_list[:]:
                    if not order.name in new_dict['ord-af']:
                        self.order_list.remove(order)
            elif key == 'clt-af':
                print('clt-af')
                for order in self.order_list[:]:
                    if not order.client in new_dict['clt-af']:
                        self.order_list.remove(order)
            elif key == 'qty-af':
                print('qty-af')
                for order in self.order_list[:]:
                    if not str(order.count) in new_dict['qty-af']:
                        self.order_list.remove(order)
            elif key == 'dat-af':
                print('dat-af')
                for order in self.order_list[:]:
                    if not str(order.date) in new_dict['dat-af']:
                        self.order_list.remove(order)
            elif key == 'tes-af':
                print('tes-af')
                for order in self.order_list[:]:
                    if not all(x in order.testers for x in new_dict['tes-af']):
                        self.order_list.remove(order)
            elif key == 'sta-af':
                print('sta-af')
                for order in self.order_list[:]:
                    if not order.get_status() in new_dict['sta-af']:
                        self.order_list.remove(order)
        self.autoFilters = OrdersClassAutoFilter(self.order_list)


class PossibleOrders:

    def __init__(self):
        self._set_orders()

    def _set_orders(self):
        # self.orders = [record[0] for record in Orders.objects.values_list("order_name")]
        self.orders = []
        orders = Orders.objects.all()
        for order in orders:
            if order.is_sent != 1:
                self.orders.append(order.order_name)


def assignComputersToOrderUsingDict(dict):
    order_name = next(iter(dict))
    indexes = dict[order_name]
    order = Orders.objects.get(order_name=order_name)
    for ind in indexes:
        compord = CompOrd(is_ready=0, f_order_id_to_order=order)
        compord.save()
        computer = Computers.objects.get(id_computer=ind)
        computer.f_id_comp_ord = compord
        computer.save()


class TesterCustomClass:

    def __init__(self, tester_name, assigned):
        self.tester_name = tester_name
        self.assigned = assigned


class OrderToEdit:

    def __init__(self, index):
        self._get_order(index)
        self._get_computers_from_order()
        self._get_testers()
        self.error_list = []
        self.count = 0

    def increment(self):
        self.count += 1
        return ''

    def _get_order(self, index):
        ord = Orders.objects.get(id_order=index)
        self.order = Order(ord)

    def _get_computers_from_order(self):
        compords = CompOrd.objects.filter(f_order_id_to_order=self.order.id)
        compordsIds = [record.id_comp_ord for record in compords]
        self.computers = Computers.objects.filter(f_id_comp_ord__in=compordsIds)

    def _get_testers(self):
        self.testers = []
        testers = Testers.objects.all()
        for tester in testers:
            custom_tester = TesterCustomClass(tester.tester_name, tester.tester_name in self.order.testers)
            self.testers.append(custom_tester)

    def isSaved(self):
        return len(self.error_list) == 0

    def get_error_message(self):
        return "\r\n".join(self.error_list)

    def set_new_data(self, data_dict):
        def _validate():
            fieldnames = (
                'order_id',
                'order_name',
                'client_name',
                'tes'
            )
            error_messages = (
                "!!!No order id!!!",
                "Order name was not set",
                "Client name was not set",
                "Testers were not set",
            )
            for i in range(len(fieldnames)):
                if data_dict.get(fieldnames[i]) == "" or data_dict.get(fieldnames[i]) is None:
                    self.error_list.append(error_messages[i])
            if self.order.isSent:
                self.error_list.append('Sent orders are not allowed for editing')

        def _save():
            order = Orders.objects.get(id_order=order_id)
            order.order_name = new_order_name
            client = Clients.objects.get_or_create(client_name=new_client_name)[0]
            order.f_id_client = client
            order.is_sent = new_is_sent_status
            order.save()
            sale = None
            if new_is_sent_status == 1:
                sale = Sales(date_of_sale=timezone.now(), f_id_client=order.f_id_client)
                sale.save()
            OrdTes.objects.filter(f_order=order).delete()
            for tester_name in testers:
                tester = Testers.objects.get(tester_name=tester_name)
                new_ordtes = OrdTes(f_order=order, f_id_tester=tester)
                new_ordtes.save()
            for status_holder in statuses:
                computer = Computers.objects.get(id_computer=status_holder.computer_id)
                compord = CompOrd.objects.get(id_comp_ord=computer.f_id_comp_ord.id_comp_ord)
                compord.is_ready = status_holder.value
                compord.save()
                computer.f_sale = sale
                computer.save()

            """
            if new_is_sent_status==1:
                for status_holder in statuses:
                    computer = Computers.objects.get(id_computer=status_holder.computer_id)
            """

        _validate()
        if len(self.error_list) == 0:
            order_id = data_dict.pop('order_id')[0]
            new_order_name = data_dict.pop('order_name')[0]
            new_client_name = data_dict.pop('client_name')[0]
            testers = data_dict.pop('tes')
            new_is_sent_status = 0
            if 'set_as_sent' in data_dict:
                received_is_sent_status = data_dict.pop('set_as_sent')[0]
                if received_is_sent_status == 'on':
                    new_is_sent_status = 1
            statuses = []
            for key, value in data_dict.items():
                if 'status' in key:
                    sh = StatusHolder(key, value)
                    statuses.append(sh)
            for status in statuses:
                data_dict.pop('status_'+status.computer_id)
            _save()


class StatusHolder:
    statuses = ("In-Preperation", "Ready")

    def __init__(self, key, value):
        self.computer_id = key.split('_')[1]
        self.value = None
        try:
            self.value = self.statuses.index(value)
        except ValueError:
            pass

