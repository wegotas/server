from ULCDTinterface.modelers import Computers, Bioses, Batteries, Cpus, CameraOptions, Categories, Computers, Diagonals, Gpus, HddSizes, Hdds, Licenses, Manufacturers, Models, Motherboards, RamSizes, Rams, Testers, Types, BatToComp, RamToComp, HddToComp

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

        self._type_save(self.data_dict.pop("type_name", "")[0])
        self._category_save(self.data_dict.pop("category_name", "")[0])
        self._tester_save(self.data_dict.pop("tester_name", "")[0])
        self._bios_save(self.data_dict.pop("bios_text", "")[0])
        self._cpu_save(self.data_dict.pop("cpu_name", "")[0])
        self._camera_option_save(self.data_dict.pop("option_name", "")[0])
        self._diagonal_save(self.data_dict.pop("diagonal_text", "")[0])
        self._gpu_save(self.data_dict.pop("gpu_name", "")[0])
        self._hddsize_save(self.data_dict.pop("hdd_size_text", "")[0])
        self._license_save(self.data_dict.pop("license_name", "")[0])
        self._manufacturer_save(self.data_dict.pop("manufacturer_name", "")[0])
        self._model_save(self.data_dict.pop("model_name", "")[0])
        self._motherboard_save(self.data_dict.pop("motherboard_serial", "")[0])
        self._ramsize_save(self.data_dict.pop("ram_size_text", "")[0])
        self._computer_save()
        self._process_ram_and_hdd_serials()
        self._process_batteries()

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
            f_motherboard=self.motherboard,
        )
        self.computer.save()

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
        self.hddsize = HddSizes.objects.get_or_create(hdd_size_text=value)[0]

    def _license_save(self, value):
        self.license = Licenses.objects.get_or_create(license_name=value)[0]

    def _manufacturer_save(self, value):
        self.manufacturer = Manufacturers.objects.get_or_create(manufacturer_name=value)[0]

    def _model_save(self, value):
        self.model = Models.objects.get_or_create(model_name=value)[0]

    def _motherboard_save(self, value):
        self.motherboard = Motherboards.objects.get_or_create(motherboard_serial=value)[0]

    def _ramsize_save(self, value):
        self.ramsize = RamSizes.objects.get_or_create(ram_size_text=value)[0]


def edit_post(data_dict):
    data_dict.pop("edit", "")
    id_computer = data_dict.pop("id_computer", "")[0]
    print("id_computer: " + id_computer)
    serial = data_dict.pop("serial", "")[0]
    print("serial: " + serial)
    type_name = data_dict.pop("type_name", "")[0]
    print("type_name: " + type_name)
    category_name = data_dict.pop("category_name", "")[0]
    print("category_name: " + category_name)
    manufacturer = data_dict.pop("manufacturer_name", "")[0]
    print("manufacturer_name: " + manufacturer)
    model = data_dict.pop("model_name", "")[0]
    print("model_name: " + model)
    cpu = data_dict.pop("cpu_name", "")[0]
    print("cpu_name: " + cpu)
    gpu = data_dict.pop("gpu_name", "")[0]
    print("gpu_name: " + gpu)
    ram_size = data_dict.pop("ram_size_text", "")[0]
    print("ram_size_text: " + ram_size)
    hdd_size = data_dict.pop("hdd_size_text", "")[0]
    print("hdd_size_text: " + hdd_size)
    diagonal = data_dict.pop("diagonal_text", "")[0]
    print("diagonal_text: " + diagonal)
    license_name = data_dict.pop("license_name", "")[0]
    print("license_name: " + license_name)
    option_name = data_dict.pop("option_name", "")[0]
    print("option_name: " + option_name)
    cover = data_dict.pop("cover", "")[0]
    print("cover: " + cover)
    display = data_dict.pop("display", "")[0]
    print("display: " + display)
    bezel = data_dict.pop("bezel", "")[0]
    print("bezel: " + bezel)
    keyboard = data_dict.pop("keyboard", "")[0]
    print("keyboard: " + keyboard)
    mouse = data_dict.pop("mouse", "")[0]
    print("mouse: " + mouse)
    sound = data_dict.pop("sound", "")[0]
    print("sound: " + sound)
    cdrom = data_dict.pop("cdrom", "")[0]
    print("cdrom: " + cdrom)
    hdd_cover = data_dict.pop("hdd_cover", "")[0]
    print("hdd_cover: " + hdd_cover)
    ram_cover = data_dict.pop("ram_cover", "")[0]
    print("ram_cover: " + ram_cover)
    other = data_dict.pop("other", "")[0]
    print("other: " + other)
    tester_name = data_dict.pop("tester_name", "")[0]
    print("tester_name: " + tester_name)
    date = data_dict.pop("date", "")[0]
    print("date: " + date)
    bios_text = data_dict.pop("bios_text", "")[0]
    print("bios_text: " + bios_text)
    motherboard = data_dict.pop("motherboard_serial", "")[0]
    print(motherboard)
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


class CatTyp:

    def __init__(self):
        self.innerList = []
        query = """select distinct tp.id_type, tp.type_name, cat.category_name from sopena_computers.Types as tp
join sopena_computers.Computers as comp on comp.f_type_id = tp.id_type
join sopena_computers.Categories as cat on cat.id_category = comp.f_category_id"""
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

def getQty(request):
    if request.GET.get('qty') is None:
        return 10
    else:
        return int(request.GET.get('qty'))

def getPage(request):
    if request.GET.get('page') is None:
        return 1
    else:
        return int(request.GET.get('page'))

def getType(request):
    if request.GET.get('type') is None:
        return None
    else:
        return request.GET.get('type')

def getCat(request):
    if request.GET.get('cat') is None:
        return None
    else:
        return request.GET.get('cat')

def getKeyword(request):
    if request.GET.get('keyword') is None:
        return None
    else:
        return request.GET.get('keyword')