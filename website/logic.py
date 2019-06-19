from ULCDTinterface.modelers import *
import xlsxwriter
from django.utils import timezone
import re
from django.db.models import Q, Count
from django.conf import settings
import os
import tarfile
import csv
import qrcode
from PIL import Image, ImageDraw, ImageFont
import subprocess
import io
import tempfile
import math
import sys
from abc import ABC
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.utils import IntegrityError
from django.core.paginator import Paginator
from datetime import datetime


class TypCatComputersLogic:

    def __init__(self, data_dict):
        pass


class SoldComputersLogic:

    def __init__(self, data_dict):
        pass


class SearchComputersLogic:
    """
    Not finnished supposed to lower ammount of code in views.py search_view()
    """

    def __init__(self, data_dict):
        self.qty = int(data_dict.get('qty', 10))
        self.page = int(data_dict.get('page', 1))
        computers = Computers.objects.all()
        computers = search(data_dict.get('keyword', None), computers)
        self.so = SearchOptions()
        for option in self.so.options:
            computers = option.search(computers, data_dict.get(option.tagname, ""))
        autoFilters = AutoFilter(data_dict)
        computers = autoFilters.filter(computers)
        self.qtySelect = QtySelect()
        self.qtySelect.setDefaultSelect(self.qty)
        self.af = AutoFiltersFromComputers(computers)
        paginator = Paginator(computers, self.qty)
        self.computers = paginator.get_page(self.page)
        # self.counter = Counter()
        # self.counter.count = qty * (page - 1)
        self.index = self.start_index = self.qty * (self.page - 1)

    def isGlobal(self):
        return True

    def poscat(self):
        return Categories.objects.values_list('category_name', flat=True)

    def typcat(self):
        return TypCat()

    '''
    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= self.qty * self.page:
            self.index = self.qty * (self.page - 1)
            raise StopIteration
        else:
            self.index += 1
            # print(self.index - self.start_index)
            print(type(self.computers))
            # return self.computers[self.index - self.start_index]
            # return next(self.computers)
    '''
    def get_computers(self):
        return self.computers


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
        self.qty = qty
        if qty == 10:
            self.state10 = "selected"
        elif qty == 20:
            self.state20 = "selected"
        elif qty == 50:
            self.state50 = "selected"
        elif qty == 100:
            self.state100 = "selected"
        elif qty == 200:
            self.state200 = "selected"
        elif qty == 1000:
            self.state1000 = "selected"


class QtySelect2:
    qty = 0
    state10 = ""
    state20 = ""
    state50 = ""
    state100 = ""
    state200 = ""

    def __init__(self, qty):
        self.qty = qty
        if qty == 10:
            self.state10 = "selected"
        elif qty == 20:
            self.state20 = "selected"
        elif qty == 50:
            self.state50 = "selected"
        elif qty == 100:
            self.state100 = "selected"
        elif qty == 200:
            self.state200 = "selected"
        elif qty == 1000:
            self.state1000 = "selected"


class FilterUnit:

    def __init__(self, name, qty):
        self.name = name
        self.qty = qty

    def __str__(self):
        return 'Name: {0}, Qty: {1}'.format(self.name, self.qty)


class AutoFiltersFromComputers:
    """
    This is a holder of unique values necessary for filtering operations website side.
    """

    def __init__(self, computers):
        self.computers = computers
        self.serials = computers.values_list('computer_serial', flat=True).distinct().order_by('computer_serial')

    def manufacturers(self):
        return self._many_to_one_getter(field_name='f_manufacturer__manufacturer_name')

    def models(self):
        return self._many_to_one_getter(field_name='f_model__model_name')

    def rams(self):
        return self._many_to_one_getter(field_name='f_ram_size__ram_size_text')

    def screens(self):
        return self._many_to_one_getter(field_name='f_diagonal__diagonal_text')

    def form_factors(self):
        return self._many_to_one_getter(field_name='f_id_computer_form_factor__form_factor_name')

    def testers(self):
        return self._many_to_one_getter(field_name='f_tester__tester_name')

    def others(self):
        observation_names = Observations.objects.filter(
            id_observation__in=Computerobservations.objects.filter(
                f_id_computer__in=self.computers
            ).values_list('f_id_observation', flat=True).distinct().order_by('f_id_observation')
        ).values_list('full_name', flat=True).distinct().order_by('full_name')
        for observation_name in observation_names:
            qty = Computerobservations.objects.filter(
                f_id_computer__in=self.computers,
                f_id_observation__full_name=observation_name
            ).count()
            yield FilterUnit(name=observation_name, qty=qty)

    def _many_to_one_getter(self, field_name):
        names = self.computers.exclude(
            **{field_name: None}
        ).values_list(field_name, flat=True).distinct().order_by(field_name)

        for name in names:
            qty = self.computers.filter(**{field_name: name}).count()
            yield FilterUnit(name=name, qty=qty)
    
    def cpus(self):
        return self._cpu_gpu_getter(
            field_name='f_id_processor__model_name',
            model=Computerprocessors
        )

    def gpus(self):
        return self._cpu_gpu_getter(
            field_name='f_id_gpu__gpu_name',
            model=Computergpus
        )

    def statuses(self):
        status_filters = []
        for computer in self.computers:
            isAdded = False
            computer_status = computer.get_status()
            for filter in status_filters:
                if filter.name == computer_status:
                    filter.qty += 1
                    isAdded = True
            if not isAdded:
                status_filters.append(FilterUnit(name=computer_status, qty=1))
        return status_filters

    def _cpu_gpu_getter(self, field_name, model):
        names = model.objects.exclude(**{field_name: ''}).filter(
            f_id_computer__in=self.computers
        ).values_list(field_name, flat=True).distinct().order_by(field_name)
        for name in names:
            qty = model.objects.filter(**{field_name: name, 'f_id_computer__in': self.computers}).count()
            yield FilterUnit(name=name, qty=qty)


class AutoFiltersFromSoldComputers(AutoFiltersFromComputers):
    """
    This is a holder's extension of AutoFiltersFromComputers to accommodate for sold computers additional choices.
    """

    def __init__(self, computers):
        super(AutoFiltersFromSoldComputers, self).__init__(computers)
        
    def prices(self):
        return self._many_to_one_getter(field_name='price')

    def dates(self):
        return self._many_to_one_getter(field_name='f_sale__date_of_sale')

    def clients(self):
        return self._many_to_one_getter(field_name='f_sale__f_id_client__client_name')


