from ULCDTinterface.modelers import BatToComp, HddToComp, RamToComp

class Bat_holder():
    def __init__(self, index=1, id=0, serial="N/A", wear="N/A", time="N/A"):
        self.index = index
        self.id = id
        self.serial = serial
        self.wear = wear
        self.time = time


def get_batteries(computer_id):
    print("Get batteries called")
    batteries = BatToComp.objects.filter(f_id_computer_bat_to_com=computer_id)
    bat_list = []
    if batteries:
        print("batteries Exists")
        i = 0
        for battery in batteries.iterator():
            bat_dict = dict()
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
    print("Get rams called")
    rams = RamToComp.objects.filter(f_id_computer_ram_to_com=computer_id)
    ram_list = []
    if rams:
        ram_dict = dict()
        print("rams Exists")
        i = 0
        for ram in rams.iterator():
            bat_dict = dict()
            i += 1
            if ram.f_id_ram_ram_to_com.ram_serial != "N/A":
                """
                ram_dict["Index"] = i
                ram_dict["Id"] = ram.id_ram_to_comp
                ram_dict["Serial"] = ram.f_id_ram_ram_to_com.ram_serial
                ram_list.append(ram_dict)
                """
                ram = Ram_Hdd_holder(
                    index=i,
                    id=ram.id_ram_to_comp,
                    serial=ram.f_id_ram_ram_to_com.ram_serial
                )
                ram_list.append(ram)
        if len(ram_list) == 0:
            """
            ram_dict = dict()
            ram_dict["Index"] = 1
            ram_dict["Id"] = 0
            ram_dict["Serial"] = "N/A"
            ram_list.append(ram_dict)
            """
            ram = Ram_Hdd_holder()
            ram_list.append(ram)
        return ram_dict
    else:
        print("Rams asociated with this computer do not exist")
    return ram_list

def get_hdds(computer_id):
    print("Get hdds called")
    hdds = HddToComp.objects.filter(f_id_computer_hdd_to_com=computer_id)
    hdd_list = []
    if hdds:
        hdd_dict = dict()
        print("hdds Exists")
        i = 0
        for hdd in hdds.iterator():
            i += 1
            if hdd.f_id_hdd_hdd_to_com.hdd_serial != "N/A":
                hdd_dict["Index"] = i
                hdd_dict["Id"] = hdd.id_hdd_to_comp
                hdd_dict["Serial"] = hdd.f_id_hdd_hdd_to_com.hdd_serial
                hdd_list.append(hdd_dict)
        if len(hdd_list) == 0:
            hdd_dict = dict()
            hdd_dict["Index"] = i
            hdd_dict["Id"] = hdd.id_hdd_to_comp
            hdd_dict["Serial"] = hdd.f_id_hdd_hdd_to_com.hdd_serial
            hdd_list.append(hdd_dict)
    else:
        print("Hdds asociated with this computer do not exist")
    return hdd_list

