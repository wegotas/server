from ULCDTinterface.modelers import *
import datetime, decimal
from django.utils import timezone


class ComputerRecord:
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
            self.computer = self._computer_save_and_get(data_dict)
            self._many_to_many_connection_save(data_dict)
            self.message += "Success"
            self.success = True
        except decimal.InvalidOperation as e:
            self.message += "Failure decimal\nPossible reason:\n"
            self.message += str(e)
            self.success = False
        except Exception as e:
            self.message += "Failure exception\nPossible reason:\n"
            self.message += str(e)
            print(str(e))
            self.success = False

    def _computer_save_and_get(self, data):
        try:
            existing_computer = Computers.objects.get(computer_serial=data['System Info']['Serial Number'])
            existing_computer.id_computer = existing_computer.id_computer

            existing_computer.f_type = self.type
            existing_computer.f_category = self.category
            existing_computer.f_manufacturer = self.manufacturer
            existing_computer.f_model = self.model
            existing_computer.f_ram_size = self.ramsize
            existing_computer.f_diagonal = self.diagonal
            existing_computer.f_license = self.license
            existing_computer.f_camera = self.camera_option

            existing_computer.other = data["Observations"]["Add. comment"]
            existing_computer.f_tester = self.tester
            existing_computer.date = self.timenow
            existing_computer.f_bios = self.bios
            existing_computer.motherboard_serial = self.motherboard_serial
            existing_computer.f_id_matrix = self.matrix
            existing_computer.f_id_computer_resolutions = self.computer_resolution
            existing_computer.box_number = data['Others']['Box number']
            if "Received batch" in data["Log Information"] and existing_computer.f_id_received_batches is None:
                existing_computer.f_id_received_batches = Receivedbatches.objects.get(received_batch_name=data["Log Information"]["Received batch"])
            existing_computer.f_id_computer_form_factor = self.computer_form_factor
            if existing_computer.f_id_comp_ord:
                if "Order" in data and "Status" in data["Order"]:
                    comp_ord = existing_computer.f_id_comp_ord
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
            if "Received batch" in data["Log Information"]:
                received_batch = Receivedbatches.objects.get(received_batch_name=data["Log Information"]["Received batch"])
            computer = Computers.objects.create(
                computer_serial=data['System Info']['Serial Number'],
                f_type=self.type,
                f_category=self.category,
                f_manufacturer=self.manufacturer,
                f_model=self.model,
                f_ram_size=self.ramsize,
                f_diagonal=self.diagonal,
                f_license=self.license,
                f_camera=self.camera_option,
                other=data["Observations"]["Add. comment"],
                f_tester=self.tester,
                date=self.timenow,
                f_bios=self.bios,
                motherboard_serial=self.motherboard_serial,
                f_id_matrix=self.matrix,
                f_id_computer_resolutions=self.computer_resolution,
                f_id_received_batches=received_batch,
                box_number=data['Others']['Box number'],
                f_id_computer_form_factor=self.computer_form_factor
            )
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
            for id in range(0, self._get_highest_first_number(battery_dict) + 1):
                if str(id) + ' Battery' in battery_dict:
                    battery = Batteries.objects.get_or_create(
                        serial=battery_dict[str(id) + ' Battery']['Serial'],
                        wear_out=battery_dict[str(id) + ' Battery']['Wear Level'],
                        expected_time=battery_dict[str(id) + ' Battery']['Estimated'],
                        model=battery_dict[str(id) + ' Battery']['Model'],
                        maximum_wh=battery_dict[str(id) + ' Battery']['Maximum Wh'],
                        factory_wh=battery_dict[str(id) + ' Battery']['Factory Wh']
                    )[0]
                    BatToComp.objects.get_or_create(
                        f_id_computer_bat_to_com=self.computer,
                        f_bat_bat_to_com=battery
                    )

        def _save_rams(ram_dict):
            print(ram_dict)
            RamToComp.objects.filter(f_id_computer_ram_to_com=self.computer).delete()
            for id in range(0, self._get_highest_first_number(ram_dict) + 1):
                if str(id) + ' Stick' in ram_dict:
                    if ram_dict[str(id) + ' Stick']:
                        ram = Rams.objects.get_or_create(
                            ram_serial=ram_dict[str(id) + ' Stick']['Serial'],
                            capacity=ram_dict[str(id) + ' Stick']['Capacity'],
                            clock=ram_dict[str(id) + ' Stick']['Clock'],
                            type=ram_dict['Type']
                        )[0]
                        RamToComp.objects.get_or_create(
                            f_id_computer_ram_to_com=self.computer,
                            f_id_ram_ram_to_com=ram
                        )

        def _save_gpus(gpu_dict):
            print(gpu_dict)
            Computergpus.objects.filter(f_id_computer=self.computer).delete()
            for id in range(0, self._get_highest_first_number(gpu_dict) + 1):
                if str(id) + ' Device' in gpu_dict:
                    if gpu_dict[str(id) + ' Device']:
                        if gpu_dict[str(id) + ' Device']:
                            manufacturer = Manufacturers.objects.get_or_create(
                                manufacturer_name=gpu_dict[str(id) + ' Device']['Manufacturer']
                            )[0]
                            gpu = Gpus.objects.get_or_create(
                                gpu_name=gpu_dict[str(id) + ' Device']['Model'],
                                f_id_manufacturer=manufacturer
                            )[0]
                            Computergpus.objects.get_or_create(
                                f_id_gpu=gpu,
                                f_id_computer=self.computer
                            )

        def _save_processors(processor_dict):
            print(processor_dict)
            Computerprocessors.objects.filter(f_id_computer=self.computer).delete()
            for id in range(0, self._get_highest_first_number(processor_dict) + 1):
                if str(id) + ' Processor' in processor_dict:
                    if processor_dict[str(id) + ' Processor']:
                        manufacturer = Manufacturers.objects.get_or_create(
                            manufacturer_name=processor_dict[str(id) + ' Processor']['Manufacturer']
                        )[0]
                        processor = Processors.objects.get_or_create(
                            f_manufacturer=manufacturer,
                            model_name=processor_dict[str(id) + ' Processor']['Model'],
                            stock_clock=processor_dict[str(id) + ' Processor']['Stock Clock'],
                            max_clock=processor_dict[str(id) + ' Processor']['Maximum Clock'],
                            cores=int(processor_dict[str(id) + ' Processor']['Cores Amount']),
                            threads=int(processor_dict[str(id) + ' Processor']['Threads Amount'])
                        )[0]
                        Computerprocessors.objects.get_or_create(
                            f_id_computer=self.computer,
                            f_id_processor=processor
                        )

        def _save_drives(drives_dict):
            print(drives_dict)
            Computerdrives.objects.filter(f_id_computer=self.computer).delete()
            if drives_dict:
                for id in range(0, self._get_highest_first_number(drives_dict) + 1):
                    if str(id) + ' Drive' in drives_dict:
                        if drives_dict[str(id) + ' Drive']:
                            drive = Drives.objects.get_or_create(
                                hdd_serial=drives_dict[str(id) + ' Drive']['Serial'],
                                health=drives_dict[str(id) + ' Drive']['Health'].replace("%", ""),
                                days_on=drives_dict[str(id) + ' Drive']['Power On'],
                                f_hdd_models=HddModels.objects.get_or_create(
                                    hdd_models_name=drives_dict[str(id) + ' Drive']['Model']
                                )[0],
                                f_hdd_sizes=HddSizes.objects.get_or_create(
                                    hdd_sizes_name=drives_dict[str(id) + ' Drive']['Capacity']
                                )[0],
                                f_lock_state=LockState.objects.get_or_create(
                                    lock_state_name=drives_dict[str(id) + ' Drive']['Locked']
                                )[0],
                                f_speed=Speed.objects.get_or_create(
                                    speed_name=drives_dict[str(id) + ' Drive']['Speed']
                                )[0],
                                f_form_factor=FormFactor.objects.get_or_create(
                                    form_factor_name=drives_dict[str(id) + ' Drive']['Size']
                                )[0]
                            )[0]
                            Computerdrives.objects.get_or_create(
                                f_id_computer=self.computer,
                                f_drive=drive
                            )

        def _save_observations(observation_dict):
            print(observation_dict)
            if observation_dict:
                Computerobservations.objects.filter(f_id_computer=self.computer).delete()
                for category_string, value in observation_dict.items():
                    if isinstance(value, dict):
                        for subcategory_string, shortcode_strings in value.items():
                            observations = Observations.objects.filter(
                                f_id_observation_category__category_name=category_string,
                                f_id_observation_subcategory__subcategory_name=subcategory_string,
                                shortcode__in=shortcode_strings
                            )
                            for observation in observations:
                                Computerobservations.objects.create(
                                    f_id_computer=self.computer,
                                    f_id_observation=observation
                                )

        def try_saving(method, keyword):
            try:
                method(data_dict[keyword])
            except Exception as e:
                print(e)
                pass

        methods_to_call = [
            _save_batteries,
            _save_rams,
            _save_gpus,
            _save_processors,
            _save_drives,
            _save_observations
        ]

        dicts_keyword_to_pass = ['Batteries', 'RAM', 'GPU', 'CPU', 'Drives', 'Observations']

        print("Start of many to many")
        for method, keyword in zip(methods_to_call, dicts_keyword_to_pass):
            try_saving(method, keyword)
        print("End of many to many")

    def _one_to_many_connection_save(self, data_dict):
        self.category = Categories.objects.get(category_name=data_dict['Log Information']["Category"])
        self.type = Types.objects.get_or_create(type_name=data_dict['System Info']["Type"])[0]
        self.tester = Testers.objects.get(tester_name=data_dict['Log Information']["Tester"])
        self.bios = Bioses.objects.get_or_create(bios_text=data_dict['System Info']["BIOS"])[0]
        self.camera_option = CameraOptions.objects.get_or_create(option_name=data_dict['Hardware']["Additional"]["Camera"])[0]
        self.diagonal = Diagonals.objects.get_or_create(diagonal_text=data_dict['Display']['Diagonal'])[0]
        self.license = Licenses.objects.get_or_create(license_name=data_dict['Others']["License"])[0]
        self.manufacturer = Manufacturers.objects.get_or_create(
            manufacturer_name=data_dict['System Info']["Manufacturer"]
        )[0]
        self.model = Models.objects.get_or_create(model_name=data_dict['System Info']['Model'])[0]
        self.motherboard_serial = data_dict['System Info']["MB Serial"]
        self.ramsize = RamSizes.objects.get_or_create(ram_size_text=data_dict['RAM']['Total'])[0]
        self.computer_form_factor = None
        if "Form factor" in data_dict["System Info"] and data_dict["System Info"]["Form factor"]:
            self.computer_form_factor = ComputerFormFactors.objects.get(form_factor_name=data_dict["System Info"]["Form factor"])
        self.timenow = timezone.now()

        resolution = Resolutions.objects.get_or_create(resolution_text=data_dict["Display"]["Resolution"])[0]
        resolutionCategory = Resolutioncategories.objects.get_or_create(resolution_category_name=data_dict["Display"]["Category"])[0]
        self.computer_resolution = Computerresolutions.objects.get_or_create(
            f_id_resolution=resolution,
            f_id_resolution_category=resolutionCategory
        )[0]

        cable_type = Cabletypes.objects.get_or_create(cable_type_name=data_dict["Display"]["Cable Type"])[0]
        self.matrix = Matrixes.objects.get_or_create(f_id_cable_type=cable_type)[0]