class TypCat:
    """
    Represents types with categories in submenu for website's navigational menu generation.
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
        """
        This method is responsible of forming csv/excel file
        computer's other column value of 5th version computer structure.

        :param computer: computer model's object.
        :return: fully formed comment string about a computer.
        """
        commentToReturn = ''
        computer_observations = Computerobservations.objects.filter(f_id_computer=computer)
        categories = computer_observations.values_list('f_id_observation__f_id_observation_category', flat=True)
        categories = list(set(categories))
        for category_id in categories:
            observations_of_category = computer_observations.filter(
                f_id_observation__f_id_observation_category=category_id)
            category_name = Observationcategory.objects.get(id_observation_category=category_id).category_name
            string_to_add = category_name + ": "
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
            lst = []
            for computer_processor in Computerprocessors.objects.filter(f_id_computer=computer):
                string = computer_processor.f_id_processor.f_manufacturer.manufacturer_name + ' ' + computer_processor.f_id_processor.model_name + ' ' + computer_processor.f_id_processor.stock_clock
                lst.append(string)
            return ', '.join(lst).replace('Intel Intel', 'Intel').replace(' GHz', '')
        except:
            return "N/A"

    @staticmethod
    def _get_ram_size(computer):
        try:
            ram_to_comp = RamToComp.objects.filter(f_id_computer_ram_to_com=computer)[0]
            return computer.f_ram_size.ram_size_text + ' ' + ram_to_comp.f_id_ram_ram_to_com.type
        except:
            return "N/A"

    @staticmethod
    def _get_gpu_name(computer):
        try:
            lst = []
            for computer_gpu in Computergpus.objects.filter(f_id_computer=computer):
                string = computer_gpu.f_id_gpu.f_id_manufacturer.manufacturer_name + ' ' + computer_gpu.f_id_gpu.gpu_name
                if 'Intel HD' in string:
                    string = 'Intel HD'
                lst.append(string)
            return ', '.join(lst)
        except:
            return "N/A"

    @staticmethod
    def _get_hdd_size(computer):
        try:
            lst = []
            for computer_drive in Computerdrives.objects.filter(f_id_computer=computer):
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
        except:
            return "N/A"

    @staticmethod
    def atleast_one_desktop(indexes):
        for index in indexes:
            if Computers.objects.get(id_computer=index).f_type.type_name.lower() == 'desktop':
                return True
        return False

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

    @staticmethod
    def _get_box_no(computer):
        try:
            return computer.box_number
        except:
            return "N/A"

    @staticmethod
    def _get_computer_form_factor(computer):
        try:
            return computer.f_id_computer_form_factor.form_factor_name
        except:
            return ''


class ExcelGenerator(AbstractDataFileGenerator):

    def __init__(self):
        self.memfile = io.BytesIO()
        super().__init__()

    def generate_desktop_file(self, indexes, worksheet, bold_bordered, bordered):
        print('generate_desktop_file')
        worksheet.write("A1", "S/N", bold_bordered)
        worksheet.write("B1", "Form factor", bold_bordered)
        worksheet.write("C1", "Manufacturer", bold_bordered)
        worksheet.write("D1", "Model", bold_bordered)
        worksheet.write("E1", "CPU", bold_bordered)
        worksheet.write("F1", "RAM", bold_bordered)
        worksheet.write("G1", "GPU", bold_bordered)
        worksheet.write("H1", "HDD", bold_bordered)
        worksheet.write("I1", "Optical", bold_bordered)
        worksheet.write("J1", "COA", bold_bordered)
        worksheet.write("K1", "Comment", bold_bordered)
        worksheet.write("L1", "Price", bold_bordered)
        worksheet.write("M1", "Box no.", bold_bordered)
        row = 1
        col = 0
        for int_index in indexes:
            computer = Computers.objects.get(id_computer=int_index)
            worksheet.write(row, col, self._get_serial(computer), bordered)
            worksheet.write(row, col + 1, self._get_computer_form_factor(computer), bordered)
            worksheet.write(row, col + 2, self._get_manufacturer(computer), bordered)
            worksheet.write(row, col + 3, self._get_model(computer), bordered)
            worksheet.write(row, col + 4, self._get_cpu_name(computer), bordered)
            worksheet.write(row, col + 5, self._get_ram_size(computer), bordered)
            worksheet.write(row, col + 6, self._get_gpu_name(computer), bordered)
            worksheet.write(row, col + 7, self._get_hdd_size(computer), bordered)
            worksheet.write(row, col + 8, self._get_cdrom(computer), bordered)
            worksheet.write(row, col + 9, self._get_license(computer), bordered)
            worksheet.write(row, col + 10, self._form_comment(computer), bordered)
            worksheet.write(row, col + 11, '', bordered)
            worksheet.write(row, col + 12, computer.box_number, bordered)
            row += 1

    def generate_laptop_file(self, indexes, worksheet, bold_bordered, bordered):
        print('generate_laptop_file')
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
        worksheet.write("O1", "Box no.", bold_bordered)
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
            worksheet.write(row, col + 12, self._form_comment(computer), bordered)
            worksheet.write(row, col + 13, '', bordered)
            worksheet.write(row, col + 14, computer.box_number, bordered)
            row += 1

    def generate_file(self, indexes):
        workbook = xlsxwriter.Workbook(self.memfile)
        worksheet = workbook.add_worksheet()
        bold_bordered = workbook.add_format({"bold": True, "border": 1})
        bordered = workbook.add_format({"border": 1})

        if self.atleast_one_desktop(indexes):
            self.generate_desktop_file(indexes, worksheet, bold_bordered, bordered)
        else:
            self.generate_laptop_file(indexes, worksheet, bold_bordered, bordered)
        workbook.close()
        return self.memfile


class CsvGenerator(AbstractDataFileGenerator):

    def __init__(self):
        self.memfile = io.StringIO()
        super().__init__()
        self.laptop_fieldnames = ["S/N", 'Manufacturer', 'Model', 'CPU', 'RAM', 'GPU', 'HDD', 'Batteries', 'LCD', 'Optical',
                           'COA', 'Cam', 'Comment', 'Price', 'Box no.']
        self.desktop_fieldnames = ["S/N", "Form factor", 'Manufacturer', 'Model', 'CPU', 'RAM', 'GPU', 'HDD', 'Optical',
                                  'COA', 'Comment', 'Price', 'Box no.']

    def generate_desktop_file(self, indexes):
        print('generate_desktop_file')
        writer = csv.DictWriter(self.memfile, fieldnames=self.desktop_fieldnames)
        writer.writeheader()
        for int_index in indexes:
            computer = Computers.objects.get(id_computer=int_index)
            writer.writerow({
                "S/N": self._get_serial(computer),
                "Form factor": self._get_computer_form_factor(computer),
                'Manufacturer': self._get_manufacturer(computer),
                'Model': self._get_model(computer),
                'CPU': self._get_cpu_name(computer),
                'RAM': self._get_ram_size(computer),
                'GPU': self._get_gpu_name(computer),
                'HDD': self._get_hdd_size(computer),
                'Optical': self._get_cdrom(computer),
                'COA': self._get_license(computer),
                'Comment': self._form_comment(computer),
                'Price': '',
                'Box no.': computer.box_number,
            })

    def generate_laptop_file(self, indexes):
        print('generate_laptop_file')
        writer = csv.DictWriter(self.memfile, fieldnames=self.laptop_fieldnames)
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
                'Comment': self._form_comment(computer),
                'Price': '',
                'Box no.': computer.box_number,
            })

    def generate_file(self, indexes):
        if self.atleast_one_desktop(indexes):
            self.generate_desktop_file(indexes)
        else:
            self.generate_laptop_file(indexes)
        return self.memfile


class Item:

    def __init__(self, item_id, item_name, permanence=0):
        self.id = item_id
        self.name = item_name
        self.permanence = bool(permanence)


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
        Observations.objects.get_or_create(
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
        Saves computer record sent using website's querydict
        """
        # If empty string is passed as form_factor in queryset it should be interpreted as None.
        computer_form_factor = None
        if self.data['form_factor']:
            computer_form_factor = ComputerFormFactors.objects.get(form_factor_name=self.data.get('form_factor'))
        computer = Computers.objects.create(
            computer_serial=self.data.get('serial'),
            box_number=self.data.get('box_number'),
            other=self.data.get('other'),
            f_type=Types.objects.get_or_create(type_name=self.data.get('type_name'))[0],
            f_category=Categories.objects.get_or_create(category_name=self.data.get('category_name'))[0],
            f_manufacturer=Manufacturers.objects.get_or_create(manufacturer_name=self.data.get('manufacturer_name'))[0],
            f_model=Models.objects.get_or_create(model_name=self.data.get('model_name'))[0],
            f_tester=Testers.objects.get_or_create(tester_name=self.data.get('tester_name'))[0],
            f_license=Licenses.objects.get_or_create(license_name=self.data.get('license_name'))[0],
            f_id_received_batches=Receivedbatches.objects.get_or_create(
                received_batch_name=self.data.get('received_batch_name')
            )[0],
            f_diagonal=Diagonals.objects.get_or_create(diagonal_text=self.data.get('diagonal_text'))[0],
            f_ram_size=RamSizes.objects.get_or_create(ram_size_text=self.data.get('ram_size_text'))[0],
            f_camera=CameraOptions.objects.get_or_create(option_name="Not tested")[0],
            f_id_computer_form_factor=computer_form_factor,
        )
        self._many_to_many_connection_save(computer)

    def _many_to_many_connection_save(self, computer):
        def _form_main_dict():
            new_ramsticks_dict = {}
            existing_ramsticks_list = []
            new_processors_dict = {}
            existing_processors_list = []
            new_gpus_dict = {}
            existing_gpus_list = []
            existing_observations_list = []

            for key, value in self.data.items():
                if "newramstick" in key:
                    new_ramsticks_dict[key] = value
                elif "rams" == key:
                    existing_ramsticks_list = self.data.getlist(key)
                elif "newproc" in key:
                    new_processors_dict[key] = value
                elif "processors" == key:
                    existing_processors_list = self.data.getlist(key)
                elif "newgpu" in key:
                    new_gpus_dict[key] = value
                elif "gpus" == key:
                    existing_gpus_list = self.data.getlist(key)
                elif "observations" == key:
                    existing_observations_list = self.data.getlist(key)
            return {
                "new_ramsticks": new_ramsticks_dict,
                "existing_ramsticks": existing_ramsticks_list,
                "new_processors": new_processors_dict,
                "existing_processors": existing_processors_list,
                "new_gpus": new_gpus_dict,
                "existing_gpus": existing_gpus_list,
                "existing_observations": existing_observations_list
            }

        def _get_unique_ids(dict):
            ids = []
            for key, value in dict.items():
                idx = key.split('_')[-1]
                if idx not in ids:
                    ids.append(idx)
                    yield idx

        def _save_new_ramsticks(ramsticks_dict):
            for idx in _get_unique_ids(ramsticks_dict):
                new_ramstick = Rams.objects.get_or_create(
                    ram_serial='N/A',
                    capacity=ramsticks_dict['newramstick_capacity_' + idx],
                    clock=ramsticks_dict['newramstick_clock_' + idx],
                    type=ramsticks_dict['newramstick_type_' + idx]
                )[0]
                RamToComp.objects.get_or_create(f_id_computer_ram_to_com=computer, f_id_ram_ram_to_com=new_ramstick)

        def _save_existing_ramsticks(existing_ramsticks_list):
            for idx in existing_ramsticks_list:
                ram = Rams.objects.get(id_ram=idx)
                RamToComp.objects.get_or_create(f_id_computer_ram_to_com=computer, f_id_ram_ram_to_com=ram)

        def _save_new_processors(new_processors_dict):
            for idx in _get_unique_ids(new_processors_dict):
                processor = Processors.objects.get_or_create(
                    f_manufacturer=Manufacturers.objects.get_or_create(
                        manufacturer_name=new_processors_dict["newproc_manufacturername_" + idx],
                    )[0],
                    model_name=new_processors_dict["newproc_modelname_" + idx],
                    stock_clock=new_processors_dict["newproc_stockclock_" + idx],
                    max_clock=new_processors_dict["newproc_maxclock_" + idx],
                    cores=new_processors_dict["newproc_cores_" + idx],
                    threads=new_processors_dict["newproc_threads_" + idx]
                )[0]
                Computerprocessors.objects.get_or_create(f_id_computer=computer, f_id_processor=processor)

        def _save_existing_processors(existing_processors_list):
            for idx in existing_processors_list:
                processor = Processors.objects.get(id_processor=idx)
                Computerprocessors.objects.get_or_create(f_id_computer=computer, f_id_processor=processor)
            
        def _save_new_gpus(new_gpus_dict):
            for idx in _get_unique_ids(new_gpus_dict):
                gpu = Gpus.objects.get_or_create(
                    gpu_name=new_gpus_dict["newgpu_gpuname_" + idx],
                    f_id_manufacturer=Manufacturers.objects.get_or_create(
                        manufacturer_name=new_gpus_dict["newgpu_manufacturername_" + idx]
                    )[0],
                )[0]
                Computergpus.objects.get_or_create(f_id_computer=computer, f_id_gpu=gpu)

        def _save_existing_gpus(existing_gpus_list):
            for idx in existing_gpus_list:
                gpu = Gpus.objects.get(id_gpu=idx)
                Computergpus.objects.get_or_create(f_id_computer=computer, f_id_gpu=gpu)
                
        def _save_existing_observations(existing_observations_list):
            for idx in existing_observations_list:
                observation = Observations.objects.get(id_observation=idx)
                Computerobservations.objects.get_or_create(f_id_computer=computer, f_id_observation=observation)

        main_dict = _form_main_dict()
        _save_new_ramsticks(main_dict["new_ramsticks"])
        _save_existing_ramsticks(main_dict["existing_ramsticks"])
        _save_new_processors(main_dict["new_processors"])
        _save_existing_processors(main_dict["existing_processors"])
        _save_new_gpus(main_dict["new_gpus"])
        _save_existing_gpus(main_dict["existing_gpus"])
        _save_existing_observations(main_dict["existing_observations"])

    def validate(self):
        """"
        Validates if all required fieldnames are present within provided queryset.
        """
        necessary_fieldnames = (
            "serial",
            "type_name",
            "category_name",
            'box_number',
            "manufacturer_name",
            "model_name",
            "tester_name",
            "license_name",
            "received_batch_name",
            "diagonal_text"
        )

        error_messages = (
            "Serial was not set",
            "Type was not set",
            "Category was not set",
            "Box number was not set",
            "Manufacturer was not set",
            "Model was not set",
            "Tester was not set",
            "License was not set",
            "Received batch was not set",
            "Diagonal was not set",
        )
        for error_message, necessary_fieldname in zip(error_messages, necessary_fieldnames):
            if self.data.get(necessary_fieldname) == "" or self.data.get(necessary_fieldname) is None:
                self.error_list.append(error_message)
        if Computers.objects.filter(computer_serial=self.data.get("serial")):
            self.error_list.append("Computer having the same serial allready exists")
        if not self.data.get("observations"):
            self.error_list.append('No observation specified: At least one observation must be set.')
        return not self.error_list


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
        self.resolutions = Resolutions.objects.values_list('resolution_text', flat=True)
        self.resolution_categories = Resolutioncategories.objects.values_list('resolution_category_name', flat=True)

        self.computer_form_factors = list(ComputerFormFactors.objects.values_list("form_factor_name", flat=True))
        self.computer_form_factors.insert(0, '')


