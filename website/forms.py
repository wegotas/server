from django import forms
import tarfile


class TarDocumentForm(forms.Form):

    document = forms.FileField()

    def clean_document(self):
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

    document = forms.FileField()
