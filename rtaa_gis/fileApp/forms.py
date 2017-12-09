from django import forms
from .utils.domains import FileTypes

ftypes = FileTypes()

date_format = [
        '%Y-%m', '%m-%Y', '%Y/%m', '%m/%Y',
        '%b %Y', '%Y %b', '%B %Y', '%Y %B'
    ]


class FilterForm(forms.Form):

    def __init__(self, init_base_name, init_date_added, init_grid_cells, init_sheet_title, sheet_types, init_sheet_types, init_project_title, init_project_desc, init_after_date,
                 init_before_date, init_sheet_description, init_vendor, disciplines, init_disciplines,
                 airports, init_airports, funding_types, init_funding_types, init_file_path, init_grant_number,
                 file_types, chkd_f_types, image_types, chkd_i_types, table_types, chkd_t_types, document_types,
                 chkd_d_types, chkd_gis_types, gis_types, *args, **kwargs):

        super(FilterForm, self).__init__(*args, **kwargs)
        # get the length of the sheet_type / discipline multiselect
        if len(sheet_types) >= len(disciplines):
            d = len(sheet_types)
        else:
            d = len(disciplines)

        self.fields['gis_type'].choices = gis_types
        self.fields['sheet_type'].choices = sheet_types
        self.fields['sheet_type'].widget.attrs = {"size": d}

        self.fields['discipline'].choices = disciplines
        self.fields['discipline'].widget.attrs = {"size": d}

        self.fields['airport'].choices = airports
        self.fields['funding_type'].choices = funding_types
        self.fields['funding_type'].widget.attrs = {"size": len(funding_types)}

        self.fields['file_type'].choices = file_types
        self.fields['image_type'].choices = image_types
        self.fields['table_type'].choices = table_types
        self.fields['document_type'].choices = document_types

        if init_base_name:
            self.fields['base_name'].initial = init_base_name
        if init_date_added:
            self.fields['date_added'].initial = init_date_added
        if init_grid_cells:
            self.fields['grid_cells'].initial = init_grid_cells
        if init_sheet_title:
            self.fields['sheet_title'].initial = init_sheet_title
        if init_sheet_types:
            self.fields['sheet_type'].initial = init_sheet_types
        if init_project_title:
            self.fields['project_title'].initial = init_project_title
        if init_project_desc:
            self.fields['project_description'].initial = init_project_desc
        if init_after_date:
            self.fields['after_date'].initial = init_after_date
        if init_before_date:
            self.fields['before_date'].initial = init_before_date
        if init_sheet_description:
            self.fields['sheet_description'].initial = init_sheet_description
        if init_vendor:
            self.fields['vendor'].initial = init_vendor
        if init_disciplines:
            self.fields['discipline'].initial = init_disciplines
        if init_airports:
            self.fields['airport'].initial = init_airports
        if init_funding_types:
            self.fields['funding_type'].initial = init_funding_types
        if init_file_path:
            self.fields['file_path'].initial = init_file_path
        if init_grant_number:
            self.fields['grant_number'].initial = init_grant_number
        if chkd_gis_types:
            self.fields['gis_type'].initial = chkd_gis_types
        if chkd_f_types:
            self.fields['file_type'].initial = chkd_f_types
        if chkd_i_types:
            self.fields['image_type'].initial = chkd_i_types
        if chkd_t_types:
            self.fields['table_type'].initial = chkd_t_types
        if chkd_d_types:
            self.fields['document_type'].initial = chkd_d_types

    base_name = forms.CharField(label="File Name", required=False)

    date_added = forms.DateField(label="Date Added", required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    grid_cells = forms.CharField(label='Grid Cells', required=False, widget=forms.TextInput())

    sheet_title = forms.CharField(label='Sheet Title', required=False)

    sheet_type = forms.MultipleChoiceField(choices=(), label="Sheet Type", required=False, widget=forms.SelectMultiple())

    discipline = forms.MultipleChoiceField(choices=(), label="Discipline", required=False, widget=forms.SelectMultiple())

    project_title = forms.CharField(label="Project Title", required=False)

    project_description = forms.CharField(label='Project Description', required=False)

    after_date = forms.DateField(label='Project After Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    before_date = forms.DateField(label='Project Before Date', required=False,  widget=forms.DateInput(attrs={'type': 'date'}))

    sheet_description = forms.CharField(label="Sheet Description", required=False)

    vendor = forms.CharField(label="Vendor", required=False)

    airport = forms.ChoiceField(choices=(), label='Airport', widget=forms.RadioSelect(), initial="rno")

    funding_type = forms.MultipleChoiceField(choices=(), label='Funding Type', required=False)

    file_path = forms.CharField(label='File Path', required=False)

    grant_number = forms.CharField(label='Grant Number', required=False)

    file_type = forms.MultipleChoiceField(choices=(), label='File Types', required=False,
                                          widget=forms.CheckboxSelectMultiple())

    image_type = forms.MultipleChoiceField(choices=(), label='Image Types', required=False,
                                           widget=forms.CheckboxSelectMultiple())

    table_type = forms.MultipleChoiceField(choices=(), label='Table Types', required=False,
                                           widget=forms.CheckboxSelectMultiple())

    document_type = forms.MultipleChoiceField(choices=(), label='Document Types', required=False,
                                              widget=forms.CheckboxSelectMultiple())

    gis_type = forms.MultipleChoiceField(choices=(), label='GIS Types', required=False,
                                         widget=forms.CheckboxSelectMultiple())


class UpdateForm(forms.Form):

    edit_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)

    edit_base_name = forms.CharField(widget=forms.TextInput(attrs={"readonly": True}), label="Filename", max_length=255)

    edit_grid_cells = forms.MultipleChoiceField(label="Currently Assigned Grid Cells", choices=(), widget=forms.CheckboxSelectMultiple)

    edit_new_grid_cells = forms.MultipleChoiceField(label="New Grid Cells", choices=(), widget=forms.CheckboxSelectMultiple)

    edit_sheet_title = forms.CharField(label="Sheet Title", strip=True, max_length=255, required=False)

    edit_discipline = forms.MultipleChoiceField(label="Disciplines", choices=ftypes.engineering_discipline_choices,
                                           widget=forms.CheckboxSelectMultiple)

    edit_sheet_type = forms.MultipleChoiceField(label="Sheet Types", choices=ftypes.engineering_sheet_types,
                                           widget=forms.CheckboxSelectMultiple, required=False)

    edit_doc_type = forms.MultipleChoiceField(label="Document Types", choices=ftypes.DOC_VIEWER_TYPES,
                                              widget=forms.CheckboxSelectMultiple, required=False)

    edit_project_title = forms.CharField(label="Project Title", strip=True, max_length=255, required=False)

    edit_project_desc = forms.CharField(label="Project Description", strip=True, max_length=255, required=False)

    edit_project_date = forms.DateField(label="Project Date", required=False,
                                        widget=forms.DateInput(attrs={'type': 'date'}))

    edit_sheet_desc = forms.CharField(label="Sheet Description", strip=True, max_length=255, required=False)

    edit_vendor = forms.CharField(label="Vendor", required=False, max_length=255)

    edit_funding_type = forms.CharField(label="Funding Type", required=False, max_length=255)

    edit_airport = forms.ChoiceField(choices=ftypes.airport_choices, label='Airport', widget=forms.RadioSelect(),
                                     required=True)

    edit_grant_number = forms.CharField(label="Grant Number", required=False, max_length=255)

    edit_date_added = forms.DateField(widget=forms.TextInput(attrs={"readonly": True}), label="Date Added", required=True)

    edit_file_path = forms.CharField(widget=forms.TextInput(attrs={"readonly": True}), label="File Path", required=True)

