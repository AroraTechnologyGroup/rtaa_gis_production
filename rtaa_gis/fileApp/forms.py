from django import forms

date_format = [
        '%Y-%m', '%m-%Y', '%Y/%m', '%m/%Y',
        '%b %Y', '%Y %b', '%B %Y', '%Y %B'
    ]


class FilterForm(forms.Form):
    def __init__(self, sheet_types, vendors, disciplines, airports, funding_types, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['sheet_type'].choices = sheet_types
        self.fields['vendor'].choices = vendors
        self.fields['discipline'].choices = disciplines
        self.fields['airport'].choices = airports
        self.fields['funding_type'].choices = funding_types

    sheet_title = forms.CharField(label='Sheet Title', required=False)

    sheet_type = forms.ChoiceField(choices=(), label="Sheet Type", required=False)

    project_title = forms.CharField(label="Project Title", required=False)

    project_description = forms.CharField(label='Project Description', required=False)

    after_date = forms.DateField(required=False, initial="Month and Year", widget=forms.DateInput(format=date_format))

    before_date = forms.DateField(required=False, initial="Month and Year", widget=forms.DateInput(format=date_format))

    sheet_description = forms.CharField(label="Sheet Description", required=False)

    vendor = forms.ChoiceField(choices=(), label="Vendor", required=False)

    discipline = forms.ChoiceField(choices=(), label="Discipline", required=False)

    airport = forms.ChoiceField(choices=(), label='Airport', widget=forms.RadioSelect(), initial="RNO")

    funding_type = forms.ChoiceField(choices=(), label='Funding Type', required=False)

    file_path = forms.CharField(label='File Path', required=False)

    grant_number = forms.CharField(label='Grant Number', required=False)

