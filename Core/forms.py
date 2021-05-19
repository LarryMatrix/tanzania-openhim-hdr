from django import forms
from API import validators as validators


class PayloadImportForm(forms.Form):

    message_types = [
        ("SVCREC", 'Services Received'),
        ("DDC", 'Death By Disease Case in Facility'),
        ("DDCOUT", 'Death By Disease Case Outside Facility'),
        ("BEDOCC", 'Bed Occupancy'),
        ("RVC", 'Revenue Received'),
    ]
    file = forms.FileField()
    message_type = forms.CharField(label='Message Type', widget=forms.Select(choices=message_types))


class CPTCodeMappingImportForm(forms.Form):

    file = forms.FileField()