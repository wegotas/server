from ULCDTinterface.modelers import Computers, Bioses, Batteries, Cpus, CameraOptions, Categories, Computers, Diagonals, Gpus, HddSizes, Hdds, Licenses, Manufacturers, Models, Motherboards, RamSizes, Rams, Testers, Types, BatToComp, RamToComp, HddToComp
import datetime

class Computer_record():

    def __init__(self, data_dict):
        print("in Computer_record")
        self.message = ""
        self.success = None
        try:
            self.category = self._category_get(data_dict["Category"])
            self.type = self._type_get(data_dict["Computer type"])
            self.tester = self._tester_get(data_dict["Tester"])
            self.bios = self._bios_save_and_get(data_dict["BIOS"])
            self.cpu = self._cpus_save_and_get(data_dict["CPU"])
            self.camera_option = self._camera_option_save_and_get(data_dict["Camera"])
            self.diagonal = self._diagonals_save_and_get(data_dict["Diagonal"])
            self.gpu = self._gpus_save_and_get(data_dict["GPU"])
            self.hddsize = self._hddSizes_save_and_get(data_dict["HDD"])
            self.license = self._licenses_save_and_get(data_dict["License"])
            self.manufacturer = self._manufacturers_save_and_get(data_dict["Manufacturer"])
            self.model = self._models_save_and_get(data_dict["Model"])
            self.motherboard = self._motherboards_save_and_get(data_dict["motherboard_serial"])
            self.ramsize = self._ramSizes_save_and_get(data_dict["RAM"])
            self.timenow = datetime.datetime.now()
            self.computer = self._computer_save_and_get(data_dict)
            if data_dict["Category"] == "Sold":
                bat1 = self._battery_save_and_get(
                    data_dict["Bat1 serial"],
                    data_dict["Bat1 wear"],
                    data_dict["Bat1 expected time"]
                )
                self._bat_to_comp_relation_creation(bat1)

                bat2 = self._battery_save_and_get(
                    data_dict["Bat2 serial"],
                    data_dict["Bat2 wear"],
                    data_dict["Bat2 expected time"]
                )
                self._bat_to_comp_relation_creation(bat2)

                ram1 = self._ram_save_and_get(data_dict["ram_serial1"])
                self._ram_to_comp_relation_creation(ram1)
                ram2 = self._ram_save_and_get(data_dict["ram_serial2"])
                self._ram_to_comp_relation_creation(ram2)
                ram3 = self._ram_save_and_get(data_dict["ram_serial3"])
                self._ram_to_comp_relation_creation(ram3)
                ram4 = self._ram_save_and_get(data_dict["ram_serial4"])
                self._ram_to_comp_relation_creation(ram4)
                ram5 = self._ram_save_and_get(data_dict["ram_serial5"])
                self._ram_to_comp_relation_creation(ram5)
                ram6 = self._ram_save_and_get(data_dict["ram_serial6"])
                self._ram_to_comp_relation_creation(ram6)

                hdd1 = self._hdd_save_and_get(data_dict["hdd_serial1"])
                self._hdd_to_comp_relation_creation(hdd1)
                hdd2 = self._hdd_save_and_get(data_dict["hdd_serial2"])
                self._hdd_to_comp_relation_creation(hdd2)
                hdd3 = self._hdd_save_and_get(data_dict["hdd_serial2"])
                self._hdd_to_comp_relation_creation(hdd3)
                self.message += "Sold category's additional serial fields have been processed\n"
            self.message += "Success"
            self.success = True
        except Exception as e:
            self.message += "Failure\nPossible reason:\n"
            self.message += str(e)
            self.success = False

    def _bat_to_comp_relation_creation(self, bat):
        try:
            existing_bat_to_comp = BatToComp.objects.filter(
                f_id_computer_bat_to_com=self.computer,
                f_bat_bat_to_com=bat
            ).first()
        except BatToComp.DoesNotExist:
            bat_to_comp =BatToComp(
                f_id_computer_bat_to_com=self.computer,
                f_bat_bat_to_com=bat
            )
            bat_to_comp.save()

    def _ram_to_comp_relation_creation(self, ram):
        try:
            existing_ram_to_comp = RamToComp.objects.filter(
                f_id_computer_ram_to_com=self.computer,
                f_id_ram_ram_to_com=ram
            ).first()
        except RamToComp.DoesNotExist:
            ram_to_comp =RamToComp(
                f_id_computer_ram_to_com=self.computer,
                f_id_ram_ram_to_com=ram
            )
            ram_to_comp.save()

    def _hdd_to_comp_relation_creation(self, hdd):
        try:
            existing_hdd_to_comp = HddToComp.objects.filter(
                f_id_computer_hdd_to_com=self.computer,
                f_id_hdd_hdd_to_com=hdd
            ).first()
        except RamToComp.DoesNotExist:
            hdd_to_comp =HddToComp(
                f_id_computer_hdd_to_com=self.computer,
                f_id_hdd_hdd_to_com=hdd
            )
            hdd_to_comp.save()

    def _battery_save_and_get(self, serial, wear_out, expected_time):
        try:
            battery = Batteries.objects.get(
                serial=serial,
                wear_out=wear_out,
                expected_time=expected_time
            )
            return battery
        except Batteries.DoesNotExist:
            battery = Batteries(
                serial=serial,
                wear_out=wear_out,
                expected_time=expected_time
            )
            battery.save()
            return battery

    def _ram_save_and_get(self, value):
        try:
            ram = Rams.objects.get(ram_serial=value)
            return ram
        except Rams.DoesNotExist:
            ram = Rams(ram_serial=value)
            ram.save()
            return ram

    def _hdd_save_and_get(self, value):
        try:
            hdd = Hdds.objects.get(hdd_serial=value)
            return hdd
        except Hdds.DoesNotExist:
            hdd = Hdds(hdd_serial=value)
            hdd.save()
            return hdd

    def _computer_save_and_get(self, data):
        try:
            existing_computer = Computers.objects.get(computer_serial=data['Serial'])
            computer = Computers(
                id_computer=existing_computer.id_computer,
                computer_serial=data['Serial'],
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
                f_tester=self.tester,
                date=self.timenow,
                f_bios=self.bios,
                f_motherboard=self.motherboard,
            )
            computer.save()
            self.message+="Existing record has been updated\n"
            return computer
        except Computers.DoesNotExist:
            print("No computer with such serial, inserting a new record")
            computer = Computers(
                computer_serial=data['Serial'],
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
                f_tester=self.tester,
                date=self.timenow,
                f_bios=self.bios,
                f_motherboard=self.motherboard,
            )
            computer.save()
            self.message += "New record has been added\n"
            return computer

    def _category_get(self, value):
        return Categories.objects.get(category_name=value)

    def _type_get(self, value):
        return Types.objects.get(type_name=value)

    def _tester_get(self, value):
        return Testers.objects.get(tester_name=value)

    def _bios_save_and_get(self, value):
        try:
            bios = Bioses.objects.get(bios_text=value)
            return bios
        except Bioses.DoesNotExist:
            bios = Bioses(bios_text=value)
            bios.save()
            return bios

    def _cpus_save_and_get(self, value):
        try:
            cpu = Cpus.objects.get(cpu_name=value)
            return cpu
        except Cpus.DoesNotExist:
            cpu = Bioses(cpu_name=value)
            cpu.save()
            return cpu

    def _camera_option_save_and_get(self, value):
        try:
            option = CameraOptions.objects.get(option_name=value)
            return option
        except CameraOptions.DoesNotExist:
            option = CameraOptions(option_name=value)
            option.save()
            return option

    def _diagonals_save_and_get(self, value):
        try:
            diagonal = Diagonals.objects.get(diagonal_text=value)
            return diagonal
        except Diagonals.DoesNotExist:
            diagonal = Diagonals(diagonal_text=value)
            diagonal.save()
            return diagonal

    def _gpus_save_and_get(self, value):
        try:
            gpu = Gpus.objects.get(gpu_name=value)
            return gpu
        except Gpus.DoesNotExist:
            gpu = Gpus(gpu_name=value)
            gpu.save()
            return gpu

    def _hddSizes_save_and_get(self, value):
        try:
            hddSize = HddSizes.objects.get(hdd_size_text=value)
            return hddSize
        except HddSizes.DoesNotExist:
            hddSize = HddSizes(hdd_size_text=value)
            hddSize.save()
            return hddSize

    def _licenses_save_and_get(self, value):
        try:
            license = Licenses.objects.get(license_name=value)
            return license
        except Licenses.DoesNotExist:
            license = Licenses(license_name=value)
            license.save()
            return license

    def _manufacturers_save_and_get(self, value):
        try:
            manufacturer = Manufacturers.objects.get(manufacturer_name=value)
            return manufacturer
        except Manufacturers.DoesNotExist:
            manufacturer = Manufacturers(manufacturer_name=value)
            manufacturer.save()
            return manufacturer

    def _models_save_and_get(self, value):
        try:
            model = Models.objects.get(model_name=value)
            return model
        except Models.DoesNotExist:
            model = Models(model_name=value)
            model.save()
            return model

    def _motherboards_save_and_get(self, value):
        try:
            motherboard = Motherboards.objects.get(motherboard_serial=value)
            return motherboard
        except Motherboards.DoesNotExist:
            motherboard = Motherboards(motherboard_serial=value)
            motherboard.save()
            return motherboard

    def _ramSizes_save_and_get(self, value):
        try:
            ramSize = RamSizes.objects.get(ram_size_text=value)
            return ramSize
        except RamSizes.DoesNotExist:
            ramSize = RamSizes(ram_size_text=value)
            ramSize.save()
            return ramSize