# -*- coding: utf-8 -*-

from nutep.models import UploadedTemplate, Contract
from django.forms.models import ModelForm
from django import forms
from django_select2.forms import ModelSelect2Widget
from django.utils.encoding import force_text


class ContractCustomWidget(ModelSelect2Widget):
    model = Contract.objects.all()
    search_fields = [
        'name__icontains'
    ]

    def label_from_instance(self, obj):
        return force_text(obj.name).upper()  
    

class TemplateForm(ModelForm):
    contract = forms.ModelChoiceField(label=u"Договор", widget=ContractCustomWidget(attrs={'style':'width:100%', 'required': None}), queryset=Contract.objects.all())
    attachment = forms.FileField(label=u"Шаблон", widget=forms.FileInput(attrs={'class':'fileupload', 'required': None}) )
    is_override = forms.BooleanField(label=u"Режим замещения", widget=forms.CheckboxInput(attrs={'class':'flat'}), initial=False, required=False)
    class Meta:
        model = UploadedTemplate
        fields = ['contract', 'attachment']