class ComputerDataDictBuilder:
    """
    Moved logic out of view to the dedicated class.
    This class represents data which is sent back to client program of an existing computer record in the database which are not generated.
    """

    def __init__(self, serial):
        self.data_dict = {}
        computer = Computers.objects.get(computer_serial=serial)
        self._form_others_dict(computer)
        self._form_observations_dict(computer)
        self._form_order_dict(computer)
        self._form_system_info(computer)

    def _form_order_dict(self, computer):
        order_dict = dict()
        if computer.f_id_comp_ord:
            order_id = computer.f_id_comp_ord.f_order_id_to_order.id_order
            order_dict['Testers'] = list(Testers.objects.filter(
                ordtes__f_order=order_id).values_list('tester_name', flat=True))
            order_dict['Order name'] = computer.f_id_comp_ord.f_order_id_to_order.order_name
            order_dict['Current status'] = "In-Preperation" if computer.f_id_comp_ord.is_ready == 0 else "Ready"
            order_dict['Statuses'] = ["In-Preperation", "Ready"]
            order_dict['Client'] = computer.f_id_comp_ord.f_order_id_to_order.f_id_client.client_name
            self.data_dict["Order"] = order_dict

    def _form_observations_dict(self, computer):
        observation_dict = dict()
        compobservs = Computerobservations.objects.filter(f_id_computer=computer)
        for compobserv in compobservs:
            if not compobserv.f_id_observation.f_id_observation_category.category_name in observation_dict:
                observation_dict[compobserv.f_id_observation.f_id_observation_category.category_name] = {}
            observation_dict[compobserv.f_id_observation.f_id_observation_category.category_name][compobserv.f_id_observation.full_name] = compobserv.f_id_observation.shortcode
            self.data_dict['Observations'] = observation_dict

    def _form_others_dict(self, computer):
        def get_is_sold(computer):
            if computer.f_sale is None:
                return False
            return True

        others_dict = dict()
        others_dict["License"] = computer.f_license.license_name
        others_dict["Previous tester"] = computer.f_tester.tester_name
        others_dict["Category"] = computer.f_category.category_name
        others_dict["isSold"] = get_is_sold(computer)
        others_dict["Other"] = computer.other
        if computer.box_number:
            others_dict['Box number'] = computer.box_number
        if computer.f_id_received_batches:
            others_dict["Received batch"] = computer.f_id_received_batches.received_batch_name
        self.data_dict["Others"] = others_dict

    def _form_system_info(self, computer):
        system_info_dict = dict()
        if computer.f_id_computer_form_factor:
            system_info_dict['Form factor'] = computer.f_id_computer_form_factor.form_factor_name
            self.data_dict['System Info'] = system_info_dict

