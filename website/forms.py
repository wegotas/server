from django import forms
import tarfile


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
