from ULCDTinterface.modelers import Computers, Bioses, Batteries, Cpus, CameraOptions, Categories, Computers, Clients, Sales, Diagonals, Gpus, HddSizes, Hdds, Licenses, Manufacturers, Models, RamSizes, Rams, Testers, Types, BatToComp, RamToComp, HddToComp
import datetime, decimal
from django.utils import timezone

class Computer_record():

    def __init__(self, data_dict):
        print("in Computer_record")
        self.message = ""
        self.success = None
        try:
            self.category = self._category_get(data_dict["Category"])
            self.type = self._type_get(data_dict["System Type"])
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
            # self.motherboard = data_dict["motherboard_serial"]
            self.ramsize = self._ramSizes_save_and_get(data_dict["RAM"])
            self.is_sold = data_dict["IsSold"]
            print("IsSold: " + str(self.is_sold))
            self.price = self._price_get(data_dict["Price"])
            self.timenow = timezone.now()
            if self.is_sold:
                self.client = self._client_save_and_get(data_dict["Client"])
                self.sale = self._sale_save_and_get(self.client)
                self.computer = self._computer_sold_save_and_get(data_dict)
                self.message += "Sold have been processed\n"
            else:
                self.computer = self._computer_save_and_get(data_dict)
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

            self._ram_to_comp_relation_creation(self._ram_save_and_get(data_dict["ram_serial1"]))
            self._ram_to_comp_relation_creation(self._ram_save_and_get(data_dict["ram_serial2"]))
            self._ram_to_comp_relation_creation(self._ram_save_and_get(data_dict["ram_serial3"]))
            self._ram_to_comp_relation_creation(self._ram_save_and_get(data_dict["ram_serial4"]))
            self._ram_to_comp_relation_creation(self._ram_save_and_get(data_dict["ram_serial5"]))
            self._ram_to_comp_relation_creation(self._ram_save_and_get(data_dict["ram_serial6"]))

            self._hdd_to_comp_relation_creation(self._hdd_save_and_get(data_dict["hdd_serial1"]))
            self._hdd_to_comp_relation_creation(self._hdd_save_and_get(data_dict["hdd_serial2"]))
            self._hdd_to_comp_relation_creation(self._hdd_save_and_get(data_dict["hdd_serial3"]))
            self.message += "Success"
            self.success = True
        except decimal.InvalidOperation as e:
            self.message += "Failure\nPossible reason:\n"
            self.message += str(e)
            self.success = False
        except Exception as e:
            self.message += "Failure\nPossible reason:\n"
            self.message += str(e)
            self.success = False

    def _price_get(self, price):
        try:
            return float(price.replace(',', '.'))
        except ValueError:
            return 0

    def _bat_to_comp_relation_creation(self, bat):
        bat_to_comp, created = BatToComp.objects.get_or_create(
            f_id_computer_bat_to_com=self.computer,
            f_bat_bat_to_com=bat
        )

    def _ram_to_comp_relation_creation(self, ram):
        ram_to_comp = RamToComp.objects.get_or_create(
            f_id_computer_ram_to_com=self.computer,
            f_id_ram_ram_to_com=ram
        )

    def _hdd_to_comp_relation_creation(self, hdd):
        hdd_to_comp = HddToComp.objects.get_or_create(
            f_id_computer_hdd_to_com=self.computer,
            f_id_hdd_hdd_to_com=hdd
        )

    def _client_save_and_get(self, client_name):
        client = Clients.objects.get_or_create(client_name=client_name)[0]
        client.save()
        return client

    def _sale_save_and_get(self, client):
        sale = Sales.objects.get_or_create(
            date_of_sale=self.timenow,
            f_id_client=client

        )[0]
        sale.save()
        return sale

    def _battery_save_and_get(self, serial, wear_out, expected_time):

        battery = Batteries.objects.get_or_create(
            serial=serial,
            wear_out=wear_out,
            expected_time=expected_time
        )[0]
        battery.save()
        return battery

    def _ram_save_and_get(self, value):
        ram = Rams.objects.get_or_create(ram_serial=value)[0]
        ram.save()
        return ram

    def _hdd_save_and_get(self, value):
        hdd = Hdds.objects.get_or_create(hdd_serial=value)[0]
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
                motherboard_serial=data["motherboard_serial"],
                # price=self.price
            )
            computer.save()
            self.message += "Existing record has been updated\n"
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
                motherboard_serial=data["motherboard_serial"],
                # price=self.price
            )
            computer.save()
            self.message += "New record has been added\n"
            return computer

    def _computer_sold_save_and_get(self, data):
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
                motherboard_serial=data["motherboard_serial"],
                price=self.price,
                f_sale=self.sale
            )
            computer.save()
            self.message += "Existing record has been updated\n"
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
                motherboard_serial=data["motherboard_serial"],
                price=self.price,
                f_sale=self.sale
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
        bios = Bioses.objects.get_or_create(bios_text=value)[0]
        bios.save()
        return bios

    def _cpus_save_and_get(self, value):
        cpu = Cpus.objects.get_or_create(cpu_name=value)[0]
        cpu.save()
        return cpu

    def _camera_option_save_and_get(self, value):
        option = CameraOptions.objects.get_or_create(option_name=value)[0]
        option.save()
        return option

    def _diagonals_save_and_get(self, value):
        diagonal = Diagonals.objects.get_or_create(diagonal_text=value)[0]
        diagonal.save()
        return diagonal

    def _gpus_save_and_get(self, value):
        gpu = Gpus.objects.get_or_create(gpu_name=value)[0]
        gpu.save()
        return gpu

    def _hddSizes_save_and_get(self, value):
        hddSize = HddSizes.objects.get_or_create(hdd_sizes_name=value)[0]
        hddSize.save()
        return hddSize

    def _licenses_save_and_get(self, value):
        license = Licenses.objects.get_or_create(license_name=value)[0]
        license.save()
        return license

    def _manufacturers_save_and_get(self, value):
        manufacturer = Manufacturers.objects.get_or_create(manufacturer_name=value)[0]
        manufacturer.save()
        return manufacturer

    def _models_save_and_get(self, value):
        model = Models.objects.get_or_create(model_name=value)[0]
        model.save()
        return model

    def _ramSizes_save_and_get(self, value):
        ramSize = RamSizes.objects.get_or_create(ram_size_text=value)[0]
        ramSize.save()
        return ramSize


