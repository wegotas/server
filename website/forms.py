from ULCDTinterface.modelers import *
from django import forms
import tarfile
from django.db.models import Count


class TarDocumentForm(forms.Form):
    """Responsible for validating Tar file upload."""

    document = forms.FileField()

    def clean_document(self):
        """Checks if uploaded file can be handled by tarfile class."""
        document = self.files.get('document', None)

        try:
            with tarfile.open(fileobj=document.file):
                pass
        except tarfile.ReadError:
            raise forms.ValidationError('Provided file is not Tar file.')
        finally:
            document.file.seek(0, 0)

        return document


class DriveOrderDocumentForm(forms.Form):
    """Responsible for validating file upload. Does not check if file is valid as csv or not."""

    document = forms.FileField()


class ExportComputersForm(forms.Form):
    """Form responsible for accepting values by which computers csv/excel file is generated to download."""

    FILE_CHOICES = (
        ('EXCEL', 'EXCEL'),
        ('CSV', 'CSV')
    )

    computer = forms.CharField(widget=forms.HiddenInput(), initial='computer')
    no_status = forms.BooleanField(initial=True, required=False)
    ordered = forms.BooleanField(initial=True, required=False)
    sold = forms.BooleanField(initial=True, required=False)
    file_type = forms.ChoiceField(choices=FILE_CHOICES)


class BoxSelectionForm(forms.Form):
    """Form responsible for providing and accepting bpx number values."""
    '''
    BOX_CHOICES = [(f'{value["box_number"]}', f'{value["box_number"]} ({value["box_number__count"]})') for value in
               Computers.objects.filter(box_number__isnull=False).values('box_number').annotate(
                   Count("box_number")).order_by(
                   'box_number')]

    box_number = forms.ChoiceField(required=True, choices=[('', '---')] + BOX_CHOICES,
                                   widget=forms.Select(attrs={'onchange': "this.form.submit();"}))
    '''

    box_number = forms.ChoiceField(required=True, widget=forms.Select(attrs={'onchange': "this.form.submit();"}))

    def __init__(self, *args, **kwargs):
        super(BoxSelectionForm, self).__init__(*args, **kwargs)
        BOX_CHOICES = [(f'{value["box_number"]}', f'{value["box_number"]} ({value["box_number__count"]})') for value in
                       Computers.objects.filter(box_number__isnull=False).values('box_number').annotate(
                           Count("box_number")).order_by(
                           'box_number')]
        # self.choices['box_number'] = [('', '---')] + BOX_CHOICES

        self.fields['box_number'].choices = [('', '---')] + BOX_CHOICES
