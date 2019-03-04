from ULCDTinterface.modelers import *
import xlsxwriter
from django.utils import timezone
import re
from django.db.models import Q, Count
from django.conf import settings
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import logging
import os
from threading import Thread
import tarfile
import datetime
import csv
import qrcode
from PIL import Image, ImageDraw, ImageFont
import subprocess
import io
from django.db.models import ProtectedError
from django.db.utils import IntegrityError
import tempfile
import math
import sys
from abc import ABC
import magic
import xlrd


class BatHolder:
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
                bat = BatHolder(
                    index=i,
                    id=battery.id_bat_to_comp,
                    serial=battery.f_bat_bat_to_com.serial,
                    wear=battery.f_bat_bat_to_com.wear_out,
                    time=battery.f_bat_bat_to_com.expected_time
                )
                bat_list.append(bat)
        if len(bat_list) == 0:
            bat = BatHolder()
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


class Edit_computer_record:

    def __init__(self, data_dict):
        self.data_dict = data_dict
        self.data_dict.pop("edit", "")
        self.data_dict.pop("edit.x", "")
        self.data_dict.pop("edit.y", "")

        self.type = Types.objects.get_or_create(type_name=self.data_dict.pop("type_name", "")[0])[0]
        self.category = Categories.objects.get_or_create(category_name=self.data_dict.pop("category_name", "")[0])[0]
        self.tester = Testers.objects.get_or_create(tester_name=self.data_dict.pop("tester_name", "")[0])[0]
        self.bios = Bioses.objects.get_or_create(bios_text=self.data_dict.pop("bios_text", "")[0])[0]
        self.cpu = Cpus.objects.get_or_create(cpu_name=self.data_dict.pop("cpu_name", "")[0])[0]
        self.camera_option = CameraOptions.objects.get_or_create(option_name=self.data_dict.pop("option_name", "")[0])[0]
        self.diagonal = Diagonals.objects.get_or_create(diagonal_text=self.data_dict.pop("diagonal_text", "")[0])[0]
        self.gpu = Gpus.objects.get_or_create(gpu_name=self.data_dict.pop("gpu_name", "")[0])[0]
        self.hddsize = HddSizes.objects.get_or_create(hdd_sizes_name=self.data_dict.pop("hdd_sizes_name", "")[0])[0]
        self.license = Licenses.objects.get_or_create(license_name=self.data_dict.pop("license_name", "")[0])[0]
        self.manufacturer = Manufacturers.objects.get_or_create(manufacturer_name=self.data_dict.pop("manufacturer_name", "")[0])[0]
        self.model = Models.objects.get_or_create(model_name=self.data_dict.pop("model_name", "")[0])[0]
        self.motherboard_serial = self.data_dict.pop("motherboard_serial", "")[0]
        self.ramsize = RamSizes.objects.get_or_create(ram_size_text=self.data_dict.pop("ram_size_text", "")[0])[0]
        self.computer = Computers.objects.get(id_computer=self.data_dict.pop("id_computer", "")[0])
        if "client_name" in data_dict:
            self.client = Clients.objects.get_or_create(client_name=self.data_dict.pop("client_name", "")[0])[0]
            self.sale = Sales.objects.get_or_create(
                date_of_sale=self.data_dict.pop("date_of_sale", "")[0],
                f_id_client=self.client
            )[0]
            self._computer_sold_save()
            self._process_ram_and_hdd_serials()
            self._process_batteries()
        else:
            self._computer_save()

    def _process_batteries(self):
        bat_to_comps = BatToComp.objects.filter(f_id_computer_bat_to_com=self.computer.id_computer)
        bat_to_comps.delete()
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
            new_battocomp = BatToComp(
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
                hdd = Drives.objects.get_or_create(hdd_serial=value)[0]
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
        # self.computer.id_computer = self.data_dict.pop("id_computer", "")[0]
        self.computer.computer_serial = self.data_dict.pop("serial", "")[0]
        self.computer.f_type = self.type
        self.computer.f_category = self.category
        self.computer.f_manufacturer = self.manufacturer
        self.computer.f_model = self.model
        self.computer.f_cpu = self.cpu
        self.computer.f_gpu = self.gpu
        self.computer.f_ram_size = self.ramsize
        self.computer.f_hdd_size = self.hddsize
        self.computer.f_diagonal = self.diagonal
        self.computer.f_license = self.license
        self.computer.f_camera = self.camera_option
        self.computer.cover = self.data_dict.pop("cover", "")[0]
        self.computer.display = self.data_dict.pop("display", "")[0]
        self.computer.bezel = self.data_dict.pop("bezel", "")[0]
        self.computer.keyboard = self.data_dict.pop("keyboard", "")[0]
        self.computer.mouse = self.data_dict.pop("mouse", "")[0]
        self.computer.sound = self.data_dict.pop("sound", "")[0]
        self.computer.cdrom = self.data_dict.pop("cdrom", "")[0]
        self.computer.hdd_cover = self.data_dict.pop("hdd_cover", "")[0]
        self.computer.ram_cover = self.data_dict.pop("ram_cover", "")[0]
        self.computer.other = self.data_dict.pop("other", "")[0]
        self.computer.f_tester = self.tester
        self.computer.date = self.data_dict.pop("date", "")[0]
        self.computer.f_bios = self.bios
        self.computer.motherboard_serial = self.motherboard_serial
        self.computer.save()
        print('_computer_save')

    def _computer_sold_save(self):
        print(self.data_dict)
        self.computer = Computers(
            id_computer=self.computer.id_computer,
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
            motherboard_serial=self.motherboard_serial
        )
        self.computer.save()


'''
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
'''


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


'''
class AutoFilters:

    def __init__(self):
        print("Modified Autofilters")
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
        # self.serials = [a['computer_serial'] for a in serials]
        self.serials =serials.values_list('computer_serial', flat=True)

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
'''


class AutoFiltersFromComputers:
    """
    This is a holder of unique values necessary for filtering operations website side.
    """

    def __init__(self, computers):
        self.serials = computers.values_list('computer_serial', flat=True).distinct().order_by('computer_serial')
        self.manufacturers = computers.values_list('f_manufacturer__manufacturer_name', flat=True).distinct() \
            .order_by('f_manufacturer__manufacturer_name')
        self.models = computers.values_list('f_model__model_name', flat=True).distinct() \
            .order_by('f_model__model_name')
        self.cpus = computers.values_list('f_cpu__cpu_name', flat=True).distinct().order_by('f_cpu__cpu_name')
        self.rams = computers.values_list('f_ram_size__ram_size_text', flat=True).distinct() \
            .order_by('f_ram_size__ram_size_text')
        self.gpus = computers.values_list('f_gpu__gpu_name', flat=True).distinct().order_by('f_gpu__gpu_name')
        self.screens = computers.values_list('f_diagonal__diagonal_text', flat=True).distinct() \
            .order_by('f_diagonal__diagonal_text')
        self.others = computers.values_list('other', flat=True).distinct().order_by('other')
        self.testers = computers.values_list('f_tester__tester_name', flat=True).distinct().order_by('f_tester__tester_name')


class AutoFiltersFromSoldComputers(AutoFiltersFromComputers):
    """
    This is a holder's extension of AutoFiltersFromComputers to accommodate for sold computers additional choices.
    """

    def __init__(self, computers):
        self.prices = computers.values_list("price", flat=True).distinct().order_by('price')
        self.dates = computers.values_list("f_sale__date_of_sale", flat=True).distinct() \
            .order_by('f_sale__date_of_sale')
        self.clients = computers.values_list("f_sale__f_id_client__client_name", flat=True).distinct() \
            .order_by('f_sale__f_id_client__client_name')
        super(AutoFiltersFromSoldComputers, self).__init__(computers)


class TypCat:
    """
    Represents types with categories in sumbenu for website's navigational menu generation.
    """

    def __init__(self):
        self.current = 0
        queryset = Computers.objects.filter(f_sale__isnull=True, f_id_comp_ord__isnull=True).values(
            'f_type__type_name', 'f_category__category_name').annotate(qty=Count('id_computer'))
        self.types = []
        for record in queryset:
            inserted = False
            for type in self.types:
                if record['f_type__type_name'] == type.type_name:
                    type.add(record['f_category__category_name'], record['qty'])
                    inserted = True
            if not inserted:
                typholder = TypHolder(record['f_type__type_name'])
                typholder.add(record['f_category__category_name'], record['qty'])
                self.types.append(typholder)
        self.types.sort(key=lambda x: x.type_name)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= len(self.types):
            self.current = 0
            raise StopIteration
        else:
            self.current += 1
            return self.types[self.current - 1]


class TypHolder:
    
    def __init__(self, type_name):
        self.current = 0
        self.type_name = type_name
        self.cat_list = []

    def add(self, category_name, qty):
        self.cat_list.append(CatHolder(category_name, qty))

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= len(self.cat_list):
            self.current = 0
            raise StopIteration
        else:
            self.current += 1
            return self.cat_list[self.current - 1]
        

class CatHolder:

    def __init__(self, category_name, qty):
        self.category_name = category_name
        self.qty = qty

    def __str__(self):
        return "category_name: {0}, qty: {1}".format(self.category_name, self.qty)

    def title(self):
        return "{0} ({1})".format(self.category_name, self.qty)


def is_get_key_true(request, key):
    if request.GET.get(key) is None:
        return False
    else:
        if request.GET.get(key) == "True":
            return True
        else:
            return False


def get_qty(data_dict):
    if data_dict.get('qty') is None:
        return 10
    else:
        return int(data_dict.pop('qty')[0])


def get_page(data_dict):
    if data_dict.get('page') is None:
        return 1
    else:
        return int(data_dict.pop('page')[0])


def get_keyword(data_dict):
    if data_dict.get('keyword') is None or data_dict.get('keyword') == "":
        return None
    else:
        return data_dict.pop('keyword')[0]


def change_category_for_computers(dict):
    category_name = next(iter(dict))
    indexes = dict[category_name]
    category = Categories.objects.get(category_name=category_name)
    for ind in indexes:
        computer = Computers.objects.get(id_computer=ind)
        computer.f_category = category
        computer.save()


class AbstractDataFileGenerator(ABC):

    # Parts of comments which should be removed out of comment, preserving the rest of the comment.
    unwantedCommentParts = (
        '\t',
        '\n',
        'oko',
        'ook',
        'oik',
        'ok',
        '-',
        'Ok,',
        'Ok',
        'ok,',
        '+',
        '0k',
        'n,',
        'other',
        'N/A'
    )

    # Comments consisting out only these strings should not be returned back at all.
    unwantedComments = (None, 'o', 'n', 'k', 'NULL', 'None', 'ko')

    def _get_processed_string(self, string):
        """
        :param string: Comment or any remark in regards to a computer's quality.
        :return: Returns empty strings if is member of unwantedComments,
        else removes unwantedCommentParts from string for output.
        """
        if string in self.unwantedComments:
            return ''
        for commentPart in self.unwantedCommentParts:
            string = string.replace(commentPart, '')
        return string.strip(' ,;').replace('\r', ' ')

    def _form_comment_part(self, field, title=None):
        """
        :param field: Comment's or remark's string
        :param title: Title of remark
        :return: Returns only value if title is none,
        returns empty string if _get_processed_string returns empty value,
        any other way returns pair of title and value ex:("cover: patrintas")
        """
        value = self._get_processed_string(field)
        if title is None:
            return value
        if value == '':
            return ''
        return ', '+title+': '+value

    def _form_comment(self, computer):
        if computer.is5th_version():
            return self._form_5th_comment(computer)
        return self._form_4th_comment(computer)

    def _form_4th_comment(self, computer):
        """
        This method is responsible of forming csv/excel file
        computer's other column value of 4th version computer structure.

        :param computer: computer model's object.
        :return: fully formed comment string about a computer.
        """
        comment_to_return = self._get_processed_string(computer.other)
        comment_to_return += self._form_comment_part(computer.cover, 'cover')
        comment_to_return += self._form_comment_part(computer.display, 'display')
        comment_to_return += self._form_comment_part(computer.bezel, 'bezel')
        comment_to_return += self._form_comment_part(computer.keyboard, 'keyboard')
        comment_to_return += self._form_comment_part(computer.mouse, 'mouse')
        comment_to_return += self._form_comment_part(computer.sound, 'sound')
        comment_to_return += self._form_comment_part(computer.cdrom, 'cdrom')
        comment_to_return += self._form_comment_part(computer.hdd_cover, 'hdd_cover')
        comment_to_return += self._form_comment_part(computer.ram_cover, 'ram_cover')
        return comment_to_return.strip(' ,;')

    def _form_5th_comment(self, computer):
        """
        This method is responsible of forming csv/excel file
        computer's other column value of 5th version computer structure.

        :param computer: computer model's object.
        :return:  fully formed comment string about a computer.
        """
        commentToReturn = ''
        computer_observations = Computerobservations.objects.filter(f_id_computer=computer)
        categories = computer_observations.values_list('f_id_observation__f_id_observation_category', flat=True)
        categories = list(set(categories))
        for category_id in categories:
            observations_of_category = computer_observations.filter(f_id_observation__f_id_observation_category=category_id)
            category_name = Observationcategory.objects.get(id_observation_category=category_id).category_name
            string_to_add = category_name+": "
            for computer_observation in observations_of_category:
                string_to_add += computer_observation.f_id_observation.full_name + ', '
            commentToReturn += string_to_add.strip(' ,;') + '; '
        commentToReturn += self._get_processed_string(computer.other)
        return commentToReturn.strip(' ,;')

    @staticmethod
    def _get_serial(computer):
        try:
            return computer.computer_serial
        except:
            return "N/A"

    @staticmethod
    def _get_manufacturer(computer):
        try:
            return computer.f_manufacturer.manufacturer_name
        except:
            return "N/A"

    @staticmethod
    def _get_model(computer):
        try:
            return computer.f_model.model_name
        except:
            return "N/A"

    @staticmethod
    def _get_cpu_name(computer):
        try:
            if computer.is5th_version():
                computer_processors = Computerprocessors.objects.filter(f_id_computer=computer)
                lst = []
                for computer_processor in computer_processors:
                    string = computer_processor.f_id_processor.f_manufacturer.manufacturer_name + ' ' + computer_processor.f_id_processor.model_name + ' ' + computer_processor.f_id_processor.stock_clock
                    lst.append(string)
                return ', '.join(lst).replace('Intel Intel', 'Intel').replace(' GHz', '')
            return computer.f_cpu.cpu_name
        except:
            return "N/A"

    @staticmethod
    def _get_ram_size(computer):
        try:
            if computer.is5th_version():
                ram_to_comp = RamToComp.objects.filter(f_id_computer_ram_to_com=computer)[0]
                return computer.f_ram_size.ram_size_text + ' ' + ram_to_comp.f_id_ram_ram_to_com.type
            return computer.f_ram_size.ram_size_text
        except:
            return "N/A"

    @staticmethod
    def _get_gpu_name(computer):
        try:
            if computer.is5th_version():
                computer_gpus = Computergpus.objects.filter(f_id_computer=computer)
                lst = []
                for computer_gpu in computer_gpus:
                    string = computer_gpu.f_id_gpu.f_id_manufacturer.manufacturer_name + ' ' + computer_gpu.f_id_gpu.gpu_name
                    if 'Intel HD' in string:
                        string = 'Intel HD'
                    lst.append(string)
                return ', '.join(lst)
            return computer.f_gpu.gpu_name
        except:
            return "N/A"

    @staticmethod
    def _get_hdd_size(computer):
        try:
            if computer.is5th_version():
                computer_drives = Computerdrives.objects.filter(f_id_computer=computer)
                lst = []
                for computer_drive in computer_drives:
                    type = ''
                    if computer_drive.f_drive.f_speed.speed_name.isdigit():
                        type = 'HDD'
                    else:
                        type = computer_drive.f_drive.f_speed.speed_name
                    string = type + ': ' + computer_drive.f_drive.f_hdd_sizes.hdd_sizes_name
                    lst.append(string)
                if len(lst) == 0:
                    return 'N/A'
                return ', '.join(lst)
            return computer.f_hdd_size.hdd_sizes_name
        except:
            return "N/A"

    @staticmethod
    def _get_battery_time(int_index):
        """
        Not fully implemented method, should somehow account for several batteries in a computer.
        For now it's just hardcoded that it lasts about an hour.
        :param int_index: computer's index in database.
        :return: string of computer's supposed expected lasting time on battery.
        """
        try:
            bat_to_comps = BatToComp.objects.filter(f_id_computer_bat_to_com=int_index)
            if len(bat_to_comps) > 2:
                return "~1h."
            elif len(bat_to_comps) < 1:
                return "No"
            else:
                return str(bat_to_comps[0].f_bat_bat_to_com.expected_time)
        except:
            return "N/A"

    @staticmethod
    def _get_diagonal(computer):
        try:
            return computer.f_diagonal.diagonal_text
        except:
            return "N/A"

    @staticmethod
    def _get_cdrom(computer):
        try:
            return computer.cdrom
        except:
            return "N/A"

    @staticmethod
    def _get_license(computer):
        try:
            return computer.f_license.license_name.replace('Windows ', 'Win')
        except:
            return "N/A"

    @staticmethod
    def _get_camera_option(computer):
        try:
            return computer.f_camera.option_name
        except:
            return "N/A"


class ExcelGenerator(AbstractDataFileGenerator):

    def __init__(self):
        self.memfile = io.BytesIO()
        super().__init__()

    def generate_file(self, indexes):
        workbook = xlsxwriter.Workbook(self.memfile)
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
        worksheet.write("M1", "Box no.", bold_bordered)
        worksheet.write("N1", "Comment", bold_bordered)
        worksheet.write("O1", "Price", bold_bordered)
        row = 1
        col = 0
        for int_index in indexes:
            computer = Computers.objects.get(id_computer=int_index)
            worksheet.write(row, col, self._get_serial(computer), bordered)
            worksheet.write(row, col + 1, self._get_manufacturer(computer), bordered)
            worksheet.write(row, col + 2, self._get_model(computer), bordered)
            worksheet.write(row, col + 3, self._get_cpu_name(computer), bordered)
            worksheet.write(row, col + 4, self._get_ram_size(computer), bordered)
            worksheet.write(row, col + 5, self._get_gpu_name(computer), bordered)
            worksheet.write(row, col + 6, self._get_hdd_size(computer), bordered)
            worksheet.write(row, col + 7, self._get_battery_time(int_index), bordered)
            worksheet.write(row, col + 8, self._get_diagonal(computer), bordered)
            worksheet.write(row, col + 9, self._get_cdrom(computer), bordered)
            worksheet.write(row, col + 10, self._get_license(computer), bordered)
            worksheet.write(row, col + 11, self._get_camera_option(computer), bordered)
            worksheet.write(row, col + 12, computer.box_number, bordered)
            worksheet.write(row, col + 13, self._form_comment(computer), bordered)
            row += 1
        workbook.close()
        return self.memfile


class CsvGenerator(AbstractDataFileGenerator):

    def __init__(self):
        self.memfile = io.StringIO()
        super().__init__()
        self.fieldnames = ["S/N", 'Manufacturer', 'Model', 'CPU', 'RAM', 'GPU', 'HDD', 'Batteries', 'LCD', 'Optical', 'COA',
                      'Cam', 'Box no.', 'Comment', 'Price']

    def generate_file(self, indexes):
        writer = csv.DictWriter(self.memfile, fieldnames=self.fieldnames)
        writer.writeheader()
        for int_index in indexes:
            computer = Computers.objects.get(id_computer=int_index)
            writer.writerow({
                "S/N": self._get_serial(computer),
                'Manufacturer': self._get_manufacturer(computer),
                'Model': self._get_model(computer),
                'CPU': self._get_cpu_name(computer),
                'RAM': self._get_ram_size(computer),
                'GPU': self._get_gpu_name(computer),
                'HDD': self._get_hdd_size(computer),
                'Batteries': self._get_battery_time(int_index),
                'LCD': self._get_diagonal(computer),
                'Optical': self._get_cdrom(computer),
                'COA': self._get_license(computer),
                'Cam': self._get_camera_option(computer),
                'Box no.': computer.box_number,
                'Comment': self._form_comment(computer),
                'Price': ''
            })
        return self.memfile


class Item:

    def __init__(self, item_id, item_name, permanence=0):
        self.id = item_id
        self.name = item_name
        self.permanence = bool(permanence)


def get_received_batches_list():
    recieved_batches = Receivedbatches.objects.all()
    recieved_batchlist = []
    for batch in recieved_batches:
        newItem = Item(batch.id_received_batch, batch.received_batch_name)
        recieved_batchlist.append(newItem)
    return recieved_batchlist


def save_received_batch(name):
    if name != "":
        Receivedbatches.objects.get_or_create(received_batch_name=name)


def edit_received_batch(data):
    recieved_batch = Receivedbatches.objects.get(id_received_batch=data["ItemId"])
    recieved_batch.received_batch_name = data["ItemName"]
    recieved_batch.save()


def delete_batch(index):
    recieved_batch = Receivedbatches.objects.get(id_received_batch=index)
    recieved_batch.delete()


def get_categories_list():
    cats = Categories.objects.all()
    catlist = []
    for cat in cats:
        newItem = Item(cat.id_category, cat.category_name, cat.permanent)
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


def delete_category(index):
    cat = Categories.objects.get(id_category=index)
    if cat.permanent != 1:
        cat.delete()


def get_types_list():
    types = Types.objects.all()
    typeslist = []
    for typie in types:
        newItem = Item(typie.id_type, typie.type_name)
        typeslist.append(newItem)
    return typeslist


def save_type(name):
    if name != "":
        Types.objects.get_or_create(type_name=name)


def edit_type(data):
    typ = Types.objects.get(id_type=data["ItemId"])
    typ.type_name = data["ItemName"]
    typ.save()


def delete_type(index):
    typ = Types.objects.get(id_type=index)
    typ.delete()


def get_testers_list():
    testers = Testers.objects.all()
    testerslist = []
    for tester in testers:
        newItem = Item(tester.id_tester, tester.tester_name)
        testerslist.append(newItem)
    return testerslist


def save_tester(name):
    if name != "":
        Testers.objects.get_or_create(tester_name=name)


def edit_tester(data):
    tes = Testers.objects.get(id_tester=data["ItemId"])
    tes.tester_name = data["ItemName"]
    tes.save()


def delete_tester(index):
    tes = Testers.objects.get(id_tester=index)
    tes.delete()


def get_observation_category_list():
    lst = []
    for member in Observationcategory.objects.all():
        lst.append(Item(item_id=member.id_observation_category, item_name=member.category_name))
    return lst


def save_observation_category(name):
    if name != "":
        Observationcategory.objects.get_or_create(category_name=name)


def delete_observation_category(index):
    item = Observationcategory.objects.get(id_observation_category=index)
    item.delete()


def edit_observation_category(data):
    item = Observationcategory.objects.get(id_observation_category=data["ItemId"])
    item.category_name = data["ItemName"]
    item.save()


def get_observation_subcategory_list():
    lst = []
    for member in Observationsubcategory.objects.all():
        lst.append(Item(item_id=member.id_observation_subcategory, item_name=member.subcategory_name))
    return lst


def save_observation_subcategory(name):
    if name != "":
        Observationsubcategory.objects.get_or_create(subcategory_name=name)


def delete_observation_subcategory(index):
    item = Observationsubcategory.objects.get(id_observation_subcategory=index)
    item.delete()


def edit_observation_subcategory(data):
    item = Observationsubcategory.objects.get(id_observation_subcategory=data["ItemId"])
    item.subcategory_name = data["ItemName"]
    item.save()


def get_all_observations_dict():
    variables = Observations.objects.all()
    observation_dict = dict()
    for variable in variables:
        cat_name = variable.f_id_observation_category.category_name
        sub_cat_name = variable.f_id_observation_subcategory.subcategory_name
        full_name = variable.full_name
        shortcode = variable.shortcode

        if not cat_name in observation_dict:
            observation_dict[cat_name] = {}
        if not sub_cat_name in observation_dict[cat_name]:
            observation_dict[cat_name][sub_cat_name] = {}
        observation_dict[cat_name][sub_cat_name][full_name] = shortcode
    return observation_dict


class ObservationMember:

    def __init__(self, id, shortcode, full_name):
        self.id = id
        self.shortcode = shortcode
        self.full_name = full_name

    def __str__(self):
       return "id: {0}, shortcode: {1}, full_name: {2}".format(self.id, self.shortcode, self.full_name)


class CollectionSecond:

    def __init__(self, category, subcategory):
        self.current = 0
        self.collection_name = subcategory
        self.css_selector = self.form_css_selector()
        self.collection = []
        self.get_collection(category)

    def form_css_selector(self):
        return self.collection_name.replace(' ', '_')

    def get_collection(self, category):
        values = Observations.objects.filter(
            f_id_observation_category__category_name=category,
            f_id_observation_subcategory__subcategory_name=self.collection_name
        )
        for value in values:
            observation_member = ObservationMember(
                id=value.id_observation,
                shortcode=value.shortcode,
                full_name=value.full_name
            )
            self.collection.append(observation_member)

    def __str__(self):
        return "collection_name: {0}, css_selector: {1}".format(self.collection_name, self.css_selector)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= len(self.collection):
            self.current = 0
            raise StopIteration
        else:
            self.current += 1
            return self.collection[self.current - 1]


class CollectionFirst:

    def __init__(self, collection_name):
        self.current = 0
        self.collection_name = collection_name
        self.css_selector = self.form_css_selector()
        self.collection = []
        self.get_collection()

    def form_css_selector(self):
        return self.collection_name.replace(' ', '_')

    def get_collection(self):
        values = Observations.objects.filter(f_id_observation_category__category_name=self.collection_name)\
            .values('f_id_observation_subcategory__subcategory_name').distinct()\
            .values_list('f_id_observation_subcategory__subcategory_name', flat=True)
        for value in values:
            collection = CollectionSecond(category=self.collection_name, subcategory=value)
            self.collection.append(collection)

    def __str__(self):
        return "collection_name: {0}, css_selector: {1}".format(self.collection_name, self.css_selector)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= len(self.collection):
            self.current = 0
            raise StopIteration
        else:
            self.current += 1
            return self.collection[self.current - 1]


class ObservationsCollection:

    def __init__(self):
        self.collection = self.processObservationsDict()
        self.current = 0

    def processObservationsDict(self):
        values = Observations.objects.values('f_id_observation_category__category_name').distinct().values_list('f_id_observation_category__category_name', flat=True)
        lst = []
        for value in values:
            collection = CollectionFirst(value)
            lst.append(collection)
        return lst

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= len(self.collection):
            self.current = 0
            raise StopIteration
        else:
            self.current += 1
            return self.collection[self.current - 1]

    def get_length(self):
        return len(self.collection)


class ObservationToAdd:

    def __init__(self, data_dict):
        print('in ObservationToAdd')
        self.message = ''
        self.cat_name = self.try_extract(data_dict, 'cat_name')
        self.sub_name = self.try_extract(data_dict, 'sub_name')
        self.shortcode = self.try_extract(data_dict, 'shortcode')
        self.full_name = self.try_extract(data_dict, 'full_name')
        
    def try_extract(self, data_dict, key):
        """
        Called by __init__ to help construct class attributes.
        If some value can't be extracted message attribute is appended.

        :param data_dict: querydict sent from client side website.
        :param key: key expected to be used for value's extraction.
        :return: None is returned if extraction failed, else extracted value.
        """
        try:
            extracted = data_dict[key]
            if extracted == '':
                self.message += '\'{0}\' was not set\r\n'.format(key)
            return extracted
        except:
            self.message += '\'{0}\' was not set\r\n'.format(key)

    def validated(self):
        """
        :return: if message is empty, that means everything is ok, hence returns True,
        else False and message attribute should be looked at.
        """
        return self.message == ''

    def process(self):
        """
        Creates supposed observation.

        :return: returns nothing and it's not expected to do so.
        """
        category = Observationcategory.objects.get(category_name=self.cat_name)
        subcategory = Observationsubcategory.objects.get(subcategory_name=self.sub_name)
        observation = Observations.objects.get_or_create(
            shortcode=self.shortcode,
            full_name=self.full_name,
            f_id_observation_category=category,
            f_id_observation_subcategory=subcategory
        )


class RecordToAdd:

    def __init__(self, data_dict):
        self.data = data_dict
        print(data_dict)
        self.error_list = []

    def get_error_message(self):
        """
        :return: string of concatinated errors by a newline characters.
        """
        return "\r\n".join(self.error_list)

    def save(self):
        """
        Saves computer record sent from website's querydict
        :return: None is returned, allways
        """
        print("rta save start")
        self._validate()
        if len(self.error_list) == 0:
            Computers.objects.create(
                computer_serial=self.data.get("serial"),
                f_type=Types.objects.get_or_create(type_name=self.data.get("type_name"))[0],
                f_category=Categories.objects.get_or_create(category_name=self.data.get("category_name"))[0],
                f_manufacturer=Manufacturers.objects.get_or_create(
                    manufacturer_name=self.data.get("manufacturer_name")
                )[0],
                f_model=Models.objects.get_or_create(model_name=self.data.get("model_name"))[0],
                f_cpu=Cpus.objects.get_or_create(cpu_name=self.data.get("cpu_name"))[0],
                f_gpu=Gpus.objects.get_or_create(gpu_name=self.data.get("gpu_name"))[0],
                f_ram_size=RamSizes.objects.get_or_create(ram_size_text=self.data.get("ram_size_text"))[0],
                f_hdd_size=HddSizes.objects.get_or_create(hdd_sizes_name=self.data.get("hdd_sizes_name"))[0],
                f_diagonal=Diagonals.objects.get_or_create(diagonal_text=self.data.get("diagonal_text"))[0],
                f_license=Licenses.objects.get_or_create(license_name=self.data.get("license_name"))[0],
                cover=self.data.get("cover"),
                display=self.data.get("display"),
                bezel=self.data.get("bezel"),
                hdd_cover=self.data.get("hdd_cover"),
                ram_cover=self.data.get("ram_cover"),
                other=self.data.get("other"),
                f_tester=Testers.objects.get_or_create(tester_name=self.data.get("tester_name"))[0],
                date=timezone.now(),
                f_id_received_batches=Receivedbatches.objects.get(
                    received_batch_name=self.data.get("received_batch_name")
                ),
                box_number=self.data.get("box_number")
            )
            print("record_to_add save end")
        else:
            print("record_to_add save FAILED")

    def isSaved(self):
        """
        Checks if there any errors in error_list.
        if there are no errors, True returned,
        else False is returned.
        :return: True/False
        """
        return len(self.error_list) == 0

    def _validate(self):
        """"
        Validates if all required fieldnames are present within provided queryset.
        """
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
            "tester_name",
            "received_batch_name",
            "box_number"
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
            "Tester was not set",
            "Received batch was not set",
            "Box number was not set"
        )

        for i in range(len(fieldnames)):
            if self.data.get(fieldnames[i]) == "" or self.data.get(fieldnames[i]) is None:
                self.error_list.append(error_messages[i])


class RecordChoices:
    """
    This class is representative of unique values available for manual data insertion in relation to computers.
    All attributes are unique values of their respective fields.
    """

    def __init__(self):
        self.types = Types.objects.values_list("type_name", flat=True)
        self.categories = Categories.objects.values_list("category_name", flat=True)
        self.manufacturers = Manufacturers.objects.values_list("manufacturer_name", flat=True)
        self.models = Models.objects.values_list("model_name", flat=True)
        self.rams = RamSizes.objects.values_list("ram_size_text", flat=True)
        self.diagonals = Diagonals.objects.values_list("diagonal_text", flat=True)
        self.licenses = Licenses.objects.values_list("license_name", flat=True)
        self.cameras = CameraOptions.objects.values_list("option_name", flat=True)
        self.testers = Testers.objects.values_list("tester_name", flat=True)
        self.received_batches = Receivedbatches.objects.values_list("received_batch_name", flat=True)

        # 4th version computers only
        self.cpus = Cpus.objects.values_list("cpu_name", flat=True)
        self.gpus = Gpus.objects.values_list("gpu_name", flat=True)
        self.hdds = HddSizes.objects.values_list("hdd_sizes_name", flat=True)

        # 5th version computers only
        self.resolutions = Resolutions.objects.values_list('resolution_text', flat=True)
        self.resolution_categories = Resolutioncategories.objects.values_list('resolution_category_name', flat=True)


class AutoFilter:
    """
    Class responsible for applying filters on a computers queryset.
    Attributes:
        keys(typple of strings) - hold on to keys which group what part of queryset should be filtered by. Logic is
        implemented in filter() method.
    """

    keys = ('man-af', 'sr-af', 'scr-af', 'ram-af', 'gpu-af', 'mod-af', 'cpu-af', 'oth-af', 'cli-af', 'dos-af', 'pri-af',
            'tes-af')

    def __init__(self, data_dict):
        """
        Builts internal collection by which filtering should take place.
        :param data_dict: key and value collection
        """
        self.filter_dict = {}
        for key in self.keys:
            if key in data_dict:
                self.filter_dict[key] = data_dict.pop(key)

    def filter(self, computers):
        """
        Based on attribute of filter_dict keys and values(collection of strings) filters computers queryset.

        :param computers: queryset of computers
        :return: filtered queryset of computers
        """
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
            elif key == 'tes-af':
                computers = computers.filter(f_tester__tester_name__in=value)
            elif key == 'pri-af':
                for i in range(len(value)):
                    if value[i] == 'None':
                        value[i] = None
                query = Q(price__in=value)
                if None in value:
                    query |= Q(price__isnull=True)
                computers = computers.filter(query)
        return computers


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace('', (str(t[0]) or str(t[1])).strip()) for t in findterms(query_string)]


def get_query(query_string):
    """
    Forms Q query to be used with filter() models method.
    :param query_string: searchable string string collection in form of string
    :return: Q object.
    """
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
    return computers.filter(get_query(keyword))


class ExecutorOfCatToSold:
    """
    Class dedicated for setting computers as sold.
    Attributes:
        error_list - list of errors which are apended to this attribute when something doesn't work as it should.
        idPrices - dictionary of id and price pairs of computers.
        client - string name of client to whom computers are sold to.
        validated - True/False value showing whether any errors are present in error_list.
    """

    def __init__(self, data_dict):
        self.error_list = []
        self.idPrices = {}
        self.client = None
        for key, value in data_dict.items():
            if "client" in key:
                self._validate_client(value)
                self.client = value
            if "price" in key:
                if self._is_price_valid(value):
                    self.idPrices[self._get_id(key)] = self._get_price(value)
        self.validated = len(self.error_list) == 0

    def write_to_database(self):
        """
        Writes to database attributes by distributing data through models.

        :return: None is returned always
        """
        dbClient = Clients.objects.get_or_create(client_name=self.client)[0]
        sale = Sales.objects.create(date_of_sale=timezone.now(), f_id_client=dbClient)
        for comp_id, price in self.idPrices.items():
            computer = Computers.objects.get(id_computer=comp_id)
            computer.price = price
            computer.f_sale = sale
            computer.save()

    def _validate_client(self, client):
        if client == "" or client == None:
            self.error_list.append("No client was specified")

    def _is_price_valid(self, price):
        if re.match(r'^[0-9]+[\.\,]{0,1}[0-9]{0,2}$', price) or price == "" or price is None:
            return True
        self.error_list.append('Price "' + price + '" is not a valid price')
        return False

    def _get_price(self, price):
        if price == "" or price is None:
            return 0
        return float(price.replace(",", "."))

    def _get_id(self, key):
        return key.split("_")[1]

    def get_error_message(self):
        return "\r\n".join(self.error_list)


class NewOrderChoices:

    def __init__(self):
        self.clients = Clients.objects.values_list("client_name", flat=True)
        self.testers = Testers.objects.values_list("tester_name", flat=True)


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

    def is_saved(self):
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
                self.error_list.append("Order with such name already exists")

        for indx, fieldname in enumerate(fieldnames):
            if self.data.get(fieldname) == "" or self.data.get(fieldname) is None:
                self.error_list.append(error_messages[indx])

    def _save_and_get_order(self):
        return Orders.objects.create(
            order_name=self.data.pop('order_name')[0],
            is_sent=0,
            creation_date=timezone.now(),
            f_id_client=Clients.objects.get_or_create(
                client_name=self.data.pop('client_name')[0]
            )[0]
        )


class Order:

    def __init__(self, order_object):
        self.id = order_object.id_order
        self.name = order_object.order_name
        self.is_sent = bool(order_object.is_sent)
        self.date = order_object.creation_date
        self.client = order_object.f_id_client.client_name
        self.testers = OrdTes.objects.filter(f_order=self.id).values_list("f_id_tester__tester_name", flat=True)

    def get_testers(self):
        """
        :return: string of concatinated tester list.
        """
        return ", ".join(self.testers)

    def is_ready(self):
        """
        :return: True if all computers belonging to an order have is_ready as 1, else False
        """
        return Computers.objects.filter(
            f_id_comp_ord__f_order_id_to_order=self.id,
            f_id_comp_ord__is_ready=0
        ).count() == 0

    def count(self):
        """
        :return: Integer count of computers in order.
        """
        return Computers.objects.filter(f_id_comp_ord__f_order_id_to_order=self.id).count()

    def get_status(self):
        """
        :return: String of order's status.
        """
        statuses = ("In-Preperation", "Ready", "Sent", "Empty")
        if self.count() == 0:
            return statuses[3]
        elif self.is_sent:
            return statuses[2]
        elif self.is_ready():
            return statuses[1]
        else:
            return statuses[0]


class OrdersClassAutoFilter:
    """
    Class responsible of holding unique values of order to filter by in website,
    """

    def __init__(self, orders):
        self.names = []
        self.clients = []
        self.qtys = []
        self.dates = []
        self.testers = []
        self.statuses = []
        for order in orders:
            self._append_unique_to_list(order.name, self.names)
            self._append_unique_to_list(order.client, self.clients)
            self._append_unique_to_list(order.count(), self.qtys)
            self._append_unique_to_list(order.date, self.dates)
            self.testers.extend(order.testers)
            self._append_unique_to_list(order.get_status(), self.statuses)
        self.names.sort()
        self.clients.sort()
        self.qtys.sort()
        self.dates.sort()
        self.testers = self._remove_duplicates_and_sort(self.testers)
        self.statuses.sort()


    def _remove_duplicates_and_sort(self, lst):
        # This line removes duplicates.
        lst = list(set(lst))
        # Returns sorted list
        return sorted(lst)

    def _append_unique_to_list(self, value, lst):
        if value not in lst:
            lst.append(value)


class OrdersClass:

    def __init__(self):
        self.order_list = []
        for ord in Orders.objects.all():
            self.order_list.append(Order(ord))
        self.autoFilters = OrdersClassAutoFilter(self.order_list)

    def filter(self, data_dict):
        """
        Filters Orders based on provided keys and values.
        :param data_dict:
        :return:
        """
        keys = ('ord-af', 'clt-af', 'qty-af', 'dat-af', 'tes-af', 'sta-af')
        new_dict = {}
        if 'orders' in data_dict:
            data_dict.pop('orders')
        for key in keys:
            if key in data_dict:
                new_dict[key] = data_dict.pop(key)
        for key, value in new_dict.items():
            if key == 'ord-af':
                for order in self.order_list[:]:
                    if not order.name in new_dict['ord-af']:
                        self.order_list.remove(order)
            elif key == 'clt-af':
                for order in self.order_list[:]:
                    if not order.client in new_dict['clt-af']:
                        self.order_list.remove(order)
            elif key == 'qty-af':
                for order in self.order_list[:]:
                    if not str(order.count) in new_dict['qty-af']:
                        self.order_list.remove(order)
            elif key == 'dat-af':
                for order in self.order_list[:]:
                    if not str(order.date) in new_dict['dat-af']:
                        self.order_list.remove(order)
            elif key == 'tes-af':
                for order in self.order_list[:]:
                    if not all(x in order.testers for x in new_dict['tes-af']):
                        self.order_list.remove(order)
            elif key == 'sta-af':
                for order in self.order_list[:]:
                    if not order.get_status() in new_dict['sta-af']:
                        self.order_list.remove(order)
        self.autoFilters = OrdersClassAutoFilter(self.order_list)


class PossibleOrders:

    def __init__(self):
        """
        Class holds orders which are not set_as_sent. Available as choices to be assigned to for computers.
        """
        self.orders = Orders.objects.exclude(is_sent=1).values_list("order_name", flat=True)


class TesterCustomClass:
    """
    Class responsible as holder for tester and whether this tester is assigned
    to a order from which this class is created.
    """

    def __init__(self, tester_name, assigned):
        self.tester_name = tester_name
        self.assigned = assigned


class OrderToEdit:
    """
    This class is reperesentative of order of computers.
    Showing order data and computers, testers belong to it.
    """

    def __init__(self, index):
        # This Order object is from logic and not the same as from models Orders.
        self.order = Order(Orders.objects.get(id_order=index))
        self.computers = Computers.objects.filter(f_id_comp_ord__f_order_id_to_order=self.order.id)
        self.testers = self._get_testers()
        # Used during verification(post method) to store what data is missing.
        self.error_list = []
        # Used as index in website
        self.count = 0

    def increment(self):
        """
        Increments counter
        :return: empty string
        """
        self.count += 1
        return ''

    def _get_testers(self):
        """
        Creates custom list of testers with their names and wether they are assigned to an order or not.
        :return: list of TesterCustomClass objects
        """
        testers = []
        for tester_name in Testers.objects.values_list("tester_name", flat=True):
            testers.append(TesterCustomClass(
                tester_name=tester_name,
                assigned=self._is_assigned(tester_name))
            )
        return testers

    def _is_assigned(self, tester_name):
        """
        :param tester_name: who is being checked whether he is assigned to an order or not.
        :return: True/False
        """
        return tester_name in self.order.testers

    def hasErrors(self):
        """
        :return: True if error_list contains members, False otherwise.
        """
        return not len(self.error_list)

    def get_error_message(self):
        """
        :return: Concatenated error_list as string.
        """
        return "\r\n".join(self.error_list)

    def set_new_data(self, data_dict):
        """
        :param data_dict: Querydict provided by post update from website for processing.
        :return: None is returned always.
        """

        def _validate():
            """
            Validates if all required fields contain required values.
            :return: True/False hasErrors() output.
            """
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
                "Testers were not set"
            )

            for fieldname, error_message in zip(fieldnames, error_messages):
                if data_dict.get(fieldname) == "" or data_dict.get(fieldname) is None:
                    self.error_list.append(error_message)
            if self.order.is_sent:
                self.error_list.append('Sent orders are not allowed for editing')
            return self.hasErrors()

        def _save_sale(order):
            """
            :param order: of whom sale is being checked.
            :return: Sales object if this order is set as being sold. Elsewise None
            """
            if new_is_sent_status == 1:
                return Sales.objects.create(date_of_sale=timezone.now(), f_id_client=order.f_id_client)
            return None
        
        def _get_order():
            """
            Sets orders sale, new client and whether order is set as sold.
            :return: changed order.
            """
            order = Orders.objects.get(id_order=data_dict.pop('order_id')[0])
            order.order_name = data_dict.pop('order_name')[0]
            order.f_id_client = Clients.objects.get_or_create(
                client_name=data_dict.pop('client_name')[0]
            )[0]
            order.is_sent = new_is_sent_status
            order.save()
            return order

        def _save_order_testers(order):
            """
            Removes previuos and sets new testers set for an order.
            :param order: order to testers should be changed.
            :return: None is returned always.
            """
            OrdTes.objects.filter(f_order=order).delete()
            for tester_name in data_dict.pop('tes'):
                OrdTes.objects.create(
                    f_order=order,
                    f_id_tester=Testers.objects.get(tester_name=tester_name)
                )

        def _save_computer_order_changes(computer, is_ready_value):
            """
            Saves compord, a connectional object between computer and an order.
            :return: None is returned always.
            """
            compord = CompOrd.objects.get(id_comp_ord=computer.f_id_comp_ord.id_comp_ord)
            compord.is_ready = is_ready_value
            compord.save()

        def _save_computer_changes(computer_id, is_ready_value, sale):
            """
            Calls to save computer order changes and saves sale.
            :return: None is returned always.
            """
            computer = Computers.objects.get(id_computer=computer_id)
            _save_computer_order_changes(computer, is_ready_value)
            computer.f_sale = sale
            computer.save()

        def _get_new_is_sent_status():
            """
            :return: 1 if in website client specifies that order is set as sent, 0 otherwise.
            """
            if 'set_as_sent' in data_dict:
                if data_dict.pop('set_as_sent')[0] == 'on':
                    return 1
            return 0
        
        def _get_computer_id(key):
            """
            Splits received string by underscore sign and returns second part of the split.
            ex: input "status_1937", output: "1937"
            :param key: String of status_*id of computer*
            :return: id of computer
            """
            return key.split('_')[1]

        def _get_status_index(value):
            """
            Accepts status used in website for an order and
            returns integer representing that status in database.
            :param value: String "In-Preperation" or "Ready"
            :return: Integer 1 or 0
            """
            statuses = ("In-Preperation", "Ready")
            return statuses.index(value)

        if _validate():
            new_is_sent_status = _get_new_is_sent_status()
            order = _get_order()
            sale = _save_sale(order)
            _save_order_testers(order)
            for key, value in data_dict.items():
                if 'status' in key:
                    _save_computer_changes(
                        computer_id=_get_computer_id(key),
                        is_ready_value=_get_status_index(value),
                        sale=sale
                    )

    """
    def process_uploaded_file(self, file):
        print("in process_uploaded_file")
        # print(file)
        # print(type(file))
        # print(magic.from_buffer(file.read(), mime=True))
        mimetype = magic.from_buffer(file.read(), mime=True)
        # print(mimetype.encode("unicode-escape"))
        # print(type(mimetype))
        file.seek(0)
        if mimetype == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            print("Excel")
            self._process_excel_file(file)
        elif mimetype == "text/plain":
            print("CSV")
            self._process_csv_file(file)
        else:
            print("Smth else")

    def _process_excel_file(self, file):
        print("Processing Excel file")
        id_dict = {
            "S/N": None,
            "Manufacturer": None,
            "Model": None,
            "CPU": None,
            "RAM": None,
            "GPU": None,
            "HDD": None,
            "Batteries": None,
            "LCD": None,
            "Optical": None,
            "COA": None,
            "Cam": None,
            "Box no.": None,
            "Comment": None,
            "Price": None
        }
        book = xlrd.open_workbook(file_contents=file.read())
        first_sheet = book.sheet_by_index(0)
        print(first_sheet)
        print(first_sheet.row(0))
        for index, cell in enumerate(first_sheet.row(0)):
            # print(dir(cell))
            # print("Type: {0}, Value: {1}".format(type(cell), cell))
            # print("Value: {0}".format(cell.value))
            print("Index: {0}, Value: {1}".format(index, cell.value))
            id_dict[cell.value] = index
        print(id_dict)
        num_cols = first_sheet.ncols
        for row_id in range(1, first_sheet.nrows):
            print(first_sheet.cell(row_id, id_dict["S/N"]).value)
            computers = Computers.objects.filter(computer_serial=first_sheet.cell(row_id, id_dict["S/N"]).value)
            print(computers)
            if computers.exists():
                print("Exists")
                comp_ord, created = CompOrd.objects.get_or_create(f_order_id_to_order=self.order, is_ready=0)
                print(created)
                computers.update(f_id_comp_ord=comp_ord)
            '''
            for col_id in range(0, num_cols):
                cell = first_sheet.cell(row_id, col_id)
                print("Row id: {0}, Column id: {1}, Cell: {2}".format(row_id, col_id, cell))
            '''
            print("=========================================")

    def _process_csv_file(self, file):
        print("Processing CSV file")
    """

def on_start():
    """
    This function is called from urls.py to ensure that it's run once.
    It is responsible for calling in seperate threads observers to monitor file creation.
    """
    print("on start")
    tarThread = Thread(target=start_tar_observer)
    txtThread = Thread(target=start_txt_observer)
    txtThread.start()
    tarThread.start()


def start_tar_observer():
    """
    Starts observation of provided directory and uses TarAndLogHandler to log errors and process Tar files.
    """
    observer = Observer()
    log_position = os.path.join(os.path.join(settings.BASE_DIR, 'logs'), 'observer.log')
    logging.basicConfig(
        filename=log_position,
        level=logging.WARNING,
        format="%(asctime)-15s %(threadName)s:%(message)s"
    )
    observer.schedule(
        event_handler=TarAndLogHandler(),
        path=os.path.join(os.path.join(settings.BASE_DIR, 'temp'))
    )
    logging.warning("Start of tar observer")
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        logging.warning('Ending observer, due to keyboard interupt')
        observer.stop()
        logging.warning('Observer ended')
    observer.join()


class TarAndLogHandler(PatternMatchingEventHandler):
    """
    Class responsible for evaluating events with tar extension and logging them.
    """
    patterns = ['*.tar']

    def process(self, event):
        logging.warning(event.src_path)
        logging.warning(event.event_type)
        atp = AlternativeTarProcessor(
            in_memory_file=event.src_path,
            filename=os.path.basename(event.src_path).replace('.tar', '')
        )
        atp.process_data()
        logging.warning('_________________________________________')

    def on_created(self, event):
        if not event.is_directory:
            self.process(event)


def start_txt_observer():
    """
    Starts observation of provided directory and uses TxtAndLogHandler to log errors and process txt files.
    """
    observer = Observer()
    log_position = os.path.join(os.path.join(settings.BASE_DIR, 'logs'), 'observer.log')
    logging.basicConfig(filename=log_position, level=logging.WARNING, format="%(asctime)-15s %(threadName)s:%(message)s")
    observer.schedule(TxtAndLogHandler(), os.path.join(os.path.join(settings.BASE_DIR, 'temp')))
    logging.warning("Start of txt observer")
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        logging.warning('Ending observer, due to keyboard interupt')
        observer.stop()
        logging.warning('Observer ended')
    observer.join()


class TxtAndLogHandler(PatternMatchingEventHandler):
    """
    Class responsible for evaluating events with tar extension and logging them.
    """
    patterns = ['*.txt']

    def process(self, event):
        logging.warning(event.src_path)
        logging.warning(event.event_type)
        ahop = AlternativeHddOrderProcessor(txt_object=event.src_path)
        ahop.process_data()
        logging.warning('_________________________________________')

    def on_created(self, event):
        if not event.is_directory:
            self.process(event)

'''
class HddWriter:

    def __init__(self, file, filename):
        self.file = file
        self.filename = filename

    def save(self):
        self._save_and_set_lots()
        lines_array = self._get_lines_array()
        for line in lines_array:
            line_array = line.split('@')

            model = self._save_and_get_models(line_array[2])
            size = self._save_and_get_size(line_array[3])
            lock_state = self._save_and_get_lock_state(line_array[4])
            speed = self._save_and_get_speed(line_array[5])
            form_factor = self._save_and_get_form_factor(line_array[6])
            self._save_hdd(line_array, model, size, lock_state, speed, form_factor)

    def _save_hdd(self, line_array, model, size, lock_state, speed, form_factor):
        if Drives.objects.filter(hdd_serial=line_array[1], f_hdd_models=model).exists():
            logging.warning("Such hdd allready exists")
            existing_hdd = Drives.objects.get(hdd_serial=line_array[1], f_hdd_models=model)
            logging.warning(existing_hdd)
            hdd = Drives(
                hdd_id=existing_hdd.hdd_id,
                hdd_serial=line_array[1],
                health=line_array[7].replace("%", ""),
                days_on=line_array[8],
                f_lot=self.lot,
                f_hdd_models=model,
                f_hdd_sizes=size,
                f_lock_state=lock_state,
                f_speed=speed,
                f_form_factor=form_factor
            )
            hdd.save()
        else:
            hdd = Drives(
                hdd_serial=line_array[1],
                health=line_array[7].replace("%", ""),
                days_on=line_array[8],
                f_lot=self.lot,
                f_hdd_models=model,
                f_hdd_sizes=size,
                f_lock_state=lock_state,
                f_speed=speed,
                f_form_factor=form_factor
            )
            hdd.save()

    def _get_lines_array(self):
        content = self.file.read()
        try:
            content = content.decode("utf-8")
        except AttributeError:
            pass
        linesArray = content.split('\n')
        del linesArray[-1]
        return linesArray

    def _save_and_set_lots(self):
        try:
            self.lot = Lots.objects.get(lot_name=self.filename)
        except Lots.DoesNotExist:
            self.lot = Lots(
                lot_name=self.filename,
                date_of_lot=timezone.now().today().date()
            )
            self.lot.save()

    def _save_and_get_models(self, model):
        model_to_return = HddModels.objects.get_or_create(hdd_models_name=model)[0]
        return model_to_return

    def _save_and_get_size(self, size):
        size_to_return = HddSizes.objects.get_or_create(hdd_sizes_name=size)[0]
        return size_to_return

    def _save_and_get_lock_state(self, lock):
        lock_to_return = LockState.objects.get_or_create(lock_state_name=lock)[0]
        return lock_to_return

    def _save_and_get_speed(self, speed):
        speed_to_return = Speed.objects.get_or_create(speed_name=speed)[0]
        return speed_to_return

    def _save_and_get_form_factor(self, form_factor):
        form_factor_to_return = FormFactor.objects.get_or_create(form_factor_name=form_factor)[0]
        return form_factor_to_return
'''

class LotHolder:

    def __init__(self, lot_id, lot_name, date_of_lot, count):
        self.lot_id = lot_id
        self.lot_name = lot_name
        self.date_of_lot = date_of_lot
        self.count = count


class LotsHolderAutoFilter:
    """
    Class responsible of holding unique values of hdd lots to filter by in website.
    """

    def __init__(self, lots):
        self.lots_names = []
        self.dates_of_lots = []
        self.counts = []
        for lot in lots:
            self._append_unique_to_list(lot.lot_name, self.lots_names)
            self._append_unique_to_list(lot.date_of_lot, self.dates_of_lots)
            self._append_unique_to_list(lot.count, self.counts)
        self.lots_names.sort()
        self.dates_of_lots.sort()
        self.counts.sort()

    def _append_unique_to_list(self, value, lst):
        if value not in lst:
            lst.append(value)


class LotsHolder:

    def __init__(self):
        self.count = 0
        self.lots = self._get_lots()
        self.autoFilters = LotsHolderAutoFilter(self.lots)

    def increment(self):
        self.count += 1
        return ''

    def _get_lots(self):
        lots_to_return = []
        for lot in Lots.objects.all():
            lots_to_return.append(
                LotHolder(
                    lot_id=lot.lot_id,
                    lot_name=lot.lot_name,
                    date_of_lot=lot.date_of_lot,
                    count=Drives.objects.filter(f_lot=lot.lot_id).count()
                )
            )
        return lots_to_return

    def filter(self, data_dict):
        keys = ('nam-af', 'day-af', 'cnt-af')
        new_dict = {}
        if 'lots' in data_dict:
            data_dict.pop('lots')
        for key in keys:
            if key in data_dict:
                new_dict[key] = data_dict.pop(key)
        for key, value in new_dict.items():
            if key == 'nam-af':
                for lot in self.lots[:]:
                    if not lot.lot_name in new_dict[key]:
                        self.lots.remove(lot)
            elif key == 'day-af':
                for lot in self.lots[:]:
                    if not str(lot.date_of_lot) in new_dict[key]:
                        self.lots.remove(lot)
            elif key == 'cnt-af':
                for lot in self.lots[:]:
                    if not str(lot.count) in new_dict[key]:
                        self.lots.remove(lot)


class HddHolder:

    def __init__(self):
        self.count = 0
        self.hdds = Drives.objects.all()
        self.autoFilters = HddAutoFilterOptions(self.hdds)
        self.changedKeys = []

    def increment(self):
        self.count += 1
        return ''

    def filter(self, data_dict):
        keys = ('ser-af', 'mod-af', 'siz-af', 'loc-af', 'spe-af', 'for-af', 'hp-af', 'day-af')
        new_dict = {}
        if 'hdds' in data_dict:
            data_dict.pop('hdds')
        for key in keys:
            if key in data_dict:
                new_dict[key] = data_dict.pop(key)
        for key, value in new_dict.items():
            if key in keys:
                self.changedKeys.append(key)
                if key == 'ser-af':
                    self.hdds = self.hdds.filter(hdd_serial__in=new_dict[key])
                elif key == 'mod-af':
                    self.hdds = self.hdds.filter(f_hdd_models__hdd_models_name__in=new_dict[key])
                elif key == 'siz-af':
                    self.hdds = self.hdds.filter(f_hdd_sizes__hdd_sizes_name__in=new_dict[key])
                elif key == 'loc-af':
                    self.hdds = self.hdds.filter(f_lock_state__lock_state_name__in=new_dict[key])
                elif key == 'spe-af':
                    self.hdds = self.hdds.filter(f_speed__speed_name__in=new_dict[key])
                elif key == 'for-af':
                    self.hdds = self.hdds.filter(f_form_factor__form_factor_name__in=new_dict[key])
                elif key == 'hp-af':
                    self.hdds = self.hdds.filter(health__in=new_dict[key])
                elif key == 'day-af':
                    self.hdds = self.hdds.filter(days_on__in=new_dict[key])
        self.autoFilters = HddAutoFilterOptions(self.hdds)


