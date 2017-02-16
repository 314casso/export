from nutep.models import UploadedTemplate
from django.forms.models import ModelForm
from django import forms


class TemplateForm(ModelForm):
    attachment = forms.FileField(label="", widget=forms.FileInput(attrs={'class':'fileupload'}) )
    class Meta:
        model = UploadedTemplate
        fields = ['attachment']