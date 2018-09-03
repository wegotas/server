from django import forms
from ULCDTinterface.modelers import Document


class UploadFileFrom(forms.Form):
    document = forms.FileField()


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)