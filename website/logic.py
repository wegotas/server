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
                print("Before appending")
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
        print("test")
        self.existing_computer = Computers(id_computer=data_dict.pop("id_computer", "")[0])

        self._type_save(data_dict.pop("type_name", "")[0])
        self._tester_save(data_dict.pop("tester_name", "")[0])
        self._bios_save(data_dict.pop("bios_text", "")[0])
        self._cpu_save(data_dict.pop("cpu_name", "")[0])
        self._camera_option_save(data_dict.pop("option_name", "")[0])
        self._camera_option_save(data_dict.pop("option_name", "")[0])
        self._diagonal_save(data_dict.pop("diagonal_text", "")[0])

    def _type_save(self, value):
        self.type = Types.objects.get_or_create(type_name=value)

    def _tester_save(self, value):
        self.tester = Testers.objects.get_or_create(tester_name=value)

    def _bios_save(self, value):
        self.bios = Bioses.objects.get_or_create(bios_text=value)

    def _cpu_save(self, value):
        self.cpu = Cpus.objects.get_or_create(cpu_name=value)

    def _camera_option_save(self, value):
        self.camera_option = CameraOptions.objects.get_or_create(option_name=value)

    def _diagonal_save(self, value):
        self.diagonal = Diagonals.objects.get_or_create(diagonal_text=value)

    def _gpu_save(self, value):
        self.gpu = Gpus.objects.get_or_create(gpu_name=value)

    def _hddsize_save(self, value):
        self.hddsize = HddSizes.objects.get_or_create(hdd_size_text=value)

    def _license_save(self, value):
        self.license = Licenses.objects.get_or_create(license_name=value)

    def _manufacturer_save(self, value):
        self.manufacturer = Manufacturers.objects.get_or_create(manufacturer_name=value)

    def _model_save(self, value):
        self.model = Models.objects.get_or_create(model_name=value)

    def _motherboard_save(self, value):
        self.motherboard = Motherboards.objects.get_or_create(motherboard_serial=value)

    def _ramsize_save(self, value):
        self.ramsize = RamSizes.objects.get_or_create(ram_size_text=value)


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
    print("hdd_size_text: " + ram_size)
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