class AutoFilter:
    """
    Class responsible for applying filters on a computers queryset.
    Attributes:
        keys(typple of strings) - hold on to keys which group what part of queryset should be filtered by. Logic is
        implemented in filter() method.
    """

    keys = ('man-af', 'sr-af', 'scr-af', 'ram-af', 'gpu-af', 'mod-af', 'cpu-af', 'oth-af', 'cli-af', 'dos-af', 'pri-af',
            'tes-af', 'cff-af', 'sta-af')

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
        print(self.filter_dict)
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
                computers = computers.filter(
                    id_computer__in=Computergpus.objects.filter(
                        f_id_gpu__gpu_name__in=value
                    ).values_list('f_id_computer', flat=True).order_by('f_id_computer')
                )
            elif key == 'mod-af':
                computers = computers.filter(f_model__model_name__in=value)
            elif key == 'cpu-af':
                computers = computers.filter(
                    id_computer__in=Computerprocessors.objects.filter(
                        f_id_processor__model_name__in=value
                    ).values_list('f_id_computer', flat=True).order_by('f_id_computer')
                )
            elif key == 'oth-af':
                computers = computers.filter(
                    id_computer__in=Computerobservations.objects.filter(
                        f_id_observation__full_name__in=value
                    ).values_list('f_id_computer', flat=True)
                )
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
            elif key == 'cff-af':
                computers = computers.filter(f_id_computer_form_factor__form_factor_name__in=value)
            elif key == 'sta-af':
                statuses = ["Sold", 'Ordered', "No status"]
                statusQueries = [Q(f_sale__isnull=False), Q(f_sale__isnull=True, f_id_comp_ord__isnull=False), Q(f_sale__isnull=True, f_id_comp_ord__isnull=True)]
                query = None
                for valuex in value:
                    if query is None:
                        query = statusQueries[statuses.index(valuex)]
                    else:
                        query |= statusQueries[statuses.index(valuex)]
                computers = computers.filter(query)
        return computers


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace('', (str(t[0]) or str(t[1])).strip()) for t in findterms(query_string)]


def search(keyword, computers):

    searchfields = (
        'computer_serial',
        'other',
        'f_manufacturer__manufacturer_name',
        'f_diagonal__diagonal_text',
        'f_ram_size__ram_size_text',
        'f_model__model_name',
        'f_sale__f_id_client__client_name',
        'f_sale__date_of_sale',
        'price',
        'computergpus__f_id_gpu__gpu_name',
        'computergpus__f_id_gpu__f_id_manufacturer__manufacturer_name',
        'computerprocessors__f_id_processor__f_manufacturer__manufacturer_name',
        'computerprocessors__f_id_processor__model_name',
        'computerprocessors__f_id_processor__stock_clock',
        'computerprocessors__f_id_processor__max_clock',
        'computerprocessors__f_id_processor__cores',
        'computerprocessors__f_id_processor__threads',
        'f_id_computer_form_factor__form_factor_name',
        'f_id_received_batches__received_batch_name',
        'computerdrives__f_drive__f_hdd_sizes__hdd_sizes_name',
        'computerdrives__f_drive__f_speed__speed_name',
        'computerdrives__f_drive__health',
        'f_id_matrix__f_id_cable_type__cable_type_name',
        'f_tester__tester_name',
        'f_id_computer_resolutions__f_id_resolution__resolution_text',
        'f_id_computer_resolutions__f_id_resolution_category__resolution_category_name',
        'computerobservations__f_id_observation__shortcode',
        # 'computerobservations__f_id_observation__full_name', # Takes to much of time to search by this field(increases 5s to 3min. 40s.)
        'computerobservations__f_id_observation__f_id_observation_category__category_name',
        'computerobservations__f_id_observation__f_id_observation_subcategory__subcategory_name',
        'battocomp__f_bat_bat_to_com__model',
        'f_id_comp_ord__f_order_id_to_order__order_name',

    )
    return computers.filter(get_query_for_item_search_from_computer_edit(keyword, searchfields)).distinct()


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
        self.orders = orders
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
    """
    Class responsible for portraying available Orders in website.
    """

    def __init__(self, data_dict=None):
        self.data_dict = data_dict
        self.order_list = []
        for ord in Orders.objects.all():
            self.order_list.append(Order(ord))

        self.filter()
        self.autoFilters = OrdersClassAutoFilter(self.order_list)

        self.qty = int(data_dict.get('qty', 10))
        self.page = int(data_dict.get('page', 1))
        self.qtySelect = QtySelect2(self.qty)
        paginator = Paginator(self.order_list, self.qty)
        self.order_list = paginator.get_page(self.page)
        self.index = self.qty * (self.page - 1)

    def increment(self):
        """
        Increments index which is used for numbering orders in website.
        :return: empty string, so that nothing would be rendered.
        """
        self.index += 1
        return ''

    def filter(self):
        """
        Filters Orders based on provided keys and values.
        :param data_dict:
        :return:
        """

        keys = ('ord-af', 'clt-af', 'qty-af', 'dat-af', 'tes-af', 'sta-af')
        new_dict = {}
        if 'orders' in self.data_dict:
            self.data_dict.pop('orders')
        for key in keys:
            if key in self.data_dict:
                new_dict[key] = self.data_dict.pop(key)

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
                    if not str(order.count()) in new_dict['qty-af']:
                        self.order_list.remove(order)
            elif key == 'dat-af':
                for order in self.order_list[:]:
                    if not str(order.date) in new_dict['dat-af']:
                        self.order_list.remove(order)
            elif key == 'tes-af':
                print(f"Keys: {new_dict['tes-af']}")
                for order in self.order_list[:]:
                    print(f'Order testers: {order.testers}')
                    if not all(x in order.testers for x in new_dict['tes-af']):
                        print('Removing')
                        self.order_list.remove(order)
            elif key == 'sta-af':
                for order in self.order_list[:]:
                    if not order.get_status() in new_dict['sta-af']:
                        self.order_list.remove(order)


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

    def __init__(self, data_dict):
        self.data_dict = data_dict
        self.lots = self._get_lots()

        self.filter()
        self.autoFilters = LotsHolderAutoFilter(self.lots)

        self.qty = int(data_dict.get('qty', 10))
        self.page = int(data_dict.get('page', 1))
        self.qtySelect = QtySelect2(self.qty)

        paginator = Paginator(self.lots, self.qty)
        self.lots = paginator.get_page(self.page)
        self.index = self.qty * (self.page - 1)

    def increment(self):
        """
        Increments index which is used for numbering Charger Categories in website.
        :return: empty string, so that nothing would be rendered.
        """
        self.index += 1
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

    def filter(self):
        keys = ('nam-af', 'day-af', 'cnt-af')
        new_dict = {}
        if 'lots' in self.data_dict:
            self.data_dict.pop('lots')
        for key in keys:
            if key in self.data_dict:
                new_dict[key] = self.data_dict.pop(key)
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

    def __init__(self, data_dict=None):
        self.data_dict = data_dict
        self.hdds = Drives.objects.all()
        self.changedKeys = []

        self.filter()
        self.autoFilters = HddAutoFilterOptions(self.hdds)

        self.qty = int(data_dict.get('qty', 10))
        self.page = int(data_dict.get('page', 1))
        self.qtySelect = QtySelect2(self.qty)
        paginator = Paginator(self.hdds, self.qty)
        self.hdds = paginator.get_page(self.page)
        self.index = self.qty * (self.page - 1)

    def increment(self):
        """
        Increments index which is used for numbering Charger Categories in website.
        :return: empty string, so that nothing would be rendered.
        """
        self.index += 1
        return ''

    def filter(self):
        keys = ('ser-af', 'mod-af', 'siz-af', 'loc-af', 'spe-af', 'for-af', 'hp-af', 'day-af')
        new_dict = {}
        if 'hdds' in self.data_dict:
            self.data_dict.pop('hdds')
        for key in keys:
            if key in self.data_dict:
                new_dict[key] = self.data_dict.pop(key)
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


class HddAutoFilterOptions:
    """
    Class responsible of holding unique values of hdd to filter by in website,
    """

    def __init__(self, hdds):
        self.hdds = hdds
        self.serials = hdds.values_list('hdd_serial', flat=True).distinct().order_by('hdd_serial')
        
    def models(self):
        return self._many_to_one_getter('f_hdd_models__hdd_models_name')

    def sizes(self):
        return self._many_to_one_getter('f_hdd_sizes__hdd_sizes_name')

    def locks(self):
        return self._many_to_one_getter('f_lock_state__lock_state_name')

    def speeds(self):
        return self._many_to_one_getter('f_speed__speed_name')

    def forms(self):
        return self._many_to_one_getter('f_form_factor__form_factor_name')
    
    def healths(self):
        return self._many_to_one_getter('health')
    
    def days(self):
        return self._many_to_one_getter('days_on')

    def _many_to_one_getter(self, field_name):
        for name in self._get_names_queryset(field_name):
            qty = self.hdds.filter(**{field_name: name}).count()
            yield FilterUnit(name=name, qty=qty)

    def _get_names_queryset(self, field_name):
        '''
        This method is to ensure that if fields passed are of int origins(field_names are hardcoded in method)
        that theirs queryset would not be excluded from empty stings.
        :param field_name: fieldname of which filter choices should be constructed.
        :return: formed queryset
        '''
        int_fields = ['health', 'days_on']
        if field_name in int_fields:
            return self.hdds.exclude(
                **{field_name: None}
            ).values_list(field_name, flat=True).distinct().order_by(field_name)
        return self.hdds.exclude(**{field_name: None}).exclude(
            **{field_name: ''}
        ).values_list(field_name, flat=True).distinct().order_by(field_name)

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

    def sizes(self):
        """
        Method which returns hddsizes choices to html form.
        :return: Collection of hddsizes.
        """
        return HddSizes.objects.values_list('hdd_sizes_name', flat=True).distinct().order_by('hdd_sizes_name')

    def states(self):
        """
        Method which returns lock states choices to html form.
        :return: Collection of lock states.
        """
        return LockState.objects.values_list('lock_state_name', flat=True).distinct().order_by('lock_state_name')

    def speeds(self):
        """
        Method which returns speeds choices to html form.
        :return: Collection of speeds.
        """
        return Speed.objects.values_list('speed_name', flat=True).distinct().order_by('speed_name')

    def form_factors(self):
        """
        Method which returns form factors to html form.
        :return: Collection of form factors.
        """
        return FormFactor.objects.values_list('form_factor_name', flat=True).distinct().order_by('form_factor_name')

    def computer_ids(self):
        """
        Method which returns computer ids to html form.
        These ids are used to form buttons which open responing computer_edit urls.
        :return: Collection of computer ids.
        """
        return Computerdrives.objects.filter(f_drive=self.hdd).values_list('f_id_computer__id_computer', flat=True)

    def manufacturers(self):
        """
        Method which returns manufacturer names to html form.
        :return: Collection of manufacturer names.
        """
        return Manufacturers.objects.values_list(
            'manufacturer_name', flat=True).distinct().order_by('manufacturer_name')

    def interfaces(self):
        """
        Method which returns interface names to html form.
        :return: Collection of interface names.
        """
        return PhysicalInterfaces.objects.values_list('interface_name', flat=True).distinct().order_by('interface_name')

    def types(self):
        """
        Method which returns type names to html form.
        :return: Collection of type names.
        """
        return DriveTypes.objects.values_list('type_name', flat=True).distinct().order_by('type_name')

    def families(self):
        """
        Method which returns family names to html form.
        :return: Collection of family names.
        """
        return DriveFamily.objects.values_list('family_name', flat=True).distinct().order_by('family_name')

    def process_edit(self, data_dict):
        '''
        Edits hdd's attributes based on provided data_dict
        :param data_dict: Attributes passed from website.
        '''
        self.hdd.hdd_serial = data_dict.pop('serial')[0]
        self.hdd.health = data_dict.pop('health')[0]
        self.hdd.days_on = data_dict.pop('days')[0]
        self.hdd.f_hdd_models = HddModels.objects.get_or_create(hdd_models_name=data_dict.pop('model')[0])[0]
        self.hdd.f_hdd_sizes = HddSizes.objects.get_or_create(hdd_sizes_name=data_dict.pop('size')[0])[0]
        self.hdd.f_lock_state = LockState.objects.get_or_create(lock_state_name=data_dict.pop('state')[0])[0]
        self.hdd.f_speed = Speed.objects.get_or_create(speed_name=data_dict.pop('speed')[0])[0]
        self.hdd.f_form_factor = FormFactor.objects.get_or_create(form_factor_name=data_dict.pop('form_factor')[0])[0]

        self.hdd.f_manufacturer = Manufacturers.objects.get_or_create(
            manufacturer_name=data_dict.pop('manufacturer_name')[0])[0]
        self.hdd.f_interface = PhysicalInterfaces.objects.get_or_create(
            interface_name=data_dict.pop('interface_name')[0])[0]
        self.hdd.description = data_dict.pop('description')[0]
        self.hdd.f_type = DriveTypes.objects.get_or_create(type_name=data_dict.pop('type_name')[0])[0]
        self.hdd.f_note = DriveNotes.objects.get_or_create(note_text=data_dict.pop('notes')[0])[0]
        self.hdd.f_family = DriveFamily.objects.get_or_create(family_name=data_dict.pop('family_name')[0])[0]
        self.hdd.f_width = DriveWidth.objects.get_or_create(width_name=data_dict.pop('width_name')[0])[0]
        self.hdd.f_height = DriveHeight.objects.get_or_create(height_name=data_dict.pop('height_name')[0])[0]
        self.hdd.f_length = DriveLength.objects.get_or_create(length_name=data_dict.pop('length_name')[0])[0]
        self.hdd.f_weight = DriveWeight.objects.get_or_create(weight_name=data_dict.pop('weight_name')[0])[0]
        self.hdd.f_power_spin = DrivePowerSpin.objects.get_or_create(
            power_spin_name=data_dict.pop('power_spin_name')[0])[0]
        self.hdd.f_power_seek = DrivePowerSeek.objects.get_or_create(
            power_seek_name=data_dict.pop('power_seek_name')[0])[0]
        self.hdd.f_power_idle = DrivePowerIdle.objects.get_or_create(
            power_idle_name=data_dict.pop('power_idle_name')[0])[0]
        self.hdd.f_power_standby = DrivePowerStandby.objects.get_or_create(
            power_standby_name=data_dict.pop('power_standby_name')[0])[0]
        self.hdd.total_writes = data_dict.pop('total_writes')[0]

        self.hdd.save()


def try_drive_delete_and_get_message(pk=None, serial=None):
    """
    Tries deleting drive record and it's pdf based on id or serial.
    In case of failure returns string of an error.
    :param pk: Id of drive,
    :param serial: Serial of drive.
    :return: string if deletion fails, None if everything is alright,
    """
    if pk:
        drive = Drives.objects.filter(hdd_id=pk)[0]
    if serial:
        drive = Drives.objects.filter(hdd_serial=serial)[0]

    try:
        try:
            os.system('tar -vf ' + os.path.join(os.path.join(settings.BASE_DIR, 'tarfiles'),
                                                drive.f_lot.lot_name + '.tar') + ' --delete "' + drive.tar_member_name + '"')
        except:
            pass
        drive.delete()
        print('Succesful deletion')
        return None
    except IntegrityError:
        return 'Drive is part of lot/order or computer.\r\nSolve this dependency first before drive deletion.'
    except Exception as e:
        print('Failed deletion')
        return 'Failure to delete record\r\n' + str(e)


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


class TarProcessor:
    """
    Class responsible for processing tar files with log of successfully deleted drives and their pdfs proving deletion.
    """

    def __init__(self, in_memory_tarfile):
        self.lot_name = in_memory_tarfile._name.replace('.tar', '')
        self.tar = tarfile.open(fileobj=in_memory_tarfile.file)
        self.drive_text_file = DriveTextFileManager(self._get_txt_file())
        self.text_to_write = WriteableMessage()
        self.lot = self._save_and_get_lots()

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

    def _get_txt_file(self):
        """
        As per now, txt file to parse has string 'Succe' in it's name.
        :return: first found txt file in tar.
        """
        for member in self.tar.getmembers():
            if 'Succe' in member.name:
                return self.tar.extractfile(member)

    def process_data(self):
        """
        Method which initiates processing of tarfile.
        Creates new reference to a new file.
        Iterates through drive_text_file.
        if line in drive_text_file iteration is not valid updates message,
        otherwise processes it by instantiating _process_valid_drive_line.
        """
        with tarfile.open(self._get_new_tarfile_location(), 'a') as self.new_tar:
            for drive_line in self.drive_text_file.get_drive_line_processors():
                if drive_line.is_valid():
                    self._process_valid_drive_line(drive_line=drive_line)
                else:
                    serial = drive_line.get_serial()
                    health = drive_line.get_health()
                    power_on = drive_line.get_power_on()
                    self.text_to_write.add(
                        string_to_add=f'SN: {serial} skipped. Health("{health}") or Power on("{power_on}") on are not digits.',
                        should_write=True
                    )

    def _get_new_tarfile_location(self):
        """
        :return: full path name where tarfiles should be saved.
        """
        return os.path.join(os.path.join(settings.BASE_DIR, 'tarfiles'), '{0}.tar'.format(self.lot_name))

    def _process_valid_drive_line(self, drive_line):
        """
        Processes valid drive line.
        :param drive_line: DriveLineProcessor object representing csv file's line as drive.
        """
        pdf = self._get_tar_member_by_serial(drive_line.get_serial())
        if drive_line.is_existing_drive():
            self._process_existing_drive(drive_line=drive_line, pdf=pdf)
        else:
            self._process_nonexistant_drive(drive_line=drive_line, pdf=pdf)

    def _get_tar_member_by_serial(self, serial):
        """
        :param serial: Drive's serial to look for in Tar.
        :return: pdf if exists or None if does not.
        """
        for member in self.tar.getmembers():
            if '(S-N ' + serial + ')' in member.name:
                return member
        return None

    @property
    def message(self):
        """
        Method returning what has failed.
        """
        return self.text_to_write.text

    def _process_existing_drive(self, drive_line, pdf):
        """
        Processes drive allready present in Drive table.
        :param drive_line: DriveLineProcessor object representing csv file's line as drive.
        :param pdf: pdf extracted from tarfile.
        """
        if pdf:
            self._process_existing_drive_with_pdf(
                drive_line=drive_line,
                pdf=pdf
            )
            self.text_to_write.add(
                string_to_add=f'SN: {drive_line.get_serial()} info updated. File updated.',
                should_write=True
            )
        else:
            self._update_existing_drive(drive_line)
            self.text_to_write.add(
                string_to_add=f'SN: {drive_line.get_serial()} record info updated. File info not changed.'
            )

    def _process_nonexistant_drive(self, drive_line, pdf):
        """
        Processes drive not present in Drive table.
        :param drive_line: DriveLineProcessor object representing csv file's line as drive.
        :param pdf: pdf extracted from tarfile.
        """
        if pdf:
            self.new_tar.addfile(pdf, self.tar.extractfile(pdf))
            self._save_new_drive(drive_line=drive_line, filename=pdf.name)
        else:
            self.text_to_write.add(
                string_to_add=f'SN: {drive_line.get_serial()} skipped. Not present in database and no file associated.',
                should_write=True
            )

    def _process_existing_drive_with_pdf(self, drive_line, pdf):
        """
        :param drive_line: DriveLineProcessor object representing csv file's line as drive.
        :param pdf: pdf extracted from tarfile.
        """
        self._try_to_remove_pdf(drive_line=drive_line)
        self.new_tar.addfile(pdf, self.tar.extractfile(pdf))
        self._update_existing_drive(drive_line, pdf.name)

    def _try_to_remove_pdf(self, drive_line):
        """
        Removes pdf out of new tarfile, to avoid file duplications.
        :param drive_line: DriveLineProcessor object representing csv file's line as drive.
        """
        try:
            pdf_to_remove = self._get_pdf_name(drive_line)
            if pdf_to_remove is not None:
                self.new_tar.getmember(pdf_to_remove)
                os.system(f'tar -vf {self._get_new_tarfile_location()} --delete "{pdf_to_remove}"')
        except:
            print('Pdf opening or its deletion had failed')
            pass

    def _get_pdf_name(self, drive_line):
        """
        Returns pdf name based on drive_line's serial number and model.
        :param drive_line: DriveLineProcessor object representing csv file's line as drive.
        :return: name of pdf.
        """
        drive = Drives.objects.filter(
            hdd_serial=drive_line.get_serial(),
            f_hdd_models=HddModels.objects.get(hdd_models_name=drive_line.get_model())
        )[0]
        return drive.tar_member_name

    def _save_new_drive(self, drive_line, filename):
        """
        Saves new drive.
        :param drive_line: DriveLineProcessor object representing csv file's line as drive.
        :param filename: filename of tarred pdf file.
        """
        Drives.objects.create(
            hdd_serial=drive_line.get_serial(),
            health=drive_line.get_health(),
            days_on=drive_line.get_power_on(),
            tar_member_name=filename,
            f_lot=self.lot,
            f_hdd_models=HddModels.objects.get_or_create(
                hdd_models_name=drive_line.get_model())[0],
            f_hdd_sizes=HddSizes.objects.get_or_create(
                hdd_sizes_name=drive_line.get_capacity())[0],
            f_lock_state=LockState.objects.get_or_create(
                lock_state_name=drive_line.get_lock())[0],
            f_speed=Speed.objects.get_or_create(
                speed_name=drive_line.get_speed())[0],
            f_form_factor=FormFactor.objects.get_or_create(
                form_factor_name=drive_line.get_form_factor())[0],

            f_manufacturer=Manufacturers.objects.get_or_create(
                manufacturer_name=drive_line.get_manufacturer())[0],
            f_interface=PhysicalInterfaces.objects.get_or_create(
                interface_name=drive_line.get_interface())[0],
            description=drive_line.get_description(),
            f_type=DriveTypes.objects.get_or_create(type_name=drive_line.get_type())[0],
            f_note=DriveNotes.objects.get_or_create(note_text=drive_line.get_notes())[0],
            f_family=DriveFamily.objects.get_or_create(family_name=drive_line.get_family())[0],
            f_width=DriveWidth.objects.get_or_create(width_name=drive_line.get_width())[0],
            f_height=DriveHeight.objects.get_or_create(height_name=drive_line.get_height())[0],
            f_length=DriveLength.objects.get_or_create(length_name=drive_line.get_length())[0],
            f_weight=DriveWeight.objects.get_or_create(weight_name=drive_line.get_weight())[0],
            f_power_spin=DrivePowerSpin.objects.get_or_create(
                power_spin_name=drive_line.get_spinup())[0],
            f_power_seek=DrivePowerSeek.objects.get_or_create(
                power_seek_name=drive_line.get_power_seek())[0],
            f_power_idle=DrivePowerIdle.objects.get_or_create(
                power_idle_name=drive_line.get_power_idle())[0],
            f_power_standby=DrivePowerStandby.objects.get_or_create(
                power_standby_name=drive_line.get_power_stand_by())[0],
            total_writes=drive_line.get_total_writes(),
            f_origin=Origins.objects.get_or_create(origin_name=f'Added with tar {self.lot_name}')[0],
            date_added=timezone.now(),
        )

    def _update_existing_drive(self, drive_line, filename=None):
        """
        Updates existing drive.
        :param drive_line: DriveLineProcessor object representing csv file's line as drive.
        :param filename: filename is passed only if drive has corresponding tarred pdf file to it.
        """
        drive = Drives.objects.filter(
            hdd_serial=drive_line.get_serial(),
            f_hdd_models=HddModels.objects.get_or_create(
                hdd_models_name=drive_line.get_model()
            )[0]
        )[0]
        drive.f_hdd_sizes = HddSizes.objects.get_or_create(
            hdd_sizes_name=drive_line.get_capacity()
        )[0]
        drive.f_lock_state = LockState.objects.get_or_create(
            lock_state_name=drive_line.get_lock()
        )[0]
        drive.f_speed = Speed.objects.get_or_create(
            speed_name=drive_line.get_speed()
        )[0]
        drive.f_form_factor = FormFactor.objects.get_or_create(
            form_factor_name=drive_line.get_form_factor()
        )[0]
        drive.health = drive_line.get_health()
        drive.days_on = drive_line.get_power_on()
        if filename:
            drive.tar_member_name = filename
        drive.f_lot = self.lot

        drive.f_manufacturer = Manufacturers.objects.get_or_create(
            manufacturer_name=drive_line.get_manufacturer())[0]
        drive.f_interface = PhysicalInterfaces.objects.get_or_create(
            interface_name=drive_line.get_interface())[0]
        drive.description = drive_line.get_description()
        drive.f_type = DriveTypes.objects.get_or_create(type_name=drive_line.get_type())[0]
        drive.f_note = DriveNotes.objects.get_or_create(note_text=drive_line.get_notes())[0]
        drive.f_family = DriveFamily.objects.get_or_create(
            family_name=drive_line.get_family())[0]
        drive.f_width = DriveWidth.objects.get_or_create(width_name=drive_line.get_width())[0]
        drive.f_height = DriveHeight.objects.get_or_create(
            height_name=drive_line.get_height())[0]
        drive.f_length = DriveLength.objects.get_or_create(
            length_name=drive_line.get_length())[0]
        drive.f_weight = DriveWeight.objects.get_or_create(
            weight_name=drive_line.get_weight())[0]
        drive.f_power_spin = DrivePowerSpin.objects.get_or_create(
            power_spin_name=drive_line.get_spinup())[0]
        drive.f_power_seek = DrivePowerSeek.objects.get_or_create(
            power_seek_name=drive_line.get_power_seek())[0]
        drive.f_power_idle = DrivePowerIdle.objects.get_or_create(
            power_idle_name=drive_line.get_power_idle())[0]
        drive.f_power_standby = DrivePowerStandby.objects.get_or_create(
            power_standby_name=drive_line.get_power_stand_by())[0]
        drive.total_writes = drive_line.get_total_writes()
        drive.save()


class DriveOrderProcessor:
    """
    Class responsible for processing order txt files.
    """

    def __init__(self, txt_object):
        self.filename = txt_object._name
        self.drive_text_file = DriveTextFileManager(txt_object)
        self.text_to_write = WriteableMessage()
        self.hddOrder = self._get_drive_order()

    def process_data(self):
        """
        Method which initiates processing of csv order file.
        Iterates through drive_text_file.
        if line in drive_text_file iteration is not valid updates message,
        otherwise processes it by instantiating _process_valid_drive_line.
        """
        for drive_line in self.drive_text_file.get_drive_line_processors():
            if drive_line.is_valid():
                self._process_valid_drive_line(drive_line=drive_line)
                pass
            else:
                serial = drive_line.get_serial()
                health = drive_line.get_health()
                power_on = drive_line.get_power_on()
                self.text_to_write.add(
                    string_to_add=f'SN: {serial} skipped. Health("{health}") or Power on("{power_on}") on are not digits.',
                    should_write=True
                )

    def _process_valid_drive_line(self, drive_line):
        """
        Processes valid drive line.
        :param drive_line: DriveLineProcessor object representing csv file's line as drive.
        """
        if drive_line.is_existing_drive():
            self._update_existing_drive(drive_line)
        else:
            self._save_new_drive(drive_line)

    def _update_existing_drive(self, drive_line):
        """
        Updates drive's order to a new one.
        :param drive_line: DriveLineProcessor object representing csv file's line as drive.
        """
        drives = Drives.objects.filter(
            hdd_serial=drive_line.get_serial(),
            f_hdd_models=HddModels.objects.get_or_create(
                hdd_models_name=drive_line.get_model()
            )[0]
        )
        if drives[0].f_hdd_order:
            self.text_to_write.add(
                string_to_add=f'SN: {drives[0].hdd_serial} had order asigned. '
                f'Was assigned to order {drives[0].f_hdd_order.order_name}. '
                f'New name is: {self.filename.replace(".txt", "")}',
                should_write=True
            )
        drives.update(f_hdd_order=self.hddOrder)

    def _save_new_drive(self, drive_line):
        """
        Saves new order's drive.
        :param drive_line: DriveLineProcessor object representing csv file's line as drive.
        """
        Drives.objects.create(
            hdd_serial=drive_line.get_serial(),
            health=drive_line.get_health(),
            days_on=drive_line.get_power_on(),
            f_hdd_models=HddModels.objects.get_or_create(
                hdd_models_name=drive_line.get_model())[0],
            f_hdd_sizes=HddSizes.objects.get_or_create(
                hdd_sizes_name=drive_line.get_capacity())[0],
            f_lock_state=LockState.objects.get_or_create(
                lock_state_name=drive_line.get_lock())[0],
            f_speed=Speed.objects.get_or_create(
                speed_name=drive_line.get_speed())[0],
            f_form_factor=FormFactor.objects.get_or_create(
                form_factor_name=drive_line.get_form_factor())[0],
            f_hdd_order=self.hddOrder,

            f_manufacturer=Manufacturers.objects.get_or_create(
                manufacturer_name=drive_line.get_manufacturer())[0],
            f_interface=PhysicalInterfaces.objects.get_or_create(
                interface_name=drive_line.get_interface())[0],
            description=drive_line.get_description(),
            f_type=DriveTypes.objects.get_or_create(type_name=drive_line.get_type())[0],
            f_note=DriveNotes.objects.get_or_create(note_text=drive_line.get_notes())[0],
            f_family=DriveFamily.objects.get_or_create(family_name=drive_line.get_family())[0],
            f_width=DriveWidth.objects.get_or_create(width_name=drive_line.get_width())[0],
            f_height=DriveHeight.objects.get_or_create(height_name=drive_line.get_height())[0],
            f_length=DriveLength.objects.get_or_create(length_name=drive_line.get_length())[0],
            f_weight=DriveWeight.objects.get_or_create(weight_name=drive_line.get_weight())[0],
            f_power_spin=DrivePowerSpin.objects.get_or_create(
                power_spin_name=drive_line.get_spinup())[0],
            f_power_seek=DrivePowerSeek.objects.get_or_create(
                power_seek_name=drive_line.get_power_seek())[0],
            f_power_idle=DrivePowerIdle.objects.get_or_create(
                power_idle_name=drive_line.get_power_idle())[0],
            f_power_standby=DrivePowerStandby.objects.get_or_create(
                power_standby_name=drive_line.get_power_stand_by())[0],
            total_writes=drive_line.get_total_writes(),
            f_origin=Origins.objects.get_or_create(origin_name=f'Added with hdd order {self.hddOrder.order_id}')[0],
            date_added=timezone.now(),
        )

    @property
    def message(self):
        """
        Method returning what has failed.
        """
        return self.text_to_write.text

    def _get_drive_order(self):
        """
        Strips drives out of existing order with same name, and deletes order with text file's name as an order's name.
        :return: HddOrder's object which should have Prepared status and text file's name as an order's name.
        """
        hdd_orders = HddOrder.objects.filter(order_name=self.filename.replace('.txt', ''))
        if hdd_orders.exists():
            print('Such hdd orders exists')
            Drives.objects.filter(f_hdd_order=hdd_orders[0].order_id).update(f_hdd_order=None)
            hdd_orders[0].delete()

        return HddOrder.objects.create(
            order_name=self.filename.replace('.txt', ''),
            date_of_order=timezone.now().today().date(),
            f_order_status=OrderStatus.objects.get(order_status_id=3)
        )


class DriveTextFileManager:
    """
    Class responsible for processing txt file where first line consists of headers and other of data.
    Data cells seperated by '@' sign.
    """

    necessary_fieldnames = ['Serial', 'Manufacturer', 'Family', 'Model', 'Capacity', 'Locked', 'Type', 'Rotation Speed',
                            'FFactor', 'Health', 'Power On', 'Interface', 'Notes', 'Width', 'Height', 'Length',
                            'Weight', 'Power Spin', 'Power Seek', 'Power Idle', 'Power Standby', 'Total Writes',
                            'Description']

    def __init__(self, csv_file):
        if isinstance(csv_file, InMemoryUploadedFile) or isinstance(csv_file, tarfile.ExFileObject):
            # InMemoryUploadedFile and ExFileObject keeps binary format file.
            # To avoid issues regarding csv library, this is converted to UTF-8 textfile.
            csv_file = (line.decode('utf8') for line in csv_file)
        self.reader = csv.DictReader(csv_file, delimiter='@')
        self._validate_fieldnames()

    def get_drive_line_processors(self):
        """
        Yields line by line from self.reader as DriveLineProcessor objects.
        """
        for row in self.reader:
            yield DriveLineProcessor(row)

    def _has_needed_fieldnames(self):
        """
        :return: True/False depending if all necessary fieldnames are in self.reader.
        """
        return set(self.necessary_fieldnames).issubset(self.reader.fieldnames)

    def _validate_fieldnames(self):
        """
        Validates if required fieldnames are present in self.reader. If not throws error.
        """
        if not self._has_needed_fieldnames():
            lacking_fieldnames = list(set(self.necessary_fieldnames).difference(self.reader.fieldnames))
            raise Warning(f'Lacking required fieldnames:\n{lacking_fieldnames}\n\n'
                          f'Present fieldnames:\n{self.reader.fieldnames}\n\n'
                          f'Required fieldnames:\n{self.necessary_fieldnames}')


class DriveLineProcessor:
    """
    Class responsible for accepting line data and processing, end result is saving or updating model record.
    """

    def __init__(self, row):
        self.row = row
        self.message = ''

    def __repr__(self):
        return f'{self.row}'

    def is_existing_drive(self):
        """
        Checks based on the object if such record exists or not.
        :return: True/False. Drive exists or not.
        """
        model = HddModels.objects.get_or_create(hdd_models_name=self.get_model())[0]
        drive = Drives.objects.filter(
            hdd_serial=self.get_serial(),
            f_hdd_models=model
        )
        return drive.exists()

    def is_valid(self):
        return self.get_health().isdigit() and self.get_power_on().isdigit()

    def get_serial(self):
        return self.row['Serial']

    def get_manufacturer(self):
        return self.row['Manufacturer']

    def get_family(self):
        return self.row['Family']

    def get_model(self):
        return self.row['Model']

    def get_capacity(self):
        return self.row['Capacity']

    def get_lock(self):
        return self.row['Locked']

    def get_type(self):
        return self.row['Type']

    def get_speed(self):
        return self.row['Rotation Speed']

    def get_form_factor(self):
        return self.row['FFactor']

    def get_health(self):
        return self.row['Health'].replace("%", "").strip()

    def get_power_on(self):
        return self.row['Power On'].strip()

    def get_interface(self):
        return self.row['Interface']

    def get_description(self):
        return self.row['Description']

    def get_notes(self):
        return self.row['Notes']

    def get_width(self):
        return self.row['Width']

    def get_height(self):
        return self.row['Height']

    def get_length(self):
        return self.row['Length']

    def get_weight(self):
        return self.row['Weight']

    def get_spinup(self):
        return self.row['Power Spin']

    def get_power_seek(self):
        return self.row['Power Seek']

    def get_power_idle(self):
        return self.row['Power Idle']

    def get_power_stand_by(self):
        return self.row['Power Standby']

    def get_total_writes(self):
        return self.row['Total Writes']


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


class DriveOrdersHolder:

    def __init__(self, data_dict=None):
        self.data_dict = data_dict
        self.orders = self._get_orders()

        self.filter()
        self.autoFilters = HddOrdersHolderAutoFilter(self.orders)

        self.qty = int(data_dict.get('qty', 10))
        self.page = int(data_dict.get('page', 1))
        self.qtySelect = QtySelect2(self.qty)
        paginator = Paginator(self.orders, self.qty)
        self.orders = paginator.get_page(self.page)
        self.index = self.qty * (self.page - 1)

    def increment(self):
        """
        Increments index which is used for numbering Charger Categories in website.
        :return: empty string, so that nothing would be rendered.
        """
        self.index += 1
        return ''

    def filter(self):
        keys = ('hon-af', 'dat-af', 'cnt-af', 'ost-af')
        new_dict = {}
        for key in keys:
            if key in self.data_dict:
                new_dict[key] = self.data_dict.pop(key)
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
            self._proccess_existing_category_charger()
        else:
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

    def _proccess_new_category_charger(self):
        Chargers.objects.get_or_create(
            charger_serial=self.charger_serial,
            f_charger_category=ChargerCategories.objects.create(
                watts=self.wattage,
                f_manufacturer=Manufacturers.objects.get_or_create(manufacturer_name=self.manufacturer_name)[0],
                connector_type=self.connector_type
            )
        )


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

    def __init__(self, data_dict=None):
        self.data_dict = data_dict
        self.chargerCategories = []
        for cat in ChargerCategories.objects.all():
            self.chargerCategories.append(ChargerCategoryHolder(cat))

        self.filter()
        self.qty = int(data_dict.get('qty', 10))
        self.page = int(data_dict.get('page', 1))
        self.qtySelect = QtySelect2(self.qty)
        paginator = Paginator(self.chargerCategories, self.qty)
        self.chargerCategories = paginator.get_page(self.page)
        self.index = self.qty * (self.page - 1)

    def increment(self):
        """
        Increments index which is used for numbering Charger Categories in website.
        :return: empty string, so that nothing would be rendered.
        """
        self.index += 1
        return ''

    def filter(self):
        keys = ('man-af', 'watts-af', 'dcmin-af', 'dcmax-af', 'count-af', 'orig-af', 'used-af')
        new_dict = {}
        if 'chargers' in self.data_dict:
            self.data_dict.pop('chargers')
        for key in keys:
            if key in self.data_dict:
                new_dict[key] = self.data_dict.pop(key)
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

    def __init__(self, int_index, printer=None):
        self.full_serial = self._form_serial(int_index)
        self.printer = printer
        self.base_url = 'http://192.168.8.254:8000/website/by_serial/'

    def _form_serial(self, int_index):
        computer = Computers.objects.get(id_computer=int_index)
        return computer.computer_serial

    def print(self):
        """
        In case one row should be printed print_as_singular() should be called.
        In case of two rows call print_as_pairs()
        """
        self.qr_gen = Qrgenerator(self.base_url, [self.full_serial], self.printer)
        if self.printer == "Godex_G500":
            self.qr_gen.print_as_pairs()
        elif not self.printer or self.printer == "Godex_DT4x":
            self.qr_gen.print_as_singular()


class ComputerMultipleSerialPrinter:

    def __init__(self, data, printer=None):
        print("Printer: {0}".format(printer))
        print("Indexes: {0}".format(data))
        self.final_serials = []
        self.printer = printer
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
        self.qr_gen = Qrgenerator(self.base_url, self.final_serials, self.printer)
        if self.printer == "Godex_G500":
            self.qr_gen.print_as_pairs()
        elif not self.printer or self.printer == "Godex_DT4x":
            self.qr_gen.print_as_singular()


class Qrgenerator:

    def __init__(self, base_url, serials, printer):
        self.printer = printer
        self.base_url = base_url
        self.serials = serials

    def print_as_pairs(self):
        print("Printing as pairs")
        for index in range(self._get_pair_cycles()):
            serial_pair = self._get_serial_pair(index)
            image = self._formImagePair(serial_pair[0], serial_pair[1])
            with tempfile.NamedTemporaryFile() as temp:
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                temp.write(img_byte_arr.getvalue())
                if self.printer:
                    subprocess.call(['lpr', '-P', self.printer, temp.name])
                else:
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
                if self.printer:
                    subprocess.call(['lpr', '-P', self.printer, temp.name])
                else:
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


class Computer5th:

    def __init__(self, computer):
        print('this is Computer5th')
        self.computer = computer

    def collect_info(self):
        self.rc = RecordChoices()

        self.received_batch = None
        if self.computer.f_id_received_batches:
            self.received_batch = self.computer.f_id_received_batches.received_batch_name
        if self.computer.f_id_computer_form_factor:
            self.form_factor = self.computer.f_id_computer_form_factor.form_factor_name

    def rams(self):
        return Rams.objects.filter(ramtocomp__f_id_computer_ram_to_com=self.computer)

    def drives(self):
        return Drives.objects.filter(computerdrives__f_id_computer=self.computer)

    def batteries(self):
        return Batteries.objects.filter(battocomp__f_id_computer_bat_to_com=self.computer)

    def processors(self):
        return Processors.objects.filter(computerprocessors__f_id_computer=self.computer)

    def gpus(self):
        return Gpus.objects.filter(computergpus__f_id_computer=self.computer)

    def observations(self):
        return Observations.objects.filter(computerobservations__f_id_computer=self.computer)

    def save_info(self, data_dict):
        print(data_dict)

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
                for ram_id in _get_unique_ids(ram_dict):
                    ram = Rams.objects.get(id_ram=ram_id)
                    count_of_rams_to_comp = RamToComp.objects.filter(f_id_ram_ram_to_com=ram).count()
                    if not (ram.type == ram_dict['ram_type_'+str(ram_id)]):
                        if count_of_rams_to_comp > 1:
                            RamToComp.objects.get(
                                f_id_computer_ram_to_com=self.computer,
                                f_id_ram_ram_to_com=ram
                            ).delete()
                            ram.id_ram = None
                            ram.type = ram_dict['ram_type_'+str(ram_id)]
                            ram.save()
                            RamToComp.objects.get_or_create(
                                f_id_computer_ram_to_com=self.computer,
                                f_id_ram_ram_to_com=ram
                            )
                        elif count_of_rams_to_comp == 1:
                            try:
                                existing_ram = Rams.objects.get(
                                    ram_serial=ram.ram_serial,
                                    capacity=ram.capacity,
                                    clock=ram.clock,
                                    type=ram_dict['ram_type_'+str(ram_id)]
                                )
                                existing_ram_to_comp = RamToComp.objects.get(
                                    f_id_computer_ram_to_com=self.computer,
                                    f_id_ram_ram_to_com=ram
                                )
                                existing_ram_to_comp.f_id_ram_ram_to_com = existing_ram
                                existing_ram_to_comp.save()
                                ram.delete()
                            except Rams.DoesNotExist:
                                ram.type = ram_dict['ram_type_'+str(ram_id)]
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

        print('Saving computer')
        if self.computer.f_sale:
            client = Clients.objects.get_or_create(client_name=data_dict.pop('client_name')[0])[0]
            sale = self.computer.f_sale
            sale.f_id_client = client
            sale.date_of_sale = data_dict.pop('date_of_sale')[0]
            sale.save()
            self.computer.price = data_dict.pop('price')[0]
        self.computer.f_type = Types.objects.get_or_create(type_name=data_dict.pop('type_name')[0])[0]
        self.computer.f_category = Categories.objects.get_or_create(category_name=data_dict.pop('category_name')[0])[0]
        self.computer.f_manufacturer = Manufacturers.objects.get_or_create(
            manufacturer_name=data_dict.pop('manufacturer_name')[0])[0]
        self.computer.f_model = Models.objects.get_or_create(model_name=data_dict.pop('model_name')[0])[0]
        self.computer.f_ram_size = RamSizes.objects.get_or_create(ram_size_text=data_dict.pop('ram_size_text')[0])[0]
        self.computer.f_diagonal = Diagonals.objects.get_or_create(diagonal_text=data_dict.pop('diagonal_text')[0])[0]
        self.computer.f_license = Licenses.objects.get_or_create(license_name=data_dict.pop('license_name')[0])[0]
        self.computer.f_camera = CameraOptions.objects.get_or_create(option_name=data_dict.pop('option_name')[0])[0]
        self.computer.f_tester = Testers.objects.get_or_create(tester_name=data_dict.pop('tester_name')[0])[0]

        resolution = Resolutions.objects.get_or_create(resolution_text=data_dict.pop('resolution_text')[0])[0]
        resolution_category = Resolutioncategories.objects.get_or_create(
            resolution_category_name=data_dict.pop('resolution_category_text')[0])[0]
        self.computer.f_id_computer_resolutions = Computerresolutions.objects.get_or_create(
            f_id_resolution=resolution, f_id_resolution_category=resolution_category)[0]

        self.computer.other = data_dict.pop('other')[0]
        if "received_batch_name" in data_dict and self.computer.f_id_received_batches is None:
            received_batch = Receivedbatches.objects.get(received_batch_name=data_dict["received_batch_name"])
            self.computer.f_id_received_batches = received_batch
        if data_dict['box_number']:
            self.computer.box_number = data_dict.pop('box_number')[0]
        computer_form_factor = None
        if data_dict['form_factor']:
            computer_form_factor = ComputerFormFactors.objects.get(form_factor_name=data_dict.pop('form_factor')[0])
        self.computer.f_id_computer_form_factor = computer_form_factor
        self.computer.save()

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
        if computer_resolution:
            resolution = computer_resolution.f_id_resolution
            resolution_category = computer_resolution.f_id_resolution_category
        else:
            resolution = None
            resolution_category = None
        sale = self.computer.f_sale
        comp_ord = self.computer.f_id_comp_ord
        matrix = self.computer.f_id_matrix
        if matrix:
            cable_type = matrix.f_id_cable_type
        else:
            cable_type = None

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
        data_dict.pop('edit.x', None)
        data_dict.pop('edit.y', None)
        data_dict.pop('id_computer', None)
        data_dict.pop('serial', None)
        data_dict.pop('motherboard_serial', None)
        data_dict.pop('date', None)
        try:
            self.record = Computer5th(computer=self.computer)
            self.record.save_info(data_dict)
        except Exception as e:
            ex_type, ex, tb = sys.exc_info()
            self.message = str(e.with_traceback(tb))
        
    def process_get(self):
        print('Processing get request')
        self.record = Computer5th(computer=self.computer)
        self.record.collect_info()

    def delete_record(self):
        print('Processing delete request')
        self.record = Computer5th(computer=self.computer)
        self.record.delete()


def get_query_for_item_search_from_computer_edit(query_string, searchfields_tupple):
    """
    Forms Q query object to be used with filter() models method.
    :param query_string: searchable string collection seperated by spaces in form of string.
    :param searchfields_tupple: Fields by which search should be done.
    :return:
    """
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in searchfields_tupple:
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


class CustomTimer:

    def __init__(self):
        self.last_time = datetime.now()

    def frame_time(self, title):
        current_time = datetime.now()
        print(f'title: {title}, current time: {current_time}, difference: {current_time - self.last_time}')
        self.last_time = current_time