class Computer_record2():

    def __init__(self, data_dict):
        print("in Computer_record2")
        print(data_dict)
        self.message = ""
        self.success = None
        try:
            self.category = self._category_get(data_dict['Others']["Category"])
            self.type = self._type_get(data_dict['SystemInfo']["System Type"])
            self.tester = self._tester_get(data_dict['Others']["Tester"])
            self.bios = self._bios_save_and_get(data_dict['SystemInfo']["BIOS"])
            self.cpu = self._cpus_save_and_get(data_dict['Processor']['Model'])
            self.camera_option = self._camera_option_save_and_get(data_dict['Others']["Camera"])
            self.diagonal = self._diagonals_save_and_get(data_dict['Display']['Diagonal'])
            self.gpu = self._gpus_save_and_get(data_dict["GPU"]['Integrated'])
            self.hddsize = self._hddSizes_save_and_get('N/A')
            self.license = self._licenses_save_and_get(data_dict['Others']["License"])
            self.manufacturer = self._manufacturers_save_and_get(data_dict['SystemInfo']["Manufacturer"])
            self.model = self._models_save_and_get(data_dict['SystemInfo']['Model'])
            self.motherboard = data_dict['SystemInfo']["MB Serial"]
            self.ramsize = self._ramSizes_save_and_get(data_dict['RAM']['RAM Capacity'])
            # self.is_sold = data_dict['Others']['isSold']
            self.is_sold = False
            self.timenow = timezone.now()
            self.computer = self._computer_save_and_get(data_dict)
            for id in range(self._get_highest_first_number(data_dict["Batteries"])):
                battery = Batteries.objects.get_or_create(
                    serial=data_dict["Batteries"][str(id+1) + ' Battery Serial'],
                    wear_out=data_dict["Batteries"][str(id + 1) + ' Battery Wear Level'],
                    expected_time=data_dict["Batteries"][str(id + 1) + ' Battery Estimated'],
                    model=data_dict["Batteries"][str(id + 1) + ' Battery Model'],
                    current_wh=data_dict["Batteries"][str(id + 1) + ' Battery Current Wh'],
                    maximum_wh=data_dict["Batteries"][str(id + 1) + ' Battery Maximum Wh'],
                    factory_wh=data_dict["Batteries"][str(id + 1) + ' Battery Factory Wh']
                )[0]
                self._bat_to_comp_relation_creation(battery)
            for id in range(self._get_highest_first_number(data_dict["RAM"])):
                ram = Rams.objects.get_or_create(
                    ram_serial=data_dict["RAM"][str(id + 1) + ' Stick SN'],
                    capacity=data_dict["RAM"][str(id + 1) + ' Stick Cap'],
                    clock=data_dict["RAM"][str(id + 1) + ' Stick Clock'],
                    type=data_dict["RAM"]['RAM Type']
                )[0]
                self._ram_to_comp_relation_creation(ram)
            self.message += "Success"
            self.success = True
        except decimal.InvalidOperation as e:
            self.message += "Failure decimal\nPossible reason:\n"
            self.message += str(e)
            self.success = False
        except Exception as e:
            self.message += "Failure exception\nPossible reason:\n"
            self.message += str(e)
            self.success = False

    def _computer_save_and_get(self, data):
        try:
            existing_computer = Computers.objects.get(computer_serial=data['SystemInfo']['Serial Number'])
            computer = Computers(
                id_computer=existing_computer.id_computer,
                computer_serial=data['SystemInfo']['Serial Number'],
                f_type=self.type,
                f_category=self.category,
                f_manufacturer=self.manufacturer,
                f_model=self.model,
                f_cpu=self.cpu,
                f_gpu=self.gpu,
                f_ram_size=self.ramsize,
                # f_hdd_size=self.hddsize,
                f_diagonal=self.diagonal,
                f_license=self.license,
                f_camera=self.camera_option,
                cover='N/A',
                display='N/A',
                bezel='N/A',
                keyboard='N/A',
                mouse='N/A',
                sound='N/A',
                cdrom='N/A',
                hdd_cover='N/A',
                ram_cover='N/A',
                other=data["Others"]["Other"],
                f_tester=self.tester,
                date=self.timenow,
                f_bios=self.bios,
                motherboard_serial=self.motherboard,
                # price=self.price
            )
            computer.save()
            self.message += "Existing record has been updated\n"
            return computer
        except Computers.DoesNotExist:
            print("No computer with such serial, inserting a new record")
            computer = Computers(
                computer_serial=data['SystemInfo']['Serial Number'],
                f_type=self.type,
                f_category=self.category,
                f_manufacturer=self.manufacturer,
                f_model=self.model,
                f_cpu=self.cpu,
                f_gpu=self.gpu,
                f_ram_size=self.ramsize,
                # f_hdd_size=self.hddsize,
                f_diagonal=self.diagonal,
                f_license=self.license,
                f_camera=self.camera_option,
                cover='N/A',
                display='N/A',
                bezel='N/A',
                keyboard='N/A',
                mouse='N/A',
                sound='N/A',
                cdrom='N/A',
                hdd_cover='N/A',
                ram_cover='N/A',
                other=data["Others"]["Other"],
                f_tester=self.tester,
                date=self.timenow,
                f_bios=self.bios,
                motherboard_serial=self.motherboard,
                # price=self.price
            )
            computer.save()
            self.message += "New record has been added\n"
            return computer

    def _bat_to_comp_relation_creation(self, bat):
        bat_to_comp, created = BatToComp.objects.get_or_create(
            f_id_computer_bat_to_com=self.computer,
            f_bat_bat_to_com=bat
        )

    def _ram_to_comp_relation_creation(self, ram):
        ram_to_comp = RamToComp.objects.get_or_create(
            f_id_computer_ram_to_com=self.computer,
            f_id_ram_ram_to_com=ram
        )

    def _get_number_out_of_string(self, string):
        variable = string.split()[0]
        if variable.isdigit():
            return int(variable)
        return 0

    def _get_highest_first_number(self, object):
        highest = 1
        for key in object.keys():
            testing_number = self._get_number_out_of_string(key)
            if testing_number > highest:
                highest = testing_number
        return highest


    def _category_get(self, value):
        return Categories.objects.get(category_name=value)

    def _type_get(self, value):
        return Types.objects.get(type_name=value)

    def _tester_get(self, value):
        return Testers.objects.get(tester_name=value)

    def _bios_save_and_get(self, value):
        bios = Bioses.objects.get_or_create(bios_text=value)[0]
        return bios

    def _cpus_save_and_get(self, value):
        cpu = Cpus.objects.get_or_create(cpu_name=value)[0]
        return cpu

    def _camera_option_save_and_get(self, value):
        option = CameraOptions.objects.get_or_create(option_name=value)[0]
        return option

    def _diagonals_save_and_get(self, value):
        diagonal = Diagonals.objects.get_or_create(diagonal_text=value)[0]
        return diagonal

    def _gpus_save_and_get(self, value):
        gpu = Gpus.objects.get_or_create(gpu_name=value)[0]
        return gpu

    def _hddSizes_save_and_get(self, value):
        hddSize = HddSizes.objects.get_or_create(hdd_sizes_name=value)[0]
        return hddSize

    def _licenses_save_and_get(self, value):
        license = Licenses.objects.get_or_create(license_name=value)[0]
        return license

    def _manufacturers_save_and_get(self, value):
        manufacturer = Manufacturers.objects.get_or_create(manufacturer_name=value)[0]
        return manufacturer

    def _models_save_and_get(self, value):
        model = Models.objects.get_or_create(model_name=value)[0]
        return model

    def _ramSizes_save_and_get(self, value):
        ramSize = RamSizes.objects.get_or_create(ram_size_text=value)[0]
        return ramSize
