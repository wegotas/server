from django.forms import ModelForm
from server.modelers import Computers

class Computers_form(ModelForm):
    class Meta:
        model = Computers
        fields = ['id_computer', 'serial', 'manufacturer', 'model', 'cpu', 'ram', 'gpu', 'hdd', 'diagonal', 'license',
                  'camera', 'cover', 'display' , 'bezel', 'keyboard', 'mouse', 'sound', 'cdrom', 'battery', 'hdd_cover',
                  'ram_cover', 'other', 'tester', 'date', 'bios']

