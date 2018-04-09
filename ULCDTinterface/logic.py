from ULCDTinterface.modelers import Computers, Bioses, Batteries, Cpus, CameraOptions, Categories, Computers, Diagonals, Gpus, HddSizes, Hdds, Licenses, Manufacturers, Models, Motherboards, RamSizes, Rams, Testers, Types
import datetime

class Computer_record():

    def __init__(self, data_dict):
        print("in Computer_record")
        self.category_id = self._category_getid(data_dict["Category"])
        self.type_id = self._type_getid(data_dict["Computer type"])
        self.test_id = self._tester_getid(data_dict["Tester"])
        self.bios_id = self._bios_save_and_getid(data_dict["BIOS"])
        self.cpu_id = self._cpus_save_and_getid(data_dict["CPU"])
        self.camera_option_id = self._camera_option_save_and_getid(data_dict["Camera"])
        self.diagonal_id = self._diagonals_save_and_getid(data_dict["Diagonal"])
        self.gpu_id = self._gpus_save_and_getid(data_dict["GPU"])
        self.hddsize_id = self._hddSizes_save_and_getid(data_dict["HDD"])
        self.license_id = self._licenses_save_and_getid(data_dict["License"])
        self.manufacturer_id = self._manufacturers_save_and_getid(data_dict["Manufacturer"])
        self.model_id = self._models_save_and_getid(data_dict["Model"])
        self.motherboard_id = self._motherboards_save_and_getid(data_dict["motherboard_serial"])
        self.ramsize_id = self._ramSizes_save_and_getid(data_dict["RAM"])
        self.timenow = datetime.datetime.now()
        self.computer_id = self._computer_save_and_getid(data_dict)

    # SIS METODAS DAR NEUZBAIGTAS KARTU SU HDD IR RAMU METODU. PO TO JU VISU ID TURETU SAUGOTI x_to_comp LENTELESE!!!
    def _battery_save_and_getid(self, serial, wear_out, expected_time):
        try:
            bios = Batteries.objects.get(
                serial=serial,
                wear_out=wear_out,
                expected_time=expected_time
            )
            print("bios: " + value + "\nIt's id is: " + bios.id_bios)
            return bios.id_bios
        except Bioses.DoesNotExist:
            print("no such bios exception: " + value)
            bios = Bioses(bios_text=value)
            bios.save()
            return bios.id_bios

    """
    def _battery_save(self, serial, wear_out, expected_time):
        if serial == "N/A" and wear_out == "N/A" and expected_time == "N/A":
            existing_battery
        battery = Batteries(
            serial=serial,
            wear_out=wear_out,
            expected_time=expected_time,
            f_id_computer_battery=self.computer_id
        )
        battery.save()
    """

    def _computer_save_and_getid(self, data):
        try:
            existing_computer = Computers.objects.get(computer_serial=data['Serial'])
            computer = Computers(
                id_computer=existing_computer.id_computer,
                computer_serial=data['Serial'],
                f_type=self.type_id,
                f_category=self.category_id,
                f_manufacturer=self.manufacturer_id,
                f_model=self.model_id,
                f_cpu=self.cpu_id,
                f_gpu=self.gpu_id,
                f_ram_size=self.ramsize_id,
                f_hdd_size=self.hddsize_id,
                f_diagonal=self.diagonal_id,
                f_license=self.license_id,
                f_camera=self.camera_option_id,
                cover=data["Cover"],
                display=data["Display"],
                bezel=data["Bezel"],
                keyboard=data["Keyboard"],
                mouse=data["Mouse"],
                sound=data["Sound"],
                cdrom=data["CD-ROM"],
                hdd_cover=data["HDD Cover"],
                ram_cover=data["RAM Cover"],
                other=data["Other"],
                f_tester=self.test_id,
                date=self.timenow,
                f_bios=self.bios_id,
                f_motherboard=self.motherboard_id,
            )
            computer.save()
            return computer.id_computer
        except Computers.DoesNotExist:
            print("No computer with such serial, inserting a new record")
            computer = Computers(
                computer_serial=data['Serial'],
                f_type=self.type_id,
                f_category=self.category_id,
                f_manufacturer=self.manufacturer_id,
                f_model=self.model_id,
                f_cpu=self.cpu_id,
                f_gpu=self.gpu_id,
                f_ram_size=self.ramsize_id,
                f_hdd_size=self.hddsize_id,
                f_diagonal=self.diagonal_id,
                f_license=self.license_id,
                f_camera=self.camera_option_id,
                cover=data["Cover"],
                display=data["Display"],
                bezel=data["Bezel"],
                keyboard=data["Keyboard"],
                mouse=data["Mouse"],
                sound=data["Sound"],
                cdrom=data["CD-ROM"],
                hdd_cover=data["HDD Cover"],
                ram_cover=data["RAM Cover"],
                other=data["Other"],
                f_tester=self.test_id,
                date=self.timenow,
                f_bios=self.bios_id,
                f_motherboard=self.motherboard_id,
            )
            computer.save()
            return computer.id_computer

    def _category_getid(self, value):
        category_id = Categories.objects.get(category_name=value).id_category
        return category_id

    def _type_getid(self, value):
        type_id = Types.objects.get(type_name=value).id_type
        return type_id

    def _tester_getid(self, value):
        tester_id = Testers.objects.get(tester_name=value).id_tester
        return tester_id

    def _bios_save_and_getid(self, value):
        try:
            bios = Bioses.objects.get(bios_text=value)
            print("bios: " + value + "\nIt's id is: " + bios.id_bios)
            return bios.id_bios
        except Bioses.DoesNotExist:
            print("no such bios exception: " + value)
            bios = Bioses(bios_text=value)
            bios.save()
            return bios.id_bios

    def _cpus_save_and_getid(self, value):
        try:
            cpu = Cpus.objects.get(cpu_name=value)
            print("cpu: " + value + "\nIt's id is: " + cpu.id_cpu)
            return cpu.id_cpu
        except Cpus.DoesNotExist:
            print("no such cpu exception: " + value)
            cpu = Bioses(cpu_name=value)
            cpu.save()
            return cpu.id_cpu

    def _camera_option_save_and_getid(self, value):
        try:
            option = CameraOptions.objects.get(option_name=value)
            print("camera option: " + value + "\nIt's id is: " + option.id_camera_options)
            return option.id_camera_options
        except CameraOptions.DoesNotExist:
            print("no such CameraOptions exception: " + value)
            option = CameraOptions(option_name=value)
            option.save()
            return option.id_camera_options

    def _diagonals_save_and_getid(self, value):
        try:
            diagonal = Diagonals.objects.get(diagonal_text=value)
            print("diagonal: " + value + "\nIt's id is: " + diagonal.id_diagonal)
            return diagonal.id_diagonal
        except Diagonals.DoesNotExist:
            print("no such diagonals exception: " + value)
            diagonal = Diagonals(diagonal_text=value)
            diagonal.save()
            return diagonal.id_diagonal

    def _gpus_save_and_getid(self, value):
        try:
            gpu = Gpus.objects.get(gpu_name=value)
            print("gpu: " + value + "\nIt's id is: " + gpu.id_gpu)
            return gpu.id_gpu
        except Gpus.DoesNotExist:
            print("no such Gpus exception: " + value)
            gpu = Gpus(gpu_name=value)
            gpu.save()
            return gpu.id_gpu

    def _hddSizes_save_and_getid(self, value):
        try:
            hddSize = HddSizes.objects.get(hdd_size_text=value)
            print("hdd_size: " + value + "\nIt's id is: " + hddSize.id_hdd_sizes)
            return hddSize.id_hdd_sizes
        except HddSizes.DoesNotExist:
            print("no such hdd_size exception: " + value)
            hddSize = HddSizes(hdd_size_text=value)
            hddSize.save()
            return hddSize.id_hdd_sizes

    def _licenses_save_and_getid(self, value):
        try:
            license = Licenses.objects.get(license_name=value)
            print("license: " + value + "\nIt's id is: " + license.id_license)
            return license.id_license
        except Licenses.DoesNotExist:
            print("no such license exception: " + value)
            license = Licenses(license_name=value)
            license.save()
            return license.id_license

    def _manufacturers_save_and_getid(self, value):
        try:
            manufacturer = Manufacturers.objects.get(manufacturer_name=value)
            print("manufacturer: " + value + "\nIt's id is: " + manufacturer.id_manufacturer)
            return manufacturer.id_manufacturer
        except Manufacturers.DoesNotExist:
            print("no such manufacturer exception: " + value)
            manufacturer = Manufacturers(manufacturer_name=value)
            manufacturer.save()
            return manufacturer.id_manufacturer

    def _models_save_and_getid(self, value):
        try:
            model = Models.objects.get(model_name=value)
            print("model: " + value + "\nIt's id is: " + model.id_model)
            return model.id_model
        except Models.DoesNotExist:
            print("no such model exception: " + value)
            model = Models(model_name=value)
            model.save()
            return model.id_model

    def _motherboards_save_and_getid(self, value):
        try:
            motherboard = Motherboards.objects.get(motherboard_serial=value)
            print("motherboard: " + value + "\nIt's id is: " + motherboard.id_motherboard)
            return motherboard.id_motherboard
        except Motherboards.DoesNotExist:
            print("no such motherboard exception: " + value)
            motherboard = Motherboards(motherboard_serial=value)
            motherboard.save()
            return motherboard.id_motherboard

    def _ramSizes_save_and_getid(self, value):
        try:
            ramSize = RamSizes.objects.get(ram_size_text=value)
            print("ramSize: " + value + "\nIt's id is: " + ramSize.id_ram_size)
            return ramSize.id_ram_size
        except RamSizes.DoesNotExist:
            print("no such ramSize exception: " + value)
            ramSize = RamSizes(ram_size_text=value)
            ramSize.save()
            return ramSize.id_ram_size