from ULCDTinterface.modelers import * # Computers, Bioses, Batteries, Cpus, CameraOptions, Categories, Computers, Clients, Sales, Diagonals, Gpus, HddSizes, Hdds, Licenses, Manufacturers, Models, RamSizes, Rams, Testers, Types, BatToComp, RamToComp, HddToComp
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
            # self.motherboard_serial = data_dict["motherboard_serial"]
            self.ramsize = self._ramSizes_save_and_get(data_dict["RAM"])
            self.is_sold = data_dict["IsSold"]
            print("IsSold: " + str(self.is_sold))
            self.price = self._price_get(data_dict["Price"])
            self.timenow = timezone.now()
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
        hdd = HddSerials.objects.get_or_create(hdd_serial=value)[0]
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
                motherboard_serial=data["motherboard_serial"]
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
                motherboard_serial=data["motherboard_serial"]
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


class ComputerRecord2:
    '''
    Modified version of Computer_record to be compatible with 5th version of build.
    '''

    def __init__(self, data_dict):
        print("in Computer_record2")
        print(data_dict)
        self.message = ""
        self.success = None
        try:
            self._one_to_many_connection_save(data_dict)
            print("_one_to_many_connection_save(data_dict)")
            self.computer = self._computer_save_and_get(data_dict)
            print("self._computer_save_and_get(data_dict)")
            self._many_to_many_connection_save(data_dict)
            print("_many_to_many_connection_save(data_dict)")
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
        print('_computer_save_and_get')
        try:
            existing_computer = Computers.objects.get(computer_serial=data['SystemInfo']['Serial Number'])
            print('after existing computer')
            existing_computer.id_computer = existing_computer.id_computer
            existing_computer.computer_serial = data['SystemInfo']['Serial Number']
            existing_computer.f_type = self.type
            existing_computer.f_category = self.category
            existing_computer.f_manufacturer = self.manufacturer
            existing_computer.f_model = self.model
            existing_computer.f_cpu = self.cpu
            existing_computer.f_gpu = self.gpu
            existing_computer.f_ram_size = self.ramsize
            existing_computer.f_diagonal = self.diagonal
            existing_computer.f_license = self.license
            existing_computer.f_camera = self.camera_option
            existing_computer.cover = 'N/A'
            existing_computer.display = 'N/A'
            existing_computer.bezel = 'N/A'
            existing_computer.keyboard = 'N/A'
            existing_computer.mouse = 'N/A'
            existing_computer.sound = 'N/A'
            existing_computer.cdrom = 'N/A'
            existing_computer.hdd_cover = 'N/A'
            existing_computer.ram_cover = 'N/A'
            existing_computer.other = data["Others"]["Other"]
            existing_computer.f_tester = self.tester
            existing_computer.date = self.timenow
            existing_computer.f_bios = self.bios
            existing_computer.motherboard_serial = self.motherboard_serial
            existing_computer.f_id_matrix = self.matrix
            existing_computer.f_id_computer_resolutions = self.computer_resolution
            if "Received batch" in data["Others"] and existing_computer.f_id_received_batches is None:
                existing_computer.f_id_received_batches = Receivedbatches.objects.get(received_batch_name=data["Others"]["Received batch"])
            if existing_computer.f_id_comp_ord:
                if "Order" in data and "Status" in data["Order"]:
                    print('___start___')
                    comp_ord = existing_computer.f_id_comp_ord
                    print('___end___')
                    if data["Order"]["Status"] == "In-Preperation":
                        comp_ord.is_ready = 0
                    elif data["Order"]["Status"] == "Ready":
                        comp_ord.is_ready = 1
                    comp_ord.save()
            existing_computer.save()
            self.message += "Existing record has been updated\n"
            return existing_computer
        except Computers.DoesNotExist:
            print("No computer with such serial, inserting a new record")
            received_batch = None
            if "Received batch" in data["Others"]:
                received_batch = Receivedbatches.objects.get(received_batch_name=data["Others"]["Received batch"])
            computer = Computers(
                computer_serial=data['SystemInfo']['Serial Number'],
                f_type=self.type,
                f_category=self.category,
                f_manufacturer=self.manufacturer,
                f_model=self.model,
                f_cpu=self.cpu,
                f_gpu=self.gpu,
                f_ram_size=self.ramsize,
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
                motherboard_serial=self.motherboard_serial,
                f_id_matrix=self.matrix,
                f_id_computer_resolutions=self.computer_resolution,
                f_id_received_batches=received_batch
            )
            computer.save()
            self.message += "New record has been added\n"
            return computer

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

    def _many_to_many_connection_save(self, data_dict):
        def _save_batteries(battery_dict):
            print(battery_dict)
            BatToComp.objects.filter(f_id_computer_bat_to_com=self.computer).delete()
            if battery_dict:
                for id in range(self._get_highest_first_number(battery_dict)):
                    battery = Batteries.objects.get_or_create(
                        serial=battery_dict[str(id + 1) + ' Battery SN'],
                        wear_out=battery_dict[str(id + 1) + ' Battery Wear Level'],
                        expected_time=battery_dict[str(id + 1) + ' Battery Estimated'],
                        model=battery_dict[str(id + 1) + ' Battery Model'],
                        maximum_wh=battery_dict[str(id + 1) + ' Battery Maximum Wh'],
                        factory_wh=battery_dict[str(id + 1) + ' Battery Factory Wh']
                    )[0]
                    BatToComp.objects.get_or_create(
                        f_id_computer_bat_to_com=self.computer,
                        f_bat_bat_to_com=battery
                    )

        def _save_rams(ram_dict):
            print(ram_dict)
            RamToComp.objects.filter(f_id_computer_ram_to_com=self.computer).delete()
            for id in range(self._get_highest_first_number(ram_dict)):
                if str(id + 1) + ' Stick SN' in ram_dict:
                    ram = Rams.objects.get_or_create(
                        ram_serial=ram_dict[str(id + 1) + ' Stick SN'],
                        capacity=ram_dict[str(id + 1) + ' Stick Cap'],
                        clock=ram_dict[str(id + 1) + ' Stick Clock'],
                        type=ram_dict['RAM Type']
                    )[0]
                    RamToComp.objects.get_or_create(
                        f_id_computer_ram_to_com=self.computer,
                        f_id_ram_ram_to_com=ram
                    )

        def _save_gpus(gpu_dict):
            print(gpu_dict)
            Computergpus.objects.filter(f_id_computer=self.computer).delete()
            for id in range(self._get_highest_first_number(gpu_dict)):
                if str(id + 1) + ' Manufacturer' in gpu_dict:
                    manufacturer = Manufacturers.objects.get_or_create(
                        manufacturer_name=gpu_dict[str(id + 1) + ' Manufacturer']
                    )[0]
                    gpu = Gpus.objects.get_or_create(
                        gpu_name=gpu_dict[str(id + 1) + ' Model'],
                        f_id_manufacturer=manufacturer
                    )[0]
                    Computergpus.objects.get_or_create(
                        f_id_gpu=gpu,
                        f_id_computer=self.computer
                    )

        def _save_processors(processor_dict):
            print(processor_dict)
            Computerprocessors.objects.filter(f_id_computer=self.computer).delete()
            for id in range(self._get_highest_first_number(processor_dict)):
                if str(id + 1) + ' Manufacturer' in processor_dict:
                    manufacturer = Manufacturers.objects.get_or_create(
                        manufacturer_name=processor_dict[str(id + 1) + ' Manufacturer']
                    )[0]
                    processor = Processors.objects.get_or_create(
                        f_manufacturer=manufacturer,
                        model_name=processor_dict[str(id + 1) + ' Model'],
                        stock_clock=processor_dict[str(id + 1) + ' Stock Clock'],
                        max_clock=processor_dict[str(id + 1) + ' MAX Clock'],
                        cores=int(processor_dict[str(id + 1) + ' Cores Amount']),
                        threads=int(processor_dict[str(id + 1) + ' Thread Amount'])
                    )[0]
                    Computerprocessors.objects.get_or_create(
                        f_id_computer=self.computer,
                        f_id_processor=processor
                    )

        def _save_drives(drives_dict):
            print(drives_dict)
            Computerdrives.objects.filter(f_id_computer=self.computer).delete()
            if drives_dict:
                for id in range(self._get_highest_first_number(drives_dict)):
                    if str(id + 1) + ' Drive SN' in drives_dict:
                        model = HddModels.objects.get_or_create(hdd_models_name=drives_dict[str(id + 1) + ' Drive SN'])[0]
                        size = HddSizes.objects.get_or_create(hdd_sizes_name=drives_dict[str(id + 1) + ' Drive Capacity'])[0]
                        lock_state = LockState.objects.get_or_create(lock_state_name=drives_dict[str(id + 1) + ' Drive Locked'])[0]
                        speed = Speed.objects.get_or_create(speed_name=drives_dict[str(id + 1) + ' Drive Speed'])[0]
                        form_factor = FormFactor.objects.get_or_create(form_factor_name=drives_dict[str(id + 1) + ' Drive Size'])[0]
                        drive = Drives.objects.get_or_create(
                            hdd_serial=drives_dict[str(id + 1) + ' Drive SN'],
                            health=drives_dict[str(id + 1) + ' Drive Health'].replace("%", ""),
                            days_on=drives_dict[str(id + 1) + ' Drive PowerOn'],
                            f_hdd_models=model,
                            f_hdd_sizes=size,
                            f_lock_state=lock_state,
                            f_speed=speed,
                            f_form_factor=form_factor
                        )[0]
                        print('drive saved')
                        Computerdrives.objects.get_or_create(
                            f_id_computer=self.computer,
                            f_drive=drive
                        )
                        print('computerdrive saved')

        def _save_observations(observation_dict):
            print(observation_dict)
            Computerobservations.objects.filter(f_id_computer=self.computer).delete()
            for key, lst in observation_dict.items():
                for value in lst:
                    print(value)
                    observation = Observations.objects.get(shortcode=value)
                    Computerobservations.objects.create(
                        f_id_computer=self.computer,
                        f_id_observation=observation
                    )

        print("Start of many to many")
        _save_batteries(data_dict["Batteries"])
        _save_rams(data_dict["RAM"])
        _save_gpus(data_dict["GPU"])
        _save_processors(data_dict["Processor"])
        _save_drives(data_dict["Drives"])
        _save_observations(data_dict['Observations'])
        print("End of many to many")

    def _one_to_many_connection_save(self, data_dict):
        print("start of _one_to_many_connection_save")
        print("before self.category")
        self.category = Categories.objects.get(category_name=data_dict['Others']["Category"])
        print("before self.type ")
        self.type = Types.objects.get(type_name=data_dict['SystemInfo']["System Type"])
        print("before self.tester")
        self.tester = Testers.objects.get(tester_name=data_dict['Others']["Tester"])
        print("before self.bios")
        self.bios = Bioses.objects.get_or_create(bios_text=data_dict['SystemInfo']["BIOS"])[0]
        print("before self.cpu")
        self.cpu = Cpus.objects.get_or_create(cpu_name=data_dict['Processor']['1 Model'])[0]
        print("before self.camera_option")
        self.camera_option = CameraOptions.objects.get_or_create(option_name=data_dict['Others']["Camera"])[0]
        print("before self.diagonal")
        self.diagonal = Diagonals.objects.get_or_create(diagonal_text=data_dict['Display']['Diagonal'])[0]
        print("before self.gpu")
        self.gpu = Gpus.objects.get_or_create(gpu_name='N/A')[0]
        print("before self.hddsize")
        self.hddsize = HddSizes.objects.get_or_create(hdd_sizes_name='N/A')
        print("before self.license")
        self.license = Licenses.objects.get_or_create(license_name=data_dict['Others']["License"])[0]
        print("before self.manufacturer")
        self.manufacturer = Manufacturers.objects.get_or_create(
            manufacturer_name=data_dict['SystemInfo']["Manufacturer"]
        )[0]
        print("before self.model")
        self.model = Models.objects.get_or_create(model_name=data_dict['SystemInfo']['Model'])[0]
        print("before self.motherboard_serial")
        self.motherboard_serial = data_dict['SystemInfo']["MB Serial"]
        print("before self.ramsize")
        self.ramsize = RamSizes.objects.get_or_create(ram_size_text=data_dict['RAM']['RAM Capacity'])[0]
        print("before self.timenow")
        self.timenow = timezone.now()

        resolution = Resolutions.objects.get_or_create(resolution_text=data_dict["Display"]["Resolution"])[0]
        resolutionCategory = Resolutioncategories.objects.get_or_create(resolution_category_name=data_dict["Display"]["Category"])[0]
        self.computer_resolution = Computerresolutions.objects.get_or_create(
            f_id_resolution=resolution,
            f_id_resolution_category=resolutionCategory
        )[0]

        cable_type = Cabletypes.objects.get_or_create(cable_type_name=data_dict["Display"]["Cable Type"])[0]
        self.matrix = Matrixes.objects.get_or_create(f_id_cable_type=cable_type)[0]
        print("end of _one_to_many_connection_save")


class Computer_data_dict_builder:
    '''
    Moved logic out of view to the dedicated class.
    This class represents data which is sent back to client program of an existing computer record in the database which are not generated.
    '''

    def __init__(self, serial):
        self.data_dict = {}
        computer = Computers.objects.get(computer_serial=serial)
        self._form_others_dict(computer)
        self._form_observations_dict(computer)
        self._form_order_dict(computer)

    def _form_order_dict(self, computer):
        order_dict = dict()
        if computer.f_id_comp_ord:
            order_id = computer.f_id_comp_ord.f_order_id_to_order.id_order
            ordtesses = OrdTes.objects.filter(f_order=order_id)
            testers = []
            for ordtes in ordtesses:
                testers.append(ordtes.f_id_tester.tester_name)
            order_dict['Testers'] = testers
            order_dict['Order name'] = computer.f_id_comp_ord.f_order_id_to_order.order_name
            order_dict['Current status'] = "In-Preperation" if computer.f_id_comp_ord.is_ready == 0 else "Ready"
            order_dict['Statusses'] = ["In-Preperation", "Ready"]
            order_dict['Client'] = computer.f_id_comp_ord.f_order_id_to_order.f_id_client.client_name
            self.data_dict["Order"] = order_dict

    def _form_observations_dict(self, computer):
        observation_dict = dict()
        compobservs = Computerobservations.objects.filter(f_id_computer=computer)
        for compobserv in compobservs:
            if not compobserv.f_id_observation.f_id_observation_category.category_name in observation_dict:
                observation_dict[compobserv.f_id_observation.f_id_observation_category.category_name] = []
            observation_dict[compobserv.f_id_observation.f_id_observation_category.category_name].\
                append(compobserv.f_id_observation.shortcode)
        self.data_dict['Observations']=observation_dict

    def _form_others_dict(self, computer):
        def get_is_sold(computer):
            if computer.f_sale is None:
                return False
            return True

        def get_camera(computer):
            if computer.f_camera.option_name:
                return computer.f_camera.option_name
            else:
                return ''

        others_dict = dict()
        # others_dict["Camera"] = get_camera(computer)
        others_dict["License"] = computer.f_license.license_name
        others_dict["Previuos tester"] = computer.f_tester.tester_name
        others_dict["Category"] = computer.f_category.category_name
        others_dict["isSold"] = get_is_sold(computer)
        others_dict["Other"] = computer.other
        if computer.f_id_received_batches:
            others_dict["Received batch"] = computer.f_id_received_batches.received_batch_name
        self.data_dict["Others"] = others_dict