class HddAutoFilterOptions:
    """
    Class responsible of holding unique values of hdd to filter by in website,
    """

    def __init__(self, hdds):
        self.serials = hdds.values_list('hdd_serial', flat=True).distinct().order_by('hdd_serial')
        self.models = hdds.values_list('f_hdd_models__hdd_models_name', flat=True).distinct().order_by(
            'f_hdd_models__hdd_models_name')
        self.sizes = hdds.values_list('f_hdd_sizes__hdd_sizes_name', flat=True).distinct().order_by(
            'f_hdd_sizes__hdd_sizes_name')
        self.locks = hdds.values_list('f_lock_state__lock_state_name', flat=True).distinct().order_by(
            'f_lock_state__lock_state_name')
        self.speeds = hdds.values_list('f_speed__speed_name', flat=True).distinct().order_by('f_speed__speed_name')
        self.forms = hdds.values_list('f_form_factor__form_factor_name', flat=True).distinct().order_by(
            'f_form_factor__form_factor_name')
        self.healths = hdds.values_list('health', flat=True).distinct().order_by('health')
        self.days = hdds.values_list('days_on', flat=True).distinct().order_by('days_on')

    def _append_unique_to_list(self, value, lst):
        if value not in lst:
            lst.append(value)


class LotContentHolder:

    def __init__(self, index):
        self.lot = Lots.objects.get(lot_id=index)
        self.hdds = Drives.objects.filter(f_lot=self.lot)
        self.autoFilters = HddAutoFilterOptions(self.hdds)
        self.changedKeys = []

    def filter(self, data_dict):
        keys = ('siz-af', 'loc-af', 'day-af', 'for-af', 'spe-af', 'mod-af', 'hp-af', 'ser-af')
        new_dict = {}
        for key in keys:
            if key in data_dict:
                new_dict[key] = data_dict.pop(key)
        for key, value in new_dict.items():
            self.changedKeys.append(key)
            if key == 'siz-af':
                self.hdds = self.hdds.filter(f_hdd_sizes__hdd_sizes_name__in=new_dict[key])
            elif key == 'loc-af':
                self.hdds = self.hdds.filter(f_lock_state__lock_state_name__in=new_dict[key])
            elif key == 'day-af':
                self.hdds = self.hdds.filter(days_on__in=new_dict[key])
            elif key == 'for-af':
                self.hdds = self.hdds.filter(f_form_factor__form_factor_name__in=new_dict[key])
            elif key == 'spe-af':
                self.hdds = self.hdds.filter(f_speed__speed_name__in=new_dict[key])
            elif key == 'mod-af':
                self.hdds = self.hdds.filter(f_hdd_models__hdd_models_name__in=new_dict[key])
            elif key == 'hp-af':
                self.hdds = self.hdds.filter(health__in=new_dict[key])
            elif key == 'ser-af':
                self.hdds = self.hdds.filter(hdd_serial__in=new_dict[key])
            self.autoFilters = HddAutoFilterOptions(self.hdds)


class HddOrderToDelete:

    def __init__(self, index):
        self.message = ''
        self.order = HddOrder.objects.get(order_id=index)
        self.hdds = Drives.objects.filter(f_hdd_order=self.order)
        self.success = False

    def delete(self):
        try:
            self.hdds.update(f_hdd_order=None)
            self.order.delete()
            self.success = True
        except Exception as e:
            self.message = str(e)
            self.success = False


class HddOrderContentHolder:

    def __init__(self, index):
        self.hdd_order = HddOrder.objects.get(order_id=index)
        self.hdds = Drives.objects.filter(f_hdd_order=self.hdd_order)
        self.autoFilters = HddAutoFilterOptions(self.hdds)
        self.changedKeys = []
        self.available_statuses = OrderStatus.objects.filter(is_shown=1)

    def filter(self, data_dict):
        keys = ('siz-af', 'loc-af', 'day-af', 'for-af', 'spe-af', 'mod-af', 'hp-af', 'ser-af')
        new_dict = {}
        for key in keys:
            if key in data_dict:
                new_dict[key] = data_dict.pop(key)
        for key, value in new_dict.items():
            self.changedKeys.append(key)
            if key == 'siz-af':
                self.hdds = self.hdds.filter(f_hdd_sizes__hdd_sizes_name__in=new_dict[key])
            elif key == 'loc-af':
                self.hdds = self.hdds.filter(f_lock_state__lock_state_name__in=new_dict[key])
            elif key == 'day-af':
                self.hdds = self.hdds.filter(days_on__in=new_dict[key])
            elif key == 'for-af':
                self.hdds = self.hdds.filter(f_form_factor__form_factor_name__in=new_dict[key])
            elif key == 'spe-af':
                self.hdds = self.hdds.filter(f_speed__speed_name__in=new_dict[key])
            elif key == 'mod-af':
                self.hdds = self.hdds.filter(f_hdd_models__hdd_models_name__in=new_dict[key])
            elif key == 'hp-af':
                self.hdds = self.hdds.filter(health__in=new_dict[key])
            elif key == 'ser-af':
                self.hdds = self.hdds.filter(hdd_serial__in=new_dict[key])
            self.autoFilters = HddAutoFilterOptions(self.hdds)

    def edit(self, data_dict):
        order = self._get_order(data_dict)
        if order:
            old_order = self.hdd_order.f_order_status
            self.hdd_order.f_order_status = order
            self.hdd_order.save()
            if not HddOrder.objects.filter(f_order_status=old_order).exists():
                if old_order.is_shown == 0:
                    old_order.delete()

    def _get_order(self, data_dict):
        if 'status_name' in data_dict:
            return OrderStatus.objects.filter(order_status_name=data_dict['status_name'])[0]
        elif 'other_name' in data_dict:
            newOrderStatus = OrderStatus(
                order_status_name=data_dict['other_name'],
                is_shown=0
            )
            newOrderStatus.save()
            return newOrderStatus
        return None


class HddToEdit:
    """
    Class responsible of editing hdd attributes and providing unique values of hdd's sizes, states, speeds and
    form factors to be used for hdd modifying.
    """

    def __init__(self, index):
        self.hdd = Drives.objects.get(hdd_id=index)
        self.sizes = HddSizes.objects.values_list('hdd_sizes_name', flat=True).distinct().order_by('hdd_sizes_name')
        self.states = LockState.objects.values_list('lock_state_name', flat=True).distinct().order_by('lock_state_name')
        self.speeds = Speed.objects.values_list('speed_name', flat=True).distinct().order_by('speed_name')
        self.form_factors = FormFactor.objects.values_list('form_factor_name', flat=True).distinct()\
            .order_by('form_factor_name')

    def process_edit(self, data_dict):
        '''
        Edits hdd's attributes based on provided data_dict
        :param data_dict: Attributes passed from website.
        '''
        model = HddModels.objects.get_or_create(hdd_models_name=data_dict.pop('model')[0])[0]
        size = HddSizes.objects.get_or_create(hdd_sizes_name=data_dict.pop('size')[0])[0]
        state = LockState.objects.get_or_create(lock_state_name=data_dict.pop('state')[0])[0]
        speed = Speed.objects.get_or_create(speed_name=data_dict.pop('speed')[0])[0]
        form_factor = FormFactor.objects.get_or_create(form_factor_name=data_dict.pop('form_factor')[0])[0]
        self.hdd.hdd_serial = data_dict.pop('serial')[0]
        self.hdd.health = data_dict.pop('health')[0]
        self.hdd.days_on = data_dict.pop('days')[0]
        self.hdd.f_hdd_models = model
        self.hdd.f_hdd_sizes = size
        self.hdd.f_lock_state = state
        self.hdd.f_speed = speed
        self.hdd.f_form_factor = form_factor
        self.hdd.save()


class HddToDelete:

    def __init__(self, pk=None, serial=None):
        if pk:
            self.hdd = Drives.objects.filter(hdd_id=pk)[0]
        if serial:
            self.hdd = Drives.objects.filter(hdd_serial=serial)[0]
        self.success = False
        self.message = ''

    def delete(self):
        try:
            try:
                os.system('tar -vf ' + os.path.join(os.path.join(settings.BASE_DIR, 'tarfiles'), self.hdd.f_lot.lot_name + '.tar') + ' --delete "' + self.hdd.tar_member_name + '"')
            except:
                pass
            self.hdd.delete()
            self.success = True
            print('Succesful deletion')
        except Exception as e:
            self.success = False
            self.message = 'Failure to delete record\r\n'+str(e)
            print('Failed deletion')


class TarProcessor:

    def __init__(self, inMemoryFile, filename=None):
        if filename is None:
            self.lot_name = inMemoryFile._name.replace('.tar', '')
            self.tar = tarfile.open(fileobj=inMemoryFile.file)
            self.fileLoc = ''
        else:
            self.lot_name = filename.replace('.tar', '')
            self.tar = tarfile.open(inMemoryFile)
            self.fileLoc = filename

    def process_data(self):
        self._save_and_set_lots()
        for member in self.tar.getmembers():
            if '.txt' in member.name:
                file = self.tar.extractfile(member)
                with open(os.path.join(os.path.join(settings.BASE_DIR, 'logs'), 'failed.log'), 'a') as logfile:
                    textToWrite = '* importing lot ' + self.lot_name + ' || ' + str(datetime.date.today()) + ' *\r\n'
                    isMissing = False
                    new_tarfile_loc = os.path.join(os.path.join(settings.BASE_DIR, 'tarfiles'), self.lot_name + '.tar')
                    with tarfile.open(new_tarfile_loc, 'a') as new_tar:
                        for bline in file.readlines():
                            try:
                                line = bline.decode('utf-8')
                                line_array = line.split('@')
                                if self.isValid(line_array):
                                    tarmember = self.get_tar_member_by_serial(line_array)
                                    if self._hdd_exists(line_array):
                                        if tarmember is not None:
                                            isMissing = True
                                            tarmember_to_remove = self.get_tarmember_name(line_array)
                                            if tarmember_to_remove is not None:
                                                tarmember_to_remove = self.get_tarmember_name(line_array)
                                                try:
                                                    new_tar.getmember(tarmember_to_remove)
                                                    os.system('tar -vf '+new_tarfile_loc+' --delete "'+tarmember_to_remove+'"')
                                                except:
                                                    print('Tarfile opening or its deletion had failed')
                                                    pass
                                            filename = tarmember.name
                                            file = self.tar.extractfile(tarmember)
                                            new_tar.addfile(tarmember, file)
                                            self._update_existing_hdd(line_array, filename)
                                            textToWrite += 'SN: ' + line_array[1] + '| info updated. File updated.\r\n'
                                        else:
                                            self._update_existing_hdd_without_file(line_array)
                                            isMissing = True
                                            textToWrite += 'SN: ' + line_array[1] + '| Record info updated. File info not changed.\r\n'
                                    else:
                                        if tarmember is not None:
                                            file = self.tar.extractfile(tarmember)
                                            filename = tarmember.name
                                            new_tar.addfile(tarmember, file)
                                            self._save_new_hdd(line_array, filename)
                                        else:
                                            isMissing = True
                                            textToWrite += 'SN: ' + line_array[1] + '| skipped. Not present in database. No file associated.\r\n'
                                else:
                                    textToWrite += 'SN: ' + line_array[1] + '| values which should be numbers, are not.\r\n'
                            except Exception as e:
                                isMissing = True
                                textToWrite +='\r\n Error: ' + str(e)+' \r\n'
                        textToWrite += '===============================================\r\n'
                        if isMissing:
                            logfile.write(textToWrite)
        try:
            if self.fileLoc != '':
                os.remove(self.fileLoc)
        except:
            pass

    def get_tarmember_name(self, line_array):
        model = HddModels.objects.get_or_create(hdd_models_name=line_array[2])[0]
        hdd = Drives.objects.filter(hdd_serial=line_array[1], f_hdd_models=model)[0]
        return hdd.tar_member_name

    def get_tar_member_by_serial(self, line_array):
        for member in self.tar.getmembers():
            if '(S-N ' + line_array[1] + ')' in member.name:
                return member
        return None

    def isValid(self, line_array):
        if line_array[7].replace("%", "").strip().isdigit() and line_array[8].strip().isdigit():
            return True
        return False

    def _update_existing_hdd_without_file(self, line_array):
        model = HddModels.objects.get_or_create(hdd_models_name=line_array[2])[0]
        hdd = Drives.objects.filter(hdd_serial=line_array[1], f_hdd_models=model)[0]
        size = self._save_and_get_size(line_array[3])
        lock_state = self._save_and_get_lock_state(line_array[4])
        speed = self._save_and_get_speed(line_array[5])
        form_factor = self._save_and_get_form_factor(line_array[6])
        hdd.f_hdd_sizes = size
        hdd.f_lock_state = lock_state
        hdd.f_speed = speed
        hdd.f_form_factor = form_factor
        hdd.health = line_array[7].replace("%", "")
        hdd.days_on = line_array[8]
        hdd.f_lot = self.lot
        hdd.save()

    def _update_existing_hdd(self, line_array, filename):
        model = HddModels.objects.get_or_create(hdd_models_name=line_array[2])[0]
        hdd = Drives.objects.filter(hdd_serial=line_array[1], f_hdd_models=model)[0]
        size = self._save_and_get_size(line_array[3])
        lock_state = self._save_and_get_lock_state(line_array[4])
        speed = self._save_and_get_speed(line_array[5])
        form_factor = self._save_and_get_form_factor(line_array[6])
        hdd.f_hdd_sizes = size
        hdd.f_lock_state = lock_state
        hdd.f_speed = speed
        hdd.f_form_factor = form_factor
        hdd.health = line_array[7].replace("%", "")
        hdd.days_on = line_array[8]
        hdd.tar_member_name = filename
        hdd.f_lot = self.lot
        hdd.save()

    def _save_new_hdd(self, line_array, filename):
        model = self._save_and_get_models(line_array[2])
        size = self._save_and_get_size(line_array[3])
        lock_state = self._save_and_get_lock_state(line_array[4])
        speed = self._save_and_get_speed(line_array[5])
        form_factor = self._save_and_get_form_factor(line_array[6])
        hdd = Drives(
            hdd_serial=line_array[1],
            health=line_array[7].replace("%", ""),
            days_on=line_array[8],
            tar_member_name=filename,
            f_lot=self.lot,
            f_hdd_models=model,
            f_hdd_sizes=size,
            f_lock_state=lock_state,
            f_speed=speed,
            f_form_factor=form_factor
        )
        hdd.save()

    def _hdd_exists(self, line_array):
        model = HddModels.objects.get_or_create(hdd_models_name=line_array[2])[0]
        hdd = Drives.objects.filter(hdd_serial=line_array[1], f_hdd_models=model)
        return hdd.exists()

    def _save_hdd(self, line_array, model, size, lock_state, speed, form_factor):
        if Drives.objects.filter(hdd_serial=line_array[1], f_hdd_models=model).exists():
            logging.warning("Such hdd allready exists")
            existing_hdd = Drives.objects.get(hdd_serial=line_array[1], f_hdd_models=model)
            logging.warning(existing_hdd)
            logging.warning(existing_hdd.__dict__)
            hdd = Drives(
                hdd_id=existing_hdd.hdd_id,
                hdd_serial=line_array[1],
                health=line_array[7].replace("%", ""),
                days_on=line_array[8],
                f_lot=self.lot,
                f_hdd_models=model,
                f_hdd_sizes=size,
                f_lock_state=lock_state,
                f_speed=speed,
                f_form_factor=form_factor
            )
            hdd.save()
        else:
            hdd = Drives(
                hdd_serial=line_array[1],
                health=line_array[7].replace("%", ""),
                days_on=line_array[8],
                f_lot=self.lot,
                f_hdd_models=model,
                f_hdd_sizes=size,
                f_lock_state=lock_state,
                f_speed=speed,
                f_form_factor=form_factor
            )
            hdd.save()

    def _save_and_set_lots(self):
        try:
            self.lot = Lots.objects.get(lot_name=self.lot_name)
        except Lots.DoesNotExist:
            self.lot = Lots(
                lot_name=self.lot_name,
                date_of_lot=timezone.now().today().date()
            )
            self.lot.save()

    def _save_and_get_models(self, model):
        model_to_return = HddModels.objects.get_or_create(hdd_models_name=model)[0]
        return model_to_return

    def _save_and_get_size(self, size):
        size_to_return = HddSizes.objects.get_or_create(hdd_sizes_name=size)[0]
        return size_to_return

    def _save_and_get_lock_state(self, lock):
        lock_to_return = LockState.objects.get_or_create(lock_state_name=lock)[0]
        return lock_to_return

    def _save_and_get_speed(self, speed):
        speed_to_return = Speed.objects.get_or_create(speed_name=speed)[0]
        return speed_to_return

    def _save_and_get_form_factor(self, form_factor):
        form_factor_to_return = FormFactor.objects.get_or_create(form_factor_name=form_factor)[0]
        return form_factor_to_return


class WriteableMessage:
    """
    Class responsible of holding text inside and true/false value
    for determining whether to use that text for next operations or not.
    """

    def __init__(self, text=''):
        self.text = text
        self.should_write = False

    def add(self, string_to_add, should_write=None):
        """
        :param string_to_add: string which is added to self.text attribute.
        :param should_write: True/False, whether text should be later written into log or not.
        :return: None is returned always
        """
        self.text += string_to_add + '\r\n'
        if should_write:
            self.should_write = should_write


class AlternativeTarProcessor:
    """
    Class responsible of handling tar processing.
    It is alternative version of TarProcessor.
    File columns can change their positions, new ones could be added and this class still should be able to process it.
    """
    headers = ['Serial number', 'Health', 'Power_On', 'Model', 'Capacity', 'Lock', 'Speed', 'Size']

    def __init__(self, in_memory_file, filename=None):
        """
        In case of upload through a website filename is not passed to __init__.
        In case of file creation being caught by watchdog, filename is passed to __init__.
        :param in_memory_file: memory file to be processed
        :param filename: filename which is provided with the help of watchdog.
        """
        if filename is None:
            # Lot name is assigned based on file's name.
            self.lot_name = in_memory_file._name.replace('.tar', '')
            self.tar = tarfile.open(fileobj=in_memory_file.file)
            self.file_loc = ''
        else:
            self.lot_name = filename.replace('.tar', '')
            self.tar = tarfile.open(in_memory_file)
            self.file_loc = filename
        self.txt_file = self.get_txt_file()
        # firstline represents header of the custom txt file
        self.firstline = self.get_first_line(self.txt_file)
        self.text_to_write = WriteableMessage()
        self.lot = None
        self.file_header_indexes = None

    @property
    def message(self):
        """
        Method called from view to return what failed to html response.
        """
        return self.text_to_write.text

    def process_data(self):
        """
        Opens logfile failed.log to keep it in case self.text_to_write should be written into.
        Initiation of whole data processing within the class.
        """
        with open(os.path.join(os.path.join(settings.BASE_DIR, 'logs'), 'failed.log'), 'a') as logfile:
            self.text_to_write.add('* importing lot ' + self.lot_name + ' || ' + str(datetime.date.today()) + ' *')
            if self.is_header_valid(self.firstline):
                self.process_file_with_valid_headers()
            else:
                self.text_to_write.add(
                    # string_to_add='All required fields in '+self.lot_name+' were not found:\r\n'+str(self.headers),
                    string_to_add='All required fields in {0} were not found:\r\n{1}'
                    .format(self.lot_name, self.headers),
                    should_write=True
                )
                self.text_to_write.add('===============================================')
            if self.text_to_write.should_write:
                logfile.write(self.text_to_write.text)

    def process_file_with_valid_headers(self):
        self.lot = self._save_and_get_lots()
        self.file_header_indexes = self._get_file_header_indexes(self.firstline.split('@'))
        new_tarfile_loc = self._get_new_tarfile_location()
        with tarfile.open(new_tarfile_loc, 'a') as new_tar:
            for line in self.txt_file.readlines():
                self.try_processing_line(line=line, new_tar=new_tar, new_tarfile_loc=new_tarfile_loc)

    def try_processing_line(self, line, new_tar, new_tarfile_loc):
        """
        :param line: line in a file representing one drive.
        :param new_tar: tar created for this class.
        :param new_tarfile_loc: Location where new_tar is located.
        """
        try:
            self._process_line(line=line, new_tar=new_tar, new_tarfile_loc=new_tarfile_loc)
        except Exception as e:
            self.text_to_write.add(string_to_add='\r\n Error: {0} \r\n'.format(e), should_write=True)
            
    def _process_line(self, line, new_tar, new_tarfile_loc):
        """
        Processes one line of txt file representing drive.
        :param line: line in a file representing one drive.
        :param new_tar: tar created for this class.
        :param new_tarfile_loc: Location where new_tar is located.
        :return:
        """
        line_array = self._get_line_array(line)
        if self.is_valid(line_array):
            self._process_valid_line_array(
                line_array=line_array,
                new_tar=new_tar,
                new_tarfile_loc=new_tarfile_loc
            )
        else:
            self.text_to_write.add(
                # string_to_add='SN: ' + line_array[self.file_header_indexes['Serial number']] + '| skipped. Health or Power on is not a proper digit.',
                tring_to_add='SN: {0}| skipped. Health or Power on is not a proper digit.'
                .format(line_array[self.file_header_indexes['Serial number']]),
                should_write=True
            )

    def _process_valid_line_array(self, line_array, new_tar, new_tarfile_loc):
        """
        :param line_array: list of strings to process.
        :param new_tar: tar created for this class.
        :param new_tarfile_loc: Location where new_tar is located.
        :return:
        """
        tarmember = self.get_tar_member_by_serial(line_array[self.file_header_indexes['Serial number']])
        if self._drive_exists(line_array):
            self._process_existing_hdd(
                line_array=line_array,
                new_tar=new_tar,
                new_tarfile_loc=new_tarfile_loc,
                tarmember=tarmember
            )
        else:
            self._process_nonexistant_hdd(line_array=line_array, new_tar=new_tar, tarmember=tarmember)

    def _process_existing_hdd(self, line_array, new_tar, new_tarfile_loc, tarmember):
        """
        :param line_array: list of strings to process.
        :param new_tar: tar created for this class.
        :param new_tarfile_loc: Location where new_tar is located.
        :param tarmember: uploaded tar file's pdf member.
        """
        if tarmember:
            self._process_tarmember_with_existing_hdd(
                line_array=line_array,
                new_tar=new_tar,
                new_tarfile_loc=new_tarfile_loc,
                tarmember=tarmember
            )
            self.text_to_write.add(
                # string_to_add='SN: ' + line_array[self.file_header_indexes['Serial number']] + '| info updated. File updated.',
                string_to_add='SN: {0}| info updated. File updated.'
                .format(line_array[self.file_header_indexes['Serial number']]),
                should_write=True
            )
        else:
            self._update_existing_drive(line_array=line_array)
            self.text_to_write.add(
                # string_to_add='SN: ' + line_array[self.file_header_indexes['Serial number']] + '| Record info updated. File info not changed.'
                string_to_add='SN: {0}| Record info updated. File info not changed.'
                .format(line_array[self.file_header_indexes['Serial number']])
            )

    def _process_nonexistant_hdd(self, tarmember, new_tar, line_array):
        """
        Calls to save new drive if has associated tar member.
        :param tarmember: uploaded tar file's pdf member.
        :param new_tar: tar created for this class.
        :param line_array: list of strings to process.
        :return:
        """
        if tarmember:
            new_tar.addfile(tarmember, self.tar.extractfile(tarmember))
            self._save_new_drive(line_array, tarmember.name)
        else:
            self.text_to_write.add(
                # string_to_add='SN: ' + line_array[self.file_header_indexes['Serial number']] + '| skipped. Not present in database. No file associated.',
                string_to_add='SN: {0}| skipped. Not present in database. No file associated.'
                .format(line_array[self.file_header_indexes['Serial number']]),
                should_write=True
            )

    def _process_tarmember_with_existing_hdd(self, line_array, new_tar, new_tarfile_loc, tarmember):
        """
        :param line_array: list of strings to process.
        :param new_tar: tar created for this class.
        :param new_tarfile_loc: Location where new_tar is located.
        :param tarmember: uploaded tar file's pdf member.
        """
        self._try_to_remove_tarmember(
            line_array=line_array,
            new_tar=new_tar,
            new_tarfile_loc=new_tarfile_loc
        )
        new_tar.addfile(tarmember, self.tar.extractfile(tarmember))
        self._update_existing_drive(line_array, tarmember.name)

    def _try_to_remove_tarmember(self, line_array, new_tar, new_tarfile_loc):
        """
        Removes tarmember out of new tar file, to avoid file duplications in new tar file.
        :param line_array: list of strings to process.
        :param new_tar: tar created for this class.
        :param new_tarfile_loc: Location where new_tar is located.
        """
        try:
            tarmember_to_remove = self.get_tarmember_name(line_array)
            if tarmember_to_remove is not None:
                new_tar.getmember(tarmember_to_remove)
                # os.system('tar -vf ' + new_tarfile_loc + ' --delete "' + tarmember_to_remove + '"')
                os.system('tar -vf {0} --delete "{1}"'.format(new_tarfile_loc, tarmember_to_remove))
        except:
            print('Tarfile opening or its deletion had failed')
            pass

    def _get_new_tarfile_location(self):
        """
        :return: full path name wher tarfiles should be saved.
        """
        # return os.path.join(os.path.join(settings.BASE_DIR, 'tarfiles'), self.lot_name + '.tar')
        return os.path.join(os.path.join(settings.BASE_DIR, 'tarfiles'), '{0}.tar'.format(self.lot_name))

    def _get_line_array(self, line):
        """
        :param line: string to process.
        :return: convert line to utf-8 if it's not, and returns it as line_array.
        """
        try:
            return line.decode('utf-8').split('@')
        except:
            return line.split('@')

    def get_tarmember_name(self, line_array):
        """
        Returns tarmember name based on line_array's serial number and model.
        :param line_array: list of strings to process.
        :return: name of tarmember
        """
        drive = Drives.objects.filter(
            hdd_serial=line_array[self.file_header_indexes['Serial number']],
            f_hdd_models=HddModels.objects.get(hdd_models_name=self.file_header_indexes['Model'])
        )[0]
        return drive.tar_member_name

    def _save_and_get_lots(self):
        """
        if Lot exists with self.lot_name returns existing one, if not creates new one and returns that one.
        :return: Lots object
        """
        try:
            return Lots.objects.get(lot_name=self.lot_name)
        except Lots.DoesNotExist:
            return Lots.objects.create(
                lot_name=self.lot_name,
                date_of_lot=timezone.now().today().date()
            )

    def get_txt_file(self):
        """
        :return: first found txt file in tar.
        """
        for member in self.tar.getmembers():
            if '.txt' in member.name:
                return self.tar.extractfile(member)

    def get_first_line(self, txt_object):
        """
        :param txt_object: text file as an object
        :return: first line of text file
        """
        return txt_object.readline().strip().decode('utf8')

    def is_header_valid(self, line):
        """
        :param line: first_line, which should represent file's header row.
        :return: True if all required headers from self.headers are present in line, returns True, else False.
        """
        for header in self.headers:
            if header not in line:
                return False
        return True

    def _get_file_header_indexes(self, file_headers):
        """
        :param file_headers: Headers present in the file.
        :return: Dictionary of header and index position's pair, of a required columns.
        """
        file_header_indexes = dict()
        for value in self.headers:
            file_header_indexes[value] = file_headers.index(value)
        return file_header_indexes

    def is_valid(self, line_array):
        """
        :param line_array: list of strings to process.
        :return: True if health is number, with possible percentage sign and Power_on is number, else False
        """
        return line_array[self.file_header_indexes['Health']].replace("%", "").strip().isdigit() \
            and line_array[self.file_header_indexes['Power_On']].strip().isdigit()

    def get_tar_member_by_serial(self, serial):
        """
        :param serial: Drive's serial to look for in Tar.
        :return: tarfile if exists or None if doesn't.
        """
        for member in self.tar.getmembers():
            if '(S-N ' + serial + ')' in member.name:
                return member
        return None

    def _drive_exists(self, line_array):
        """
        :param line_array: list of strings to process.
        :return: True/False, whether such drive with such serial and model exists or not.
        """
        model = HddModels.objects.get_or_create(hdd_models_name=line_array[self.file_header_indexes['Model']])[0]
        drive = Drives.objects.filter(
            hdd_serial=line_array[self.file_header_indexes['Serial number']],
            f_hdd_models=model
        )
        return drive.exists()

    def _save_new_drive(self, line_array, filename):
        """
        :param line_array: list of strings to process.
        :param filename: filename of tarred pdf file.
        :return: None is returned always.
        """
        Drives.objects.create(
            hdd_serial=line_array[self.file_header_indexes['Serial number']],
            health=line_array[self.file_header_indexes['Health']].replace("%", ""),
            days_on=line_array[self.file_header_indexes['Power_On']],
            tar_member_name=filename,
            f_lot=self.lot,
            f_hdd_models=HddModels.objects.get_or_create(
                hdd_models_name=line_array[self.file_header_indexes['Model']]
            )[0],
            f_hdd_sizes=HddSizes.objects.get_or_create(
                hdd_sizes_name=line_array[self.file_header_indexes['Capacity']]
            )[0],
            f_lock_state=LockState.objects.get_or_create(
                lock_state_name=line_array[self.file_header_indexes['Lock']]
            )[0],
            f_speed=Speed.objects.get_or_create(
                speed_name=line_array[self.file_header_indexes['Speed']]
            )[0],
            f_form_factor=FormFactor.objects.get_or_create(
                form_factor_name=line_array[self.file_header_indexes['Size']]
            )[0]
        )

    def _update_existing_drive(self, line_array, filename=None):
        """
        :param line_array: list of strings to process.
        :param filename: filename is passed only if drive has coresponding tarred pdf file to it.
        :return: None is returned always.
        """
        drive = Drives.objects.filter(
            hdd_serial=line_array[self.file_header_indexes['Serial number']],
            f_hdd_models=HddModels.objects.get_or_create(
                hdd_models_name=line_array[self.file_header_indexes['Model']]
            )[0]
        )[0]
        drive.f_hdd_sizes = HddSizes.objects.get_or_create(
            hdd_sizes_name=line_array[self.file_header_indexes['Capacity']]
        )[0]
        drive.f_lock_state = LockState.objects.get_or_create(
            lock_state_name=line_array[self.file_header_indexes['Lock']]
        )[0]
        drive.f_speed = Speed.objects.get_or_create(
            speed_name=line_array[self.file_header_indexes['Speed']]
        )[0]
        drive.f_form_factor = FormFactor.objects.get_or_create(
            form_factor_name=line_array[self.file_header_indexes['Size']]
        )[0]
        drive.health = line_array[self.file_header_indexes['Health']].replace("%", "")
        drive.days_on = line_array[self.file_header_indexes['Power_On']]
        if filename:
            drive.tar_member_name = filename
        drive.f_lot = self.lot
        drive.save()


class HddOrderProcessor:

    def __init__(self, txtObject):
        self.message = ''
        if type(txtObject) is str:
            filename = os.path.basename(txtObject)
            txtObject = open(txtObject, "r")
        else:
            filename = txtObject._name
        hddOrder = self.get_hdd_order(filename)
        with open(os.path.join(os.path.join(settings.BASE_DIR, 'logs'), 'failed.log'), 'a') as logfile:
            isMissing = False
            textToWrite = '* importing order ' + filename.replace('.txt', '') + ' || ' + str(datetime.date.today()) + ' *\r\n'
            for line in txtObject.readlines():
                try:
                    line = line.decode('utf-8')
                except:
                    pass
                line_array = line.split('@')
                if self.isValid(line_array):
                    model = HddModels.objects.get_or_create(hdd_models_name=line_array[2])[0]
                    hdds = Drives.objects.filter(hdd_serial=line_array[1], f_hdd_models=model)
                    if hdds.exists():
                        if hdds[0].f_hdd_order is not None:
                            isMissing = True
                            textToWrite += 'SN: ' + hdds[0].hdd_serial + '| had order asign. Was assigned to order ' + hdds[0].f_hdd_order.order_name
                        hdds.update(f_hdd_order=hddOrder)
                    else:
                        model = HddModels.objects.get_or_create(hdd_models_name=line_array[2])[0]
                        size = HddSizes.objects.get_or_create(hdd_sizes_name=line_array[3])[0]
                        lock_state = LockState.objects.get_or_create(lock_state_name=line_array[4])[0]
                        speed = Speed.objects.get_or_create(speed_name=line_array[5])[0]
                        form_factor = FormFactor.objects.get_or_create(form_factor_name=line_array[6])[0]
                        hdd = Drives(
                            hdd_serial=line_array[1],
                            health=line_array[7].replace("%", ""),
                            days_on=line_array[8],
                            f_hdd_models=model,
                            f_hdd_sizes=size,
                            f_lock_state=lock_state,
                            f_speed=speed,
                            f_form_factor=form_factor,
                            f_hdd_order=hddOrder
                        )
                        hdd.save()
            textToWrite += '===============================================\r\n'
            if isMissing:
                logfile.write(textToWrite)
                self.message = textToWrite

    def isValid(self, line_array):
        if line_array[7].replace("%", "").strip().isdigit() and line_array[8].strip().isdigit():
            return True
        return False

    def get_hdd_order(self, txtFileName):
        hddOrders = HddOrder.objects.filter(order_name=txtFileName.replace('.txt', ''))
        if hddOrders.exists():
            hdds = Drives.objects.filter(f_hdd_order=hddOrders[0].order_id)
            hdds.update(f_hdd_order=None)
            hddOrders[0].delete()
        orderStatus = OrderStatus.objects.get(order_status_id=3)
        hddOrder = HddOrder(
            order_name=txtFileName.replace('.txt', ''),
            date_of_order=timezone.now().today().date(),
            f_order_status=orderStatus
        )
        hddOrder.save()
        return hddOrder


class AlternativeHddOrderProcessor:
    """
    Class responsible for processing order txt files,
    either provided from website or as a file copied into temp directory.
    """
    headers = ['Serial number', 'Health', 'Power_On', 'Model', 'Capacity', 'Lock', 'Speed', 'Size']

    def __init__(self, txt_object):
        if type(txt_object) is str:
            self.filename = os.path.basename(txt_object)
            self.txt_object = open(txt_object, "r")
        else:
            self.filename = txt_object._name
            self.txt_object = txt_object
        self.hddOrder = None
        self.file_header_indexes = None
        self.text_to_write = WriteableMessage()

    def process_data(self):
        """
        Processes text file representing an order.
        """
        firstline = self._get_first_line(self.txt_object)
        if self._is_header_valid(firstline):
            self._process_file_with_valid_headers(firstline)
        else:
            self.text_to_write.text = 'All required fields in '+self.filename+' were not found:\r\n'+str(self.headers)+'\r\n'
            self.text_to_write.should_write = True

    def _process_file_with_valid_headers(self, firstline):
        """
        :param firstline: first line of text file.
        """
        file_headers = firstline.split('@')
        self.file_header_indexes = self._get_file_header_indexes(file_headers)
        self.hddOrder = self._get_hdd_order(self.filename)
        with open(os.path.join(os.path.join(settings.BASE_DIR, 'logs'), 'failed.log'), 'a') as logfile:
            self.text_to_write.add(
                string_to_add='* importing order ' + self.filename.replace('.txt', '') + ' || ' + str(
                    datetime.date.today()) + ' *'
            )
            for line in self.txt_object.readlines():
                self._process_line(line)
            self.text_to_write.add('===============================================')
            if self.text_to_write.should_write:
                logfile.write(self.text_to_write.text)
            
    def _process_line(self, line):
        """
        Processes line, if it's valid passes to _process_valid_line_array, else add's to logfile that line is not valid.
        :param line: One line of text read from txt file.
        """
        line_array = self._get_line_array(line)
        if self._is_valid(line_array):
            self._process_valid_line_array(line_array)
        else:
            self.text_to_write.add(
                string_to_add='Hdd with S/N: ' + line_array[self.file_header_indexes[
                    'Serial number']] + ' most likely has incorrect health and days_on, because they were not found to be numbers.',
                should_write=True
            )

    def _process_valid_line_array(self, line_array):
        """
        :param line_array: list of strings to process.
        """
        model = HddModels.objects.get_or_create(
            hdd_models_name=line_array[self.file_header_indexes['Model']]
        )[0]
        hdds = Drives.objects.filter(
            hdd_serial=line_array[self.file_header_indexes['Serial number']],
            f_hdd_models=model
        )
        self._process_hdd(line_array, model, hdds)

    def _process_hdd(self, line_array, model, hdds):
        """
        Calls _update_existing_hdd() or _save_new_drive() based whether there are any hdds in given queryset.
        :param line_array: list of strings to process.
        :param model: HddModel object.
        :param hdds:queryset of hdds.
        :return:
        """
        if hdds.exists():
            self._update_existing_hdd(hdds)
        else:
            self._save_new_drive(line_array, model)

    def _update_existing_hdd(self, hdds):
        '''
        Updates existing hdds with new order.
        :param hdds: queryset of hdds.
        '''
        if hdds[0].f_hdd_order:
            self.text_to_write.add(
                string_to_add='SN: ' + hdds[0].hdd_serial + '| had order asign. Was assigned to order ' + hdds[0].f_hdd_order.order_name,
                should_write=True
            )
        hdds.update(f_hdd_order=self.hddOrder)

    @property
    def message(self):
        """
        Method called from view to return what failed to html response.
        """
        return self.text_to_write.text

    def _save_new_drive(self, line_array, model):
        """
        Saves order's new  drive.
        :param line_array: list of strings to process.
        :param model: HddModel object for a drive saving.
        """
        Drives.objects.create(
            hdd_serial=line_array[self.file_header_indexes['Serial number']],
            health=line_array[self.file_header_indexes['Health']].replace("%", ""),
            days_on=line_array[self.file_header_indexes['Power_On']],
            f_hdd_models=model,
            f_hdd_sizes=HddSizes.objects.get_or_create(
                hdd_sizes_name=line_array[self.file_header_indexes['Capacity']]
            )[0],
            f_lock_state=LockState.objects.get_or_create(
                lock_state_name=line_array[self.file_header_indexes['Lock']]
            )[0],
            f_speed=Speed.objects.get_or_create(
                speed_name=line_array[self.file_header_indexes['Speed']]
            )[0],
            f_form_factor=FormFactor.objects.get_or_create(
                form_factor_name=line_array[self.file_header_indexes['Size']]
            )[0],
            f_hdd_order=self.hddOrder
        )

    def _get_line_array(self, line):
        """
        :param line: string to process.
        :return: convert line to utf-8 if it's not, and returns it as line_array.
        """
        try:
            return line.decode('utf-8').split('@')
        except:
            return line.split('@')

    def _get_file_header_indexes(self, file_headers):
        """
        :param file_headers: Headers present in the file.
        :return: Dictionary of header and index position's pair, of a required columns.
        """
        file_header_indexes = dict()
        for value in self.headers:
            file_header_indexes[value] = file_headers.index(value)
        return file_header_indexes

    def _get_first_line(self, txt_object):
        """
        :param txt_object: text file as an object
        :return: first line of text file
        """
        try:
            return txt_object.readline().strip().decode('utf8')
        except:
            return txt_object.readline().strip()

    def _is_header_valid(self, line):
        """
        :param line: first_line, which should represent file's header row.
        :return: True if all required headers from self.headers are present in line, returns True, else False.
        """
        for header in self.headers:
            if header not in line:
                return False
        return True

    def _is_valid(self, line_array):
        """
        :param line_array: list of strings to process.
        :return: True if health is number, with possible percentage sign and Power_on is number, else False
        """
        return line_array[self.file_header_indexes['Health']].replace("%", "").strip().isdigit() \
            and line_array[self.file_header_indexes['Power_On']].strip().isdigit()

    def _get_hdd_order(self, txt_file_name):
        """
        Strips hdds out of existing order with same name, and deletes order with text file's name as an order's name.
        :return: HddOrder's object which should have Prepared status and text file's name as an order's name.
        """
        hdd_orders = HddOrder.objects.filter(order_name=txt_file_name.replace('.txt', ''))
        if hdd_orders.exists():
            print('Such hdd orders exists')
            Drives.objects.filter(f_hdd_order=hdd_orders[0].order_id).update(f_hdd_order=None)
            hdd_orders[0].delete()

        return HddOrder.objects.create(
            order_name=txt_file_name.replace('.txt', ''),
            date_of_order=timezone.now().today().date(),
            f_order_status=OrderStatus.objects.get(order_status_id=3)
        )


class HddOrderHolder:

    def __init__(self, order_id, order_name, date_of_order, order_status_name, count):
        self.order_id = order_id
        self.order_name = order_name
        self.date_of_order = date_of_order
        self.order_status_name = order_status_name
        self.count = count


class HddOrdersHolderAutoFilter:
    """
    Class responsible of holding unique values of hdd orders to filter by in website.
    """

    def __init__(self, orders):
        self.orders_names = []
        self.dates_of_orders = []
        self.order_status_names = []
        self.counts = []
        for order in orders:
            self._append_unique_to_list(order.order_name, self.orders_names)
            self._append_unique_to_list(order.date_of_order, self.dates_of_orders)
            self._append_unique_to_list(order.order_status_name, self.order_status_names)
            self._append_unique_to_list(order.count, self.counts)
        self.orders_names.sort()
        self.dates_of_orders.sort()
        self.order_status_names.sort()
        self.counts.sort()

    def _append_unique_to_list(self, value, lst):
        if value not in lst:
            lst.append(value)


class HddOrdersHolder:

    def __init__(self):
        self.count = 0
        self.orders = self._get_orders()
        self.autoFilters = HddOrdersHolderAutoFilter(self.orders)

    def increment(self):
        self.count += 1
        return ''

    def filter(self, data_dict):
        keys = ('hon-af', 'dat-af', 'cnt-af', 'ost-af')
        new_dict = {}
        for key in keys:
            if key in data_dict:
                new_dict[key] = data_dict.pop(key)
        for key, value in new_dict.items():
            if key == 'hon-af':
                for order in self.orders[:]:
                    if not order.order_name in new_dict[key]:
                        self.orders.remove(order)
            elif key == 'dat-af':
                for order in self.orders[:]:
                    if not str(order.date_of_order) in new_dict[key]:
                        self.orders.remove(order)
            elif key == 'cnt-af':
                for order in self.orders[:]:
                    if not str(order.count) in new_dict[key]:
                        self.orders.remove(order)
            elif key == 'ost-af':
                for order in self.orders[:]:
                    if not str(order.order_status_name) in new_dict[key]:
                        self.orders.remove(order)
        self.autoFilters = HddOrdersHolderAutoFilter(self.orders)

    def _get_orders(self):
        orders = []
        for order in HddOrder.objects.all():
            orders.append(
                HddOrderHolder(
                    order_id=order.order_id,
                    order_name=order.order_name,
                    date_of_order=order.date_of_order,
                    order_status_name=order.f_order_status.order_status_name,
                    count=Drives.objects.filter(f_hdd_order=order).count()
                )
            )
        return orders


class ChargerSerialProcessor:
    """
    Class responsible for processing scanned charger QRs .
    """

    def __init__(self, serial):
        self.manufacturer_name, middle_section, self.charger_serial = serial.split('_')
        self.wattage, self.connector_type = middle_section.split('W', 1)
        self.message = ''

    def serial_exists(self):
        return Chargers.objects.filter(charger_serial=self.charger_serial).exists()

    def process(self):
        if self._is_category_existing():
            print('Such charger category allready exists')
            self._proccess_existing_category_charger()
        else:
            print('No such charger category  exist')
            self._proccess_new_category_charger()

    def _is_category_existing(self):
        return ChargerCategories.objects.filter(
            f_manufacturer__manufacturer_name=self.manufacturer_name,
            watts=self.wattage,
            connector_type=self.connector_type
        ).exists()

    def _proccess_existing_category_charger(self):
        Chargers.objects.get_or_create(
            charger_serial=self.charger_serial,
            f_charger_category=ChargerCategories.objects.get(
                f_manufacturer__manufacturer_name=self.manufacturer_name,
                watts=self.wattage,
                connector_type=self.connector_type
            )
        )
        print('End of existing_charger')

    def _proccess_new_category_charger(self):
        Chargers.objects.get_or_create(
            charger_serial=self.charger_serial,
            f_charger_category=ChargerCategories.objects.create(
                watts=self.wattage,
                f_manufacturer=Manufacturers.objects.get_or_create(manufacturer_name=self.manufacturer_name)[0],
                connector_type=self.connector_type
            )
        )
        print('End of new_charger')


class ChargerHolder:

    def __init__(self, serial=None):
        if serial:
            self.charger = Chargers.objects.get(charger_serial=serial.split('_')[2])
        self.qty = Chargers.objects.filter(f_charger_category=self.charger.f_charger_category).count()


class ChargerCategoryHolder:

    def __init__(self, chargerCategory):
        self.chargerCategory = chargerCategory
        self.qty = Chargers.objects.filter(f_charger_category=self.chargerCategory).count()


class ChargerCategoriesHolder:

    def __init__(self):
        self.count = 0
        self.chargerCategories = []
        for cat in ChargerCategories.objects.all():
            self.chargerCategories.append(ChargerCategoryHolder(cat))

    def filter(self, data_dict):
        keys = ('man-af', 'watts-af', 'dcmin-af', 'dcmax-af', 'count-af', 'orig-af', 'used-af')
        new_dict = {}
        if 'chargers' in data_dict:
            data_dict.pop('chargers')
        for key in keys:
            if key in data_dict:
                new_dict[key] = data_dict.pop(key)
        for key, value in new_dict.items():
            if key == 'man-af':
                for cat in self.chargerCategories[:]:
                    if not cat.chargerCategory.f_manufacturer.manufacturer_name in new_dict['man-af']:
                        self.chargerCategories.remove(cat)
            if key == 'watts-af':
                for cat in self.chargerCategories[:]:
                    if not str(cat.chargerCategory.watts) in new_dict['watts-af']:
                        self.chargerCategories.remove(cat)
            if key == 'dcmin-af':
                for cat in self.chargerCategories[:]:
                    if not str(cat.chargerCategory.dcoutvoltsmin) in new_dict['dcmin-af']:
                        self.chargerCategories.remove(cat)
            if key == 'dcmax-af':
                for cat in self.chargerCategories[:]:
                    if not str(cat.chargerCategory.dcoutvoltsmax) in new_dict['dcmax-af']:
                        self.chargerCategories.remove(cat)
            if key == 'count-af':
                for cat in self.chargerCategories[:]:
                    if not str(cat.qty) in new_dict['count-af']:
                        self.chargerCategories.remove(cat)
            if key == 'orig-af':
                for cat in self.chargerCategories[:]:
                    if not str(cat.chargerCategory.is_original()) in new_dict['orig-af']:
                        self.chargerCategories.remove(cat)
            if key == 'used-af':
                for cat in self.chargerCategories[:]:
                    if not str(cat.chargerCategory.is_used()) in new_dict['used-af']:
                        self.chargerCategories.remove(cat)

    def increment(self):
        self.count += 1
        return ''

    def unique_manufacturers(self):
        holder = []
        for chargerCategory in self.chargerCategories:
            self._append_unique_to_list(chargerCategory.chargerCategory.f_manufacturer.manufacturer_name, holder)
        return sorted(holder)

    def unique_watts(self):
        holder = []
        for chargerCategory in self.chargerCategories:
            self._append_unique_to_list(chargerCategory.chargerCategory.watts, holder)
        return sorted(holder)

    def unique_dcoutvoltsmin(self):
        holder = []
        for chargerCategory in self.chargerCategories:
            self._append_unique_to_list(chargerCategory.chargerCategory.dcoutvoltsmin, holder)
        return sorted(holder)

    def unique_dcoutvoltsmax(self):
        holder = []
        for chargerCategory in self.chargerCategories:
            self._append_unique_to_list(chargerCategory.chargerCategory.dcoutvoltsmax, holder)
        return sorted(holder)

    def unique_counts(self):
        holder = []
        for chargerCategory in self.chargerCategories:
            self._append_unique_to_list(chargerCategory.qty, holder)
        return sorted(holder)

    def unique_originals(self):
        holder = []
        for chargerCategory in self.chargerCategories:
            self._append_unique_to_list(chargerCategory.chargerCategory.is_original(), holder)
        return sorted(holder)

    def unique_used(self):
        holder = []
        for chargerCategory in self.chargerCategories:
            self._append_unique_to_list(chargerCategory.chargerCategory.is_used(), holder)
        return sorted(holder)

    def _append_unique_to_list(self, value, lst):
        if value not in lst:
            lst.append(value)


class ChargerCategoryToEdit:
    """
    Class responsible for editing charger category.
    """

    def __init__(self, index):
        self.chargerCategory = ChargerCategories.objects.get(charger_category_id=index)
        self.qty = Chargers.objects.filter(f_charger_category=self.chargerCategory).count()
        self.chargers = Chargers.objects.filter(f_charger_category=self.chargerCategory).order_by('charger_serial')
        self.counter = 0
        self.message = ''
        self.isValidData = True

    def process(self, data_dict):
        """
        Checks validity of data passed by website.
        If data is valid it is saved.
        :param data_dict: data passed from website in a form of dictionary.
        """
        required_string_fields = ('manufacturer_name', 'connector_type')
        required_string_values = [None, None]
        required_boolean_fields = ('is_original', 'is_used')
        required_boolean_values = [None, None]
        required_integer_fields = ('connector_contacts_qty', 'watts')
        required_integer_values = [None, None]
        required_decimal_fields = ('connector_inner_diameter', 'connector_outer_diameter', 'dcoutvoltsmin', 'dcoutvoltsmax', 'dcoutampers')
        required_decimal_values = [None, None, None, None, None]
        optional_integer_fields = ('acinhzmin', 'acinhzmax')
        optional_integer_values = [None, None]
        optional_decimal_fields = ('acinampers', 'acinvoltsmin', 'acinvoltsmax')
        optional_decimal_values = [None, None, None]

        fields_list = [required_string_fields, required_boolean_fields, required_integer_fields,
                  required_decimal_fields, optional_integer_fields, optional_decimal_fields]
        values_list = [required_string_values, required_boolean_values, required_integer_values,
                  required_decimal_values, optional_integer_values, optional_decimal_values]
        methods_list = [self._get_required_string_field_value, self._get_required_bool_field_value,
                   self._get_required_integer_field_value, self._get_required_decimal_field_value,
                   self._get_optional_integer_field_value, self._get_optional_decimal_field_value]

        try:
            for fields, values, method in zip(fields_list, values_list, methods_list):
                self._run_method_on_lists(fields, values, method, data_dict)

            if self.isValidData:
                print('Charger edit data passed is valid')
                print(self.message)
                self._save(rsv=required_string_values, rbv=required_boolean_values,
                           riv=required_integer_values, rdv=required_decimal_values,
                           oiv=optional_integer_values, odv=optional_decimal_values)
            else:
                print('Charger edit data passed is wrong')
                print(self.message)

        except Exception as e:
            self.isValidData = False
            self.message = str(e)

    def _run_method_on_lists(self, fields, values, method, data_dict):
        """
        Iterates through fields, values and methods and assigns using methods and fieldnames appropriate values.
        :param fields: List of fields from which values should be extracted out of data dict.
        :param values: List of values in which extracted values should be stored.
        :param method: Methods which should be run in order to check validity of extracted values.
        :param data_dict: data passed from website in a form of dictionary.
        """
        for index, value in enumerate(fields):
            values[index] = method(data_dict, value)

    def _save(self, rsv, rbv, riv, rdv, oiv, odv):
        """
        Saves charger category based on value lists given.
        :param rsv: required_string_values.
        :param rbv: required_boolean_values.
        :param riv: required_integer_values.
        :param rdv: required_decimal_values.
        :param oiv: optional_integer_values.
        :param odv: optional_decimal_values.
        """
        print('Starting saving process')
        manufacturer = Manufacturers.objects.get_or_create(manufacturer_name=rsv[0])[0]
        self.chargerCategory.f_manufacturer = manufacturer
        self.chargerCategory.watts = riv[1]
        self.chargerCategory.acinvoltsmin = odv[1]
        self.chargerCategory.acinvoltsmax = odv[2]
        self.chargerCategory.acinampers = odv[0]
        self.chargerCategory.acinhzmin = oiv[0]
        self.chargerCategory.acinhzmax = oiv[1]
        self.chargerCategory.dcoutvoltsmin = rdv[2]
        self.chargerCategory.dcoutvoltsmax = rdv[3]
        self.chargerCategory.dcoutampers = rdv[4]
        self.chargerCategory.connector_inner_diameter = rdv[0]
        self.chargerCategory.connector_outer_diameter = rdv[1]
        self.chargerCategory.connector_contacts_qty = riv[0]
        self.chargerCategory.originality_status = rbv[0]
        self.chargerCategory.used_status = rbv[1]
        self.chargerCategory.connector_type = rsv[1]
        self.chargerCategory.save()
        print('Finished saving process')

    def _get_optional_decimal_field_value(self, data_dict, field_name):
        """
        Check's if value in a given fieldname out of data_dict is valid float value or not.
        If value is empty string or 'none' returns None,
        if value valid float then function returns float number,
        if neither adds error to the message and returns None.
        :param data_dict: data passed from website in a form of dictionary.
        :param field_name: Fieldname of value to extract out of data dict.
        :return: float or None.
        """
        try:
            value = data_dict.pop(field_name, '')[0]
            value = value.replace(',', '.')
            if value == '' or value.lower() == 'none':
                return None
            if value.replace('.', '', 1).isdigit():
                return float(value)
            else:
                self.message += 'Value in '+field_name+' should be decimal number, empty string or None\r\n'
        except:
            self.message += 'Failed to retrieve ' + field_name + '\r\n'

    def _get_optional_integer_field_value(self, data_dict, field_name):
        """
        Check's if value in a given fieldname out of data_dict is valid int value or not.
        If value is empty string or 'none' returns None
        if value valid int then function returns int number,
        if neither adds error to the message and returns None.
        :param data_dict: data passed from website in a form of dictionary.
        :param field_name: Fieldname of value to extract out of data dict.
        :return: Integer or None.
        """
        try:
            value = data_dict.pop(field_name, '')[0]
            if value == '' or value.lower() == 'none':
                return None
            if value.isdigit():
                return int(value)
            else:
                self.message += 'Value in '+field_name+' should be an integer\r\n'
        except:
            self.message += 'Failed to retrieve ' + field_name + '\r\n'

    def _get_required_string_field_value(self, data_dict, field_name):
        """
        Check's if value in a given fieldname out of data_dict is valid string value or not.
        If valid then function returns string value, if not adds error to the message and returns None.
        :param data_dict: data passed from website in a form of dictionary.
        :param field_name: Fieldname of value to extract out of data dict.
        :return: string or None.
        """
        try:
            value = data_dict.pop(field_name, '')[0]
            if self._is_string_valid(value):
                return value
            else:
                self.message += 'Value in '+field_name+' shouldn\'t be empty string or None\r\n'
                self.isValidData = False
        except:
            self.message += 'Failed to retrieve '+field_name+'\r\n'
            self.isValidData = False

    def _get_required_bool_field_value(self, data_dict, field_name):
        """
        Check's if value in a given fieldname out of data_dict is valid boolean value or not.
        If valid then function returns boolean value, if not adds error to the message and returns None.
        :param data_dict: data passed from website in a form of dictionary.
        :param field_name: Fieldname of value to extract out of data dict.
        :return: boolean or None
        """
        try:
            value = data_dict.pop(field_name, '')[0]
            if self._is_bool_valid(value):
                return self._string_to_bool(value)
            else:
                self.message += 'Value in '+field_name+' can be either \'True\' or \'False\'\r\n'
                self.isValidData = False
        except:
            self.message += 'Failed to retrieve ' + field_name + '\r\n'
            self.isValidData = False

    def _get_required_integer_field_value(self, data_dict, field_name):
        """
        Check's if value in a given fieldname out of data_dict is valid int value or not.
        If valid then function returns int number, if not adds error to the message and returns None.
        :param data_dict: data passed from website in a form of dictionary.
        :param field_name: Fieldname of value to extract out of data dict.
        :return: int or None.
        """
        try:
            value = data_dict.pop(field_name, '')[0]
            if value.isdigit():
                return int(value)
            else:
                self.message += 'Value in '+field_name+' must be an integer\r\n'
                self.isValidData = False
        except:
            self.message += 'Failed to retrieve ' + field_name + '\r\n'
            self.isValidData = False

    def _get_required_decimal_field_value(self, data_dict, field_name):
        """
        Check's if value in a given fieldname out of data_dict is valid decimal value or not.
        If valid then function returns float number, if not adds error to the message and returns None.
        :param data_dict: data passed from website in a form of dictionary.
        :param field_name: Fieldname of value to extract out of data dict.
        :return: float or None.
        """
        try:
            value = data_dict.pop(field_name, '')[0]
            value = value.replace(',', '.')
            if value.replace('.', '', 1).isdigit():
                return float(value)
            else:
                self.message += 'Value in '+field_name+'  should be decimal number. Not empty string or None\r\n'
                self.isValidData = False
        except:
            self.message += 'Failed to retrieve ' + field_name + '\r\n'
            self.isValidData = False

    def _string_to_bool(self, string):
        """
        Returns True or False based on which boolean value is represented in string.
        True - 'true', '1', 't', 'y', 'yes'
        False - 'false', '0', 'n', 'f', 'no'
        :param string: bool in a form as string
        :return: True/False.
        """
        if string.lower() in ['true', '1', 't', 'y', 'yes']:
            return True
        if string.lower() in ['false', '0', 'n', 'f', 'no']:
            return False

    def _is_bool_valid(self, string):
        """
        If string fits into possible_values returns True, else False.
        :param string: String to check if fits in possible_values.
        :return: True/False.
        """
        possible_values = ['true', '1', 't', 'y', 'yes', 'false', '0', 'n', 'f', 'no']
        return string.lower() in possible_values

    def _is_string_valid(self, string):
        """
        If string is empty or it's none as lowercase it will return False, otherwise True.
        :param string: String to check.
        :return: True/False.
        """
        return not (string == '' or string.lower() == 'none')


class ChargerSerialEditor:

    def __init__(self, data):
        self.index = data['Index']
        self.serial = data['Serial']

    def process(self):
        charger = Chargers.objects.get(charger_id=self.index)
        charger.charger_serial = self.serial
        charger.save()


class ChargerSingleSerialPrinter:

    def __init__(self, data):
        self.full_serial = self._form_serial(data['Index'])
        self.base_url = 'http://192.168.8.254:8000/website/serial/'

    def _form_serial(self, int_index):
        charger = Chargers.objects.get(charger_id=int_index)
        manufacturer = charger.f_charger_category.f_manufacturer.manufacturer_name
        power = charger.f_charger_category.watts
        connector_type = charger.f_charger_category.connector_type
        serial = charger.charger_serial
        full_serial = manufacturer + '_' + str(power) + 'W' + connector_type + '_' + serial
        return full_serial

    def print(self):
        self.qr_gen = Qrgenerator(self.base_url, [self.full_serial])
        self.qr_gen.print_as_singular()


class ChargerDualSerialPrinter:

    def __init__(self, data):
        self.final_serials = []
        for member in data:
            full_serial = self._form_serial(data['Index'])
            self.final_serials.append(full_serial)
        self.base_url = 'http://192.168.8.254:8000/website/serial/'

    def _form_serial(self, int_index):
        charger = Chargers.objects.get(charger_id=int_index)
        manufacturer = charger.f_charger_category.f_manufacturer.manufacturer_name
        power = charger.f_charger_category.watts
        connector_type = charger.f_charger_category.connector_type
        serial = charger.charger_serial
        full_serial = manufacturer + '_' + str(power) + 'W' + connector_type + '_' + serial
        return full_serial

    def print(self):
        self.qr_gen = Qrgenerator(self.base_url, self.final_serials)
        self.qr_gen.print_as_pairs()


class ComputerSingleSerialPrinter:

    def __init__(self, int_index):
        self.full_serial = self._form_serial(int_index)
        self.base_url = 'http://192.168.8.254:8000/website/by_serial/'

    def _form_serial(self, int_index):
        computer = Computers.objects.get(id_computer=int_index)
        return computer.computer_serial

    def print(self):
        """
        In case one row should be printed print_as_singular() should be called.
        In case of two rows call print_as_pairs()
        """
        self.qr_gen = Qrgenerator(self.base_url, [self.full_serial])
        # self.qr_gen.print_as_pairs()
        self.qr_gen.print_as_singular()


class ComputerMultipleSerialPrinter:

    def __init__(self, data):
        self.final_serials = []
        for member in data:
            self.final_serials.append(self._form_serial(member))
        self.base_url = 'http://192.168.8.254:8000/website/by_serial/'

    def _form_serial(self, int_index):
        computer = Computers.objects.get(id_computer=int_index)
        return computer.computer_serial

    def print(self):
        """
        In case one row should be printed print_as_singular() should be called.
        In case of two rows call print_as_pairs()
        """
        self.qr_gen = Qrgenerator(self.base_url, self.final_serials)
        # self.qr_gen.print_as_pairs()
        self.qr_gen.print_as_singular()


class Qrgenerator:

    def __init__(self, base_url, serials):
        self.base_url = base_url
        self.serials = serials

    def print_as_pairs(self):
        for index in range(self._get_pair_cycles()):
            serial_pair = self._get_serial_pair(index)
            image = self._formImagePair(serial_pair[0], serial_pair[1])
            with tempfile.NamedTemporaryFile() as temp:
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                temp.write(img_byte_arr.getvalue())
                subprocess.call(['lpr', temp.name])

    def _get_pair_cycles(self):
        # Returns how many cycles of pairs of images should be done.
        # example: 1 serial=1cycle  2 serials=1 cycle, 3serials=2 cycles and so on.
        return math.ceil(len(self.serials) / 2)

    def _get_serial_pair(self, index):
        first = self.serials[index*2]
        try:
            second = self.serials[index*2+1]
        except IndexError:
            second = None
        return first, second

    def print_as_singular(self):
        print('print_as_singular')
        print(self.serials)
        for serial in self.serials:
            # image = self._formImagePair(serial, None)
            image = self._fromSerialToImage(serial)
            with tempfile.NamedTemporaryFile() as temp:
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                temp.write(img_byte_arr.getvalue())
                temp.flush()
                subprocess.call(['lpr', temp.name])

    def _generate_qr(self, serial):
        qr_img = qrcode.make(self.base_url + serial + '/')
        qr_img.thumbnail((410, 410), Image.ANTIALIAS)
        return qr_img

    def _formPrintableSerial(self, serial):
        if len(serial) > 7:
            return '..' + serial[-6:]
        return serial

    def _generateTxtImg(self, serial):
        textImg = Image.new('RGB', (410, 120), color=(255, 255, 255))
        fnt = ImageFont.truetype("VeraMono.ttf", size=48)
        drawer = ImageDraw.Draw(textImg)
        printableSerial = self._formPrintableSerial(serial).upper()
        w, h = drawer.textsize(printableSerial, font=fnt)
        drawer.text(((410 - w) / 2, -1), printableSerial, font=fnt, fill=(0, 0, 0))
        return textImg

    def _fromSerialToImage(self, serial):
        qrImg = self._generate_qr(serial)
        textImg = self._generateTxtImg(serial)
        image = Image.new('RGB', (350, 400), color=(255, 255, 255))
        image.paste(qrImg, (-30, -30))
        image.paste(textImg, (-30, 350))
        return image

    def _formImagePair(self, firstSerial, secondSerial=None):
        firstImage = self._fromSerialToImage(firstSerial)
        # margin is meant to determine how much additional space is added to the all sides of a image.
        # The idea is hat as dimensions of image increase printer resizes image during printing to fit to it's standard,
        # therefore dimensions of QR itself on the printed sticker decrease.
        margin = 10
        padding = 50
        heightDisplacement = -14
        width, height = firstImage.size
        pairImage = Image.new('RGB', (width + margin, int(height * 2) + 10 + (margin * 2) + padding),
                              color=(255, 255, 255))
        pairImage.paste(firstImage, (int(margin * 0.5), int(0 + (margin * 0.5) + heightDisplacement)))
        if secondSerial is not None:
            secondImage = self._fromSerialToImage(secondSerial)
            pairImage.paste(secondImage,
                            (int(margin * 0.5), int((width * 1.15) + margin + heightDisplacement) + padding))
        return pairImage

    def _sendToPrint(self, image):
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format='PNG')
        lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
        lpr.stdin.write(imgByteArr.getvalue())


class ChargerToDelete:

    def __init__(self, data):
        self.charger = Chargers.objects.get(charger_id=data['Index'])

    def delete(self):
        self.charger.delete()


class ChargerCategoryToDelete:

    def __init__(self, int_index):
        self.charger_category = ChargerCategories.objects.get(charger_category_id=int_index)
        self.message = ''
        self.success = False

    def delete(self):
        try:
            self.charger_category.delete()
            self.success = True
        except ProtectedError as e:
            self.success = False
            self.message += 'Failed to delete category:\r\n' + str(e)
        except IntegrityError as e:
            self.success = False
            self.message += 'Failed to delete category:\r\nMost probable cause is that category still has chargers in it\r\n' + str(e)


class HddOrderContentCsv:

    def __init__(self, int_index):
        self.order = HddOrder.objects.get(order_id=int_index)
        self.hdds = Drives.objects.filter(f_hdd_order=self.order).order_by('f_hdd_sizes__hdd_sizes_name', 'f_form_factor__form_factor_name')

    def createCsvFile(self):
        '''
        Since you can address those columns which have fieldnames, and there is a summary table which has no names,
        following rule is used:
        1) columns which should be created, but other than that contain nothing within them
        have empty string fieldname ''
        2) fieldnames which should not have header, but still can generate summary table have fieldnames out of spaces.
        ' ' one space simbolising first column
        '  ' two spaces simbolising second column
        '   ' three spaces simbolising third column
        3) columns which do have headers, have apropriate fieldnames to their headers.
        '''
        memfile = io.StringIO()
        fieldnames = ['', ' ', '  ', '   ', '', 'Serial number', 'Model', 'Size', 'Lock', 'Speed', 'Form factor', 'Health', 'Days on']
        writer = csv.DictWriter(memfile, fieldnames=fieldnames)
        writer.writeheader()
        for index in range(len(self.hdds)):
            hdd = self.hdds[index]
            triplet = self._get_aux_table_row(index)
            writer.writerow(
                {
                    ' ': triplet[0],
                    '  ': triplet[1],
                    '   ': triplet[2],
                    'Serial number': hdd.hdd_serial,
                    'Model': hdd.f_hdd_models.hdd_models_name,
                    'Size': hdd.f_hdd_sizes.hdd_sizes_name,
                    'Lock': hdd.f_lock_state.lock_state_name,
                    'Speed': hdd.f_speed.speed_name,
                    'Form factor': hdd.f_form_factor.form_factor_name,
                    'Health': hdd.health,
                    'Days on': hdd.days_on
                }
            )
        return memfile

    def _get_aux_table_row(self, index):
        if index == 0:
            return 'Date', 'Client', 'Order No'
        if index == 1:
            return self.order.date_of_order, '####', '####'
        if index == 3:
            return 'Drive size', 'Capacity', 'Quantity'
        if index > 3 and index <= 3 + self.hdds.values('f_hdd_sizes', 'f_form_factor').distinct().count():
            valuelist = self.hdds.values('f_hdd_sizes', 'f_form_factor').distinct()
            formfactor = FormFactor.objects.get(form_factor_id=valuelist[index-4]['f_form_factor'])
            hddsize = HddSizes.objects.get(hdd_sizes_id=valuelist[index-4]['f_hdd_sizes'])
            return formfactor.form_factor_name, hddsize.hdd_sizes_name, self.hdds.filter(f_hdd_sizes=hddsize, f_form_factor=formfactor).count()
        return '', '', ''


class OptionSelection:

    def __init__(self, title, tagname, content_list, search_method):
        self.title = title
        self.tagname = tagname
        self.content_list = content_list
        self.search_method = search_method

    def search(self, computers, lst):
        return self.search_method(computers, lst)


class SearchOptions:

    def __init__(self):
        self.options = []
        self.set_categories()
        self.set_statuses()

    def set_categories(self):
        def search_method(computers, lst):
            return computers.filter(f_category__category_name__in=lst)

        categories = Categories.objects.all().values_list('category_name', flat=True)
        category_selection = OptionSelection('Categories', 'cat', categories, search_method)
        self.options.append(category_selection)

    def set_statuses(self):
        no_status = 'No status'
        ordered = 'Ordered'
        sold = 'Sold'
        choices = [no_status, ordered, sold]

        def search_method(computers, lst):
            query = None
            if ordered in lst:
                query = Q(f_sale__isnull=True, f_id_comp_ord__isnull=False)
            if sold in lst:
                if not query:
                    query = Q(f_sale__isnull=False)
                else:
                    query = query | Q(f_sale__isnull=False)
            if no_status in lst:
                if not query:
                    query = Q(f_id_comp_ord__isnull=True, f_sale__isnull=True)
                else:
                    query = query | Q(f_id_comp_ord__isnull=True, f_sale__isnull=True)
            return computers.filter(query)

        statuses_selection = OptionSelection('Status', 'stat', choices, search_method)
        self.options.append(statuses_selection)


class Computer4th:

    def __init__(self, computer):
        print('this is Computer4th')
        self.version = 4
        self.computer = computer


    def collect_info(self):
        self.rc = RecordChoices()
        self.rams = get_rams(self.computer.id_computer)
        self.hdds = get_hdds(self.computer.id_computer)
        self.batts = get_batteries(self.computer.id_computer)
        self.received_batches = list(Receivedbatches.objects.all().values_list('received_batch_name', flat=True))
        self.received_batch = None
        if self.computer.f_id_received_batches != None:
            self.received_batch = self.computer.f_id_received_batches.received_batch_name

    def save_info(self, data_dict):

        def _save_sold_computer():
            print('saving sold computer')
            client = Clients.objects.get_or_create(client_name=data_dict.pop('client_name')[0])[0]
            sale = self.computer.f_sale
            sale.f_id_client = client
            sale.date_of_sale = data_dict.pop('date_of_sale')[0]
            sale.save()
            self.computer.f_type = type
            self.computer.f_category = category
            self.computer.f_manufacturer = manufacturer
            self.computer.f_model = model
            self.computer.f_cpu = cpu
            self.computer.f_gpu = gpu
            self.computer.f_ram_size = ram_size
            self.computer.f_hdd_size = hdd_size
            self.computer.f_diagonal = diagonal
            self.computer.f_license = license
            self.computer.f_camera = option
            self.computer.cover = data_dict.pop('cover')[0]
            self.computer.display = data_dict.pop('display')[0]
            self.computer.bezel = data_dict.pop('bezel')[0]
            self.computer.keyboard = data_dict.pop('keyboard')[0]
            self.computer.mouse = data_dict.pop('mouse')[0]
            self.computer.sound = data_dict.pop('sound')[0]
            self.computer.cdrom = data_dict.pop('cdrom')[0]
            self.computer.hdd_cover = data_dict.pop('hdd_cover')[0]
            self.computer.ram_cover = data_dict.pop('ram_cover')[0]
            self.computer.other = data_dict.pop('other')[0]
            self.computer.f_tester = tester
            self.computer.f_bios = bios
            self.computer.price = data_dict.pop('price')[0]
            if "received_batch_name" in data_dict and self.computer.f_id_received_batches is None:
                received_batch = Receivedbatches.objects.get(received_batch_name=data_dict["received_batch_name"])
                self.computer.f_id_received_batches = received_batch
            if data_dict['box_number']:
                self.computer.box_number = data_dict.pop('box_number')[0]
            self.computer.save()

        def _save_ordered_computer():
            print('saving ordered computer')
            self.computer.f_type = type
            self.computer.f_category = category
            self.computer.f_manufacturer = manufacturer
            self.computer.f_model = model
            self.computer.f_cpu = cpu
            self.computer.f_gpu = gpu
            self.computer.f_ram_size = ram_size
            self.computer.f_hdd_size = hdd_size
            self.computer.f_diagonal = diagonal
            self.computer.f_license = license
            self.computer.f_camera = option
            self.computer.cover = data_dict.pop('cover')[0]
            self.computer.display = data_dict.pop('display')[0]
            self.computer.bezel = data_dict.pop('bezel')[0]
            self.computer.keyboard = data_dict.pop('keyboard')[0]
            self.computer.mouse = data_dict.pop('mouse')[0]
            self.computer.sound = data_dict.pop('sound')[0]
            self.computer.cdrom = data_dict.pop('cdrom')[0]
            self.computer.hdd_cover = data_dict.pop('hdd_cover')[0]
            self.computer.ram_cover = data_dict.pop('ram_cover')[0]
            self.computer.other = data_dict.pop('other')[0]
            self.computer.f_tester = tester
            self.computer.f_bios = bios
            if "received_batch_name" in data_dict and self.computer.f_id_received_batches is None:
                received_batch = Receivedbatches.objects.get(received_batch_name=data_dict["received_batch_name"])
                self.computer.f_id_received_batches = received_batch
            if data_dict['box_number']:
                print("Passed box_number check")
                self.computer.box_number = data_dict.pop('box_number')[0]
            self.computer.save()

        def _save_stored_computer():
            print('saving stored computer')
            self.computer.f_type = type
            self.computer.f_category = category
            self.computer.f_manufacturer = manufacturer
            self.computer.f_model = model
            self.computer.f_cpu = cpu
            self.computer.f_gpu = gpu
            self.computer.f_ram_size = ram_size
            self.computer.f_hdd_size = hdd_size
            self.computer.f_diagonal = diagonal
            self.computer.f_license = license
            self.computer.f_camera = option
            self.computer.cover = data_dict.pop('cover')[0]
            self.computer.display = data_dict.pop('display')[0]
            self.computer.bezel = data_dict.pop('bezel')[0]
            self.computer.keyboard = data_dict.pop('keyboard')[0]
            self.computer.mouse = data_dict.pop('mouse')[0]
            self.computer.sound = data_dict.pop('sound')[0]
            self.computer.cdrom = data_dict.pop('cdrom')[0]
            self.computer.hdd_cover = data_dict.pop('hdd_cover')[0]
            self.computer.ram_cover = data_dict.pop('ram_cover')[0]
            self.computer.other = data_dict.pop('other')[0]
            self.computer.f_tester = tester
            self.computer.f_bios = bios
            if "received_batch_name" in data_dict and self.computer.f_id_received_batches is None:
                received_batch = Receivedbatches.objects.get(received_batch_name=data_dict["received_batch_name"])
                self.computer.f_id_received_batches = received_batch
            if data_dict['box_number']:
                print("Passed box_number check")
                self.computer.box_number = data_dict.pop('box_number')[0]
            self.computer.save()

        type = Types.objects.get_or_create(type_name=data_dict.pop('type_name')[0])[0]
        category = Categories.objects.get_or_create(category_name=data_dict.pop('category_name')[0])[0]
        manufacturer = Manufacturers.objects.get_or_create(manufacturer_name=data_dict.pop('manufacturer_name')[0])[0]
        model = Models.objects.get_or_create(model_name=data_dict.pop('model_name')[0])[0]
        cpu = Cpus.objects.get_or_create(cpu_name=data_dict.pop('cpu_name')[0])[0]
        print('Start of problematic section')
        gpu = Gpus.objects.get_or_create(gpu_name=data_dict.pop('gpu_name')[0])[0]
        print('End of problematic section')
        ram_size = RamSizes.objects.get_or_create(ram_size_text=data_dict.pop('ram_size_text')[0])[0]
        hdd_size = HddSizes.objects.get_or_create(hdd_sizes_name=data_dict.pop('hdd_sizes_name')[0])[0]
        diagonal = Diagonals.objects.get_or_create(diagonal_text=data_dict.pop('diagonal_text')[0])[0]
        license = Licenses.objects.get_or_create(license_name=data_dict.pop('license_name')[0])[0]
        option = CameraOptions.objects.get_or_create(option_name=data_dict.pop('option_name')[0])[0]
        tester = Testers.objects.get_or_create(tester_name=data_dict.pop('tester_name')[0])[0]
        bios = Bioses.objects.get_or_create(bios_text=data_dict.pop('bios_text')[0])[0]

        if self.computer.f_sale:
            _save_sold_computer()
        elif self.computer.f_id_comp_ord:
            _save_ordered_computer()
        else:
            _save_stored_computer()

    def delete(self):
        def try_to_delete(object):
            try:
                object.delete()
            except:
                pass
            
        print("This is 4th version's delete")
        for bat_to_comp in BatToComp.objects.filter(f_id_computer_bat_to_com=self.computer):
            bat = bat_to_comp.f_bat_bat_to_com
            try_to_delete(bat_to_comp)
            try_to_delete(bat)

        for hdd_to_comp in HddToComp.objects.filter(f_id_computer_hdd_to_com=self.computer):
            hdd = hdd_to_comp.f_id_hdd_hdd_to_com
            try_to_delete(hdd_to_comp)
            try_to_delete(hdd)

        for ram_to_comp in RamToComp.objects.filter(f_id_computer_ram_to_com=self.computer):
            ram = ram_to_comp.f_id_ram_ram_to_com
            try_to_delete(ram_to_comp)
            try_to_delete(ram)

        # gathering objects
        comp_ord = self.computer.f_id_comp_ord
        sale = self.computer.f_sale
        diagonal = self.computer.f_diagonal
        ramsize = self.computer.f_ram_size
        hddsize = self.computer.f_hdd_size
        cpu = self.computer.f_cpu
        model = self.computer.f_model

        # objects deletion
        try_to_delete(self.computer)
        try_to_delete(comp_ord)
        try_to_delete(sale)
        try_to_delete(diagonal)
        try_to_delete(ramsize)
        try_to_delete(hddsize)
        try_to_delete(cpu)
        try_to_delete(model)


class Computer5th:

    def __init__(self, computer):
        print('this is Computer5th')
        self.version = 5
        self.computer = computer

    def collect_info(self):
        def _get_rams():
            ram_to_comp = RamToComp.objects.filter(f_id_computer_ram_to_com=self.computer)
            rams = []
            for member in ram_to_comp:
                rams.append(member.f_id_ram_ram_to_com)
            return rams

        def _get_drives():
            computer_drives = Computerdrives.objects.filter(f_id_computer=self.computer)
            drives = []
            for member in computer_drives:
                drives.append(member.f_drive)
            return drives

        def _get_batteries():
            bat_to_comp = BatToComp.objects.filter(f_id_computer_bat_to_com=self.computer)
            batteries = []
            for member in bat_to_comp:
                batteries.append(member.f_bat_bat_to_com)
            return batteries

        def _get_processors():
            computer_processors = Computerprocessors.objects.filter(f_id_computer=self.computer)
            processors = []
            for member in computer_processors:
                processors.append(member.f_id_processor)
            return processors

        def _get_gpus():
            computer_gpus = Computergpus.objects.filter(f_id_computer=self.computer)
            gpus = []
            for member in computer_gpus:
                gpus.append(member.f_id_gpu)
            return gpus

        def _get_observations():
            computer_observations = Computerobservations.objects.filter(f_id_computer=self.computer)
            observations = []
            for member in computer_observations:
                observations.append(member.f_id_observation)
            return observations

        self.rc = RecordChoices()
        self.rams = _get_rams()
        self.drives = _get_drives()
        self.batteries = _get_batteries()
        self.processors = _get_processors()
        self.gpus = _get_gpus()
        self.observations = _get_observations()
        self.received_batches = list(Receivedbatches.objects.all().values_list('received_batch_name', flat=True))
        self.received_batch = None
        if self.computer.f_id_received_batches != None:
            self.received_batch = self.computer.f_id_received_batches.received_batch_name


    def save_info(self, data_dict):
        def _save_sold_computer():
            print('saving sold computer')
            client = Clients.objects.get_or_create(client_name=data_dict.pop('client_name')[0])[0]
            sale = self.computer.f_sale
            sale.f_id_client = client
            sale.date_of_sale = data_dict.pop('date_of_sale')[0]
            sale.save()
            self.computer.price = data_dict.pop('price')[0]
            self.computer.f_type = type
            self.computer.f_category = category
            self.computer.f_manufacturer = manufacturer
            self.computer.f_model = model
            self.computer.f_ram_size = ram_size
            self.computer.f_diagonal = diagonal
            self.computer.f_license = license
            self.computer.f_camera = option
            self.computer.f_tester = tester
            self.computer.f_diagonal = diagonal
            self.computer.f_id_computer_resolutions = computer_resolutions
            self.computer.other = data_dict.pop('other')[0]
            if "received_batch_name" in data_dict and self.computer.f_id_received_batches is None:
                received_batch = Receivedbatches.objects.get(received_batch_name=data_dict["received_batch_name"])
                self.computer.f_id_received_batches = received_batch
            if data_dict['box_number']:
                self.computer.box_number = data_dict.pop('box_number')[0]
            self.computer.save()

        def _save_ordered_computer():
            print('saving ordered computer')
            self.computer.f_type = type
            self.computer.f_category = category
            self.computer.f_manufacturer = manufacturer
            self.computer.f_model = model
            self.computer.f_ram_size = ram_size
            self.computer.f_diagonal = diagonal
            self.computer.f_license = license
            self.computer.f_camera = option
            self.computer.f_tester = tester
            self.computer.f_diagonal = diagonal
            self.computer.f_id_computer_resolutions = computer_resolutions
            self.computer.other = data_dict.pop('other')[0]
            if "received_batch_name" in data_dict and self.computer.f_id_received_batches is None:
                received_batch = Receivedbatches.objects.get(received_batch_name=data_dict["received_batch_name"])
                self.computer.f_id_received_batches = received_batch
            if data_dict['box_number']:
                self.computer.box_number = data_dict.pop('box_number')[0]
            self.computer.save()

        def _save_stored_computer():
            print('saving stored computer')
            self.computer.f_type = type
            self.computer.f_category = category
            self.computer.f_manufacturer = manufacturer
            self.computer.f_model = model
            self.computer.f_ram_size = ram_size
            self.computer.f_diagonal = diagonal
            self.computer.f_license = license
            self.computer.f_camera = option
            self.computer.f_tester = tester
            self.computer.f_diagonal = diagonal
            self.computer.f_id_computer_resolutions = computer_resolutions
            self.computer.other = data_dict.pop('other')[0]
            if "received_batch_name" in data_dict and self.computer.f_id_received_batches is None:
                received_batch = Receivedbatches.objects.get(received_batch_name=data_dict["received_batch_name"])
                self.computer.f_id_received_batches = received_batch
            if data_dict['box_number']:
                self.computer.box_number = data_dict.pop('box_number')[0]
            self.computer.save()

        def _save_many_to_many():
            """
            Function responsible of handling many to many relationship record updating in database.
            Tables which records are updated: Rams, Batteries, Processors and Gpus.
            """
            def _get_unique_ids(object_dict):
                """
                :param object_dict: Dictionary item, having keys in a pattern 'entity_field_id'
                :return: list of unique ids
                """
                lst = []
                for keyx, valuex in object_dict.items():
                    object_id = keyx.split('_')[2]
                    if object_id not in lst:
                        lst.append(object_id)
                return lst

            def _save_rams():
                """
                Updates new values to Rams.
                If that Ram record is referenced somewhere else, those values change just as well.
                """
                for keyx, valuex in ram_dict.items():
                    if "ram_type" in keyx:
                        ram = Rams.objects.get(id_ram=keyx.split('_')[2])
                        ram.type = valuex
                        ram.save()

            def _save_batteries():
                """
                Updates new values to Batteries.
                If that Batteries record is referenced somewhere else, those values change just as well.
                """
                bat_ids = _get_unique_ids(bat_dict)

                for bat_id in bat_ids:
                    battery = Batteries.objects.get(id_battery=bat_id)
                    battery.wear_out = bat_dict["bat_wearout_" + str(bat_id)]
                    battery.expected_time = bat_dict["bat_expectedtime_" + str(bat_id)]
                    battery.model = bat_dict["bat_model_" + str(bat_id)]
                    battery.maximum_wh = bat_dict["bat_maximumwh_" + str(bat_id)]
                    battery.factory_wh = bat_dict["bat_factorywh_" + str(bat_id)]
                    battery.save()

            def _save_processors():
                """
                If Processors record is referenced more than once in Computerprocessors:
                    * Creates new record and changes computer reference to a new record with edited values in Processors.
                If Processors record is referenced only once in Computerprocessors and there is already Processors with
                provided new values:
                    * Reference that Processors record in Computerprocessors.
                If Processors record is referenced only once in Computerprocessors:
                    * Updates new values to Processors.
                """
                proc_ids = _get_unique_ids(proc_dict)
                for proc_id in proc_ids:
                    processor = Processors.objects.get(id_processor=proc_id)
                    count_of_computer_processors = Computerprocessors.objects.filter(f_id_processor=processor).count()
                    if not (processor.f_manufacturer.manufacturer_name == proc_dict[
                        "proc_manufacturername_" + str(proc_id)]
                            and processor.model_name == proc_dict["proc_modelname_" + str(proc_id)]
                            and processor.stock_clock == proc_dict["proc_stockclock_" + str(proc_id)]
                            and processor.max_clock == proc_dict["proc_maxclock_" + str(proc_id)]
                            and processor.cores == int(proc_dict["proc_cores_" + str(proc_id)])
                            and processor.threads == int(proc_dict["proc_threads_" + str(proc_id)])):
                        manufacturer = Manufacturers.objects.get_or_create(
                            manufacturer_name=proc_dict["proc_manufacturername_" + str(proc_id)])[0]
                        if count_of_computer_processors > 1:
                            Computerprocessors.objects.get(
                                f_id_computer=self.computer,
                                f_id_processor=processor
                            ).delete()
                            new_processor = Processors.objects.get_or_create(
                                f_manufacturer=manufacturer,
                                model_name=proc_dict["proc_modelname_" + str(proc_id)],
                                stock_clock=proc_dict["proc_stockclock_" + str(proc_id)],
                                max_clock=proc_dict["proc_maxclock_" + str(proc_id)],
                                cores=int(proc_dict["proc_cores_" + str(proc_id)]),
                                threads=int(proc_dict["proc_threads_" + str(proc_id)])
                            )[0]
                            Computerprocessors.objects.get_or_create(
                                f_id_computer=self.computer,
                                f_id_processor=new_processor
                            )
                        elif count_of_computer_processors == 1:
                            try:
                                existing_processor = Processors.objects.get(
                                    f_manufacturer=manufacturer,
                                    model_name=proc_dict["proc_modelname_" + str(proc_id)],
                                    stock_clock=proc_dict["proc_stockclock_" + str(proc_id)],
                                    max_clock=proc_dict["proc_maxclock_" + str(proc_id)],
                                    cores=int(proc_dict["proc_cores_" + str(proc_id)]),
                                    threads=int(proc_dict["proc_threads_" + str(proc_id)]),
                                )
                                computer_processor = Computerprocessors.objects.get(
                                    f_id_computer=self.computer,
                                    f_id_processor=processor
                                )
                                computer_processor.f_id_processor = existing_processor
                                computer_processor.save()
                                processor.delete()
                            except Processors.DoesNotExist:
                                processor.f_manufacturer = manufacturer
                                processor.model_name = proc_dict["proc_modelname_" + str(proc_id)]
                                processor.stock_clock = proc_dict["proc_stockclock_" + str(proc_id)]
                                processor.max_clock = proc_dict["proc_maxclock_" + str(proc_id)]
                                processor.cores = int(proc_dict["proc_cores_" + str(proc_id)])
                                processor.threads = int(proc_dict["proc_threads_" + str(proc_id)])
                                processor.save()

            def _save_gpus():
                """
                If Gpus record is referenced more than once in Computergpus:
                    * Creates new record and changes computer reference to a new record with edited values in Gpus.
                If Gpus record is referenced only once in Computergpus and there is already Gpus with
                provided new values:
                    * Reference that Gpus record in Computergpus.
                If Gpus record is referenced only once in Computergpus:
                    * Updates new values to Gpus.
                """
                gpu_ids = _get_unique_ids(gpu_dict)
                for gpu_id in gpu_ids:
                    gpu = Gpus.objects.get(id_gpu=gpu_id)
                    count_of_computer_gpus = Computergpus.objects.filter(f_id_gpu=gpu).count()
                    if not (gpu.f_id_manufacturer.manufacturer_name == gpu_dict["gpu_manufacturername_" + str(gpu_id)]
                        and gpu.gpu_name == gpu_dict["gpu_gpuname_" + str(gpu_id)]):
                        manufacturer = Manufacturers.objects.get_or_create(
                            manufacturer_name=gpu_dict["gpu_manufacturername_" + str(gpu_id)])[0]
                        if count_of_computer_gpus > 1:
                            Computergpus.objects.get(
                                f_id_gpu=gpu,
                                f_id_computer=self.computer
                            ).delete()
                            new_gpu = Gpus.objects.get_or_create(
                                gpu_name=gpu_dict["gpu_gpuname_" + str(gpu_id)],
                                f_id_manufacturer=manufacturer
                            )[0]
                            Computergpus.objects.get_or_create(
                                f_id_gpu=new_gpu,
                                f_id_computer=self.computer
                            )
                        elif count_of_computer_gpus == 1:
                            try:
                                existing_gpu = Gpus.objects.get(
                                    f_id_manufacturer=manufacturer,
                                    gpu_name=gpu_dict["gpu_gpuname_" + str(gpu_id)]
                                )
                                computer_gpu = Computergpus.objects.get(f_id_gpu=gpu, f_id_computer=self.computer)
                                computer_gpu.f_id_gpu = existing_gpu
                                computer_gpu.save()
                                gpu.delete()
                            except Gpus.DoesNotExist:
                                gpu.f_id_manufacturer = manufacturer
                                gpu.gpu_name = gpu_dict["gpu_gpuname_" + str(gpu_id)]
                                gpu.save()

            ram_dict = {}
            bat_dict = {}
            proc_dict = {}
            gpu_dict = {}
            for key, value in data_dict.items():
                if 'ram' in key:
                    ram_dict[key] = value
                elif 'bat' in key:
                    bat_dict[key] = value
                elif 'proc' in key:
                    proc_dict[key] = value
                elif 'gpu' in key:
                    gpu_dict[key] = value
            _save_rams()
            _save_batteries()
            _save_processors()
            _save_gpus()

        type = Types.objects.get_or_create(type_name=data_dict.pop('type_name')[0])[0]
        category = Categories.objects.get_or_create(category_name=data_dict.pop('category_name')[0])[0]
        manufacturer = Manufacturers.objects.get_or_create(manufacturer_name=data_dict.pop('manufacturer_name')[0])[0]
        model = Models.objects.get_or_create(model_name=data_dict.pop('model_name')[0])[0]
        ram_size = RamSizes.objects.get_or_create(ram_size_text=data_dict.pop('ram_size_text')[0])[0]
        tester = Testers.objects.get_or_create(tester_name=data_dict.pop('tester_name')[0])[0]
        license = Licenses.objects.get_or_create(license_name=data_dict.pop('license_name')[0])[0]
        option = CameraOptions.objects.get_or_create(option_name=data_dict.pop('option_name')[0])[0]
        diagonal = Diagonals.objects.get_or_create(diagonal_text=data_dict.pop('diagonal_text')[0])[0]
        resolution = Resolutions.objects.get_or_create(resolution_text=data_dict.pop('resolution_text')[0])[0]
        resolution_category = Resolutioncategories.objects.get_or_create(resolution_category_name=data_dict.pop('resolution_category_text')[0])[0]
        computer_resolutions = Computerresolutions.objects.get_or_create(
            f_id_resolution=resolution,
            f_id_resolution_category=resolution_category
        )[0]

        if self.computer.f_sale:
            _save_sold_computer()
        elif self.computer.f_id_comp_ord:
            _save_ordered_computer()
        else:
            _save_stored_computer()
        _save_many_to_many()

    def delete(self):

        def try_to_delete(object):
            try:
                object.delete()
            except:
                pass

        print("This is 5th version's delete")
        for bat_to_comp in BatToComp.objects.filter(f_id_computer_bat_to_com=self.computer):
            bat = bat_to_comp.f_bat_bat_to_com
            try_to_delete(bat_to_comp)
            try_to_delete(bat)

        for ram_to_comp in RamToComp.objects.filter(f_id_computer_ram_to_com=self.computer):
            ram = ram_to_comp.f_id_ram_ram_to_com
            try_to_delete(ram_to_comp)
            try_to_delete(ram)

        for computer_drive in Computerdrives.objects.filter(f_id_computer=self.computer):
            drive = computer_drive.f_drive
            try_to_delete(computer_drive)
            try_to_delete(drive)

        for computer_processor in Computerprocessors.objects.filter(f_id_computer=self.computer):
            processor = computer_processor.f_id_processor
            try_to_delete(computer_processor)
            try_to_delete(processor)

        for computer_gpu in Computergpus.objects.filter(f_id_computer=self.computer):
            gpu = computer_gpu.f_id_gpu
            try_to_delete(computer_gpu)
            try_to_delete(gpu)

        for computer_observation in Computerobservations.objects.filter(f_id_computer=self.computer):
            try_to_delete(computer_observation)

        # gathering objects
        computer_resolution = self.computer.f_id_computer_resolutions
        resolution = computer_resolution.f_id_resolution
        resolution_category = computer_resolution.f_id_resolution_category
        sale = self.computer.f_sale
        comp_ord = self.computer.f_id_comp_ord
        matrix = self.computer.f_id_matrix
        cable_type = matrix.f_id_cable_type

        # objects deletion
        try_to_delete(self.computer)
        try_to_delete(computer_resolution)
        try_to_delete(resolution)
        try_to_delete(resolution_category)
        try_to_delete(sale)
        try_to_delete(comp_ord)
        try_to_delete(matrix)
        try_to_delete(cable_type)


class ComputerToEdit:

    def __init__(self, int_index=None, serial=None):
        print('ComputerToEdit constructor')
        if int_index:
            self.computer = Computers.objects.get(id_computer=int_index)
        elif serial:
            self.computer = Computers.objects.get(computer_serial=serial)
        else:
            raise Exception("Neither index, nor serial were passed to ComputerToEdit class.")
        self.message = ''

    def success(self):
        return self.message == ''

    def process_post(self, data_dict):
        print('Processing post request')
        data_dict.pop('edit.x')
        data_dict.pop('edit.y')
        data_dict.pop('id_computer')
        data_dict.pop('serial')
        data_dict.pop('motherboard_serial')
        data_dict.pop('date')
        if self._is5thVersion(self.computer):
            print('Computer is of 5th version')
            try:
                self.record = Computer5th(computer=self.computer)
                self.record.save_info(data_dict)
            except Exception as e:
                ex_type, ex, tb = sys.exc_info()
                self.message = str(e.with_traceback(tb))
        else:
            print('Computer is of 4th version')
            try:
                self.record = Computer4th(computer=self.computer)
                self.record.save_info(data_dict)
            except Exception as e:
                ex_type, ex, tb = sys.exc_info()
                self.message = str(e.with_traceback(tb))
        
    def process_get(self):
        print('Processing get request')
        if self._is5thVersion(self.computer):
            print('Computer is of 5th version')
            self.record = Computer5th(computer=self.computer)
            self.record.collect_info()
        else:
            print('Computer is of 4th version')
            self.record = Computer4th(computer=self.computer)
            self.record.collect_info()

    def delete_record(self):
        print('Processing delete request')
        if self._is5thVersion(self.computer):
            print('Computer is of 5th version')
            self.record = Computer5th(computer=self.computer)
            self.record.delete()
        else:
            print('Computer is of 4th version')
            self.record = Computer4th(computer=self.computer)
            self.record.delete()

    def _is5thVersion(self, computer):
        return computer.f_id_computer_resolutions \
                or computer.f_id_matrix \
                or Computerprocessors.objects.filter(f_id_computer=computer).count() > 0 \
                or Computergpus.objects.filter(f_id_computer=computer).count() > 0 \
                or Computerobservations.objects.filter(f_id_computer=computer).count() > 0 \
                or Computerdrives.objects.filter(f_id_computer=computer).count() > 0


def get_query_for_computer_search_from_order_edit(query_string):
    """
    Forms Q query to be used with filter() models method.
    Used for creating search from order edit.
    :param query_string: searchable string string collection in form of string
    :return: Q object.
    """
    searchfields = (
        'computer_serial',
        'f_model__model_name',
        'f_manufacturer__manufacturer_name'
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
    return query & Q(f_id_comp_ord__isnull=True, f_sale__isnull=True)
