vendor_choices = [
    ('all', 'All'),
    ('unk', 'Unknown'),
]

airport_choices = [
    ('rno', 'Reno-Tahoe International Airport'),
    ('rts', 'Reno-Stead Airport')
]

funding_choices = [
    ('all', 'All'),
    ('unk', 'Unknown'),
]

document_types = [
    ('all', 'All'),
    ('unk', 'Unknown'),
    ('memoranda', 'Memoranda'),
    ('agenda', 'Agenda'),
    ('meeting_document', 'Meeting Document'),
    ('literature_review', 'Literature Review'),
    ('report', 'Report'),
    ('letter', 'Letter'),
    ('proposal', 'Proposal'),
    ('press_release', 'Press Release'),
    ('specification', 'Specification'),
    ('documentation', 'Documentation'),
    ('instructions_and_procedures', 'Instructions and Procedures'),
    ('style_guide', 'Style Guide'),
    ('thesis', "Thesis"),
    ('oral_presentation', "Oral Presentation"),
    ('resume', "Resume"),
    ('notebook', "Notebook"),
    ('email', 'Email'),
    ('notes', 'Notes')
]

engineering_discipline_choices = [
                ('all', 'All'),
                ('unk', 'Unknown'),
                ('misc', 'Miscellaneous'),
                ('civil', 'Civil'),
                ('arch', 'Architectural'),
                ('structural', 'Structural'),
                ('landscaping', 'Landscaping'),
                ('mechanical-hvac', 'Mechanical-HVAC'),
                ('plumbing', 'Plumbing'),
                ('electrical', 'Electrical'),
                ('mechanical', 'Mechanical'),
                ('fire protection', 'Fire Protection')
            ]

engineering_sheet_types = [
                ('all', 'All'),
                ('unk', 'Unknown'),
                ('details', 'Details'),
                ('plan', 'Plan'),
                ('title', 'Title'),
                ('key', 'Key'),
                ('index', 'Index'),
                ('elevations', 'Elevations'),
                ('notes', 'Notes'),
                ('sections', 'Sections'),
                ('symbols', 'Symbols'),
                ('quantity', 'Quantity'),
                ('specifications', 'Specifications'),
                ('schedule', 'Schedule'),
                ('diagram', 'Diagram')
            ]


class FileTypes:
    """the type of files that we are interested in are defined here"""

    def __init__(self):
        pdf = {"pdf": "application/pdf"}
        odt = {"odt": "application/vnd.oasis.opendocument.text"}
        ods = {"ods": "application/vnd.oasis.opendocument.spreadsheet"}
        odp = {"odp": "application/vnd.oasis.opendocument.presentation"}
        msdoc = {"doc": "application/msword"}
        msdocx = {"docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
        excel1 = {"xls": "application/vnd.ms-excel"}
        excel2 = {"xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}
        text = {"txt": "text/plain"}
        csv = {"csv": "text/csv"}
        png = {"png": "image/png"}
        jpeg = {"jpg": "image/jpeg"}
        tif = {"tif": "image/tiff"}
        dwg = {"dwg": "image/vnd.dwg"}
        lyr = {"lyr": "application/octet-stream"}
        lpk = {"lpk": "application/octet-stream"}
        mpk = {"mpk": "application/octet-stream"}
        mxd = {"mxd": "application/octet-stream"}
        pptx = {"pptx": "application/octet-stream"}
        img = {"img": "image/img"}
        zip = {"zip": "application/zip"}

        self.file_type_choices = {
            "PDF": pdf,
            "Open Office Doc": odt,
            "Open Office Sheet": ods,
            "Open Office Presentation": odp,
            "MS Word Doc": msdoc,
            "MS Word Docx": msdocx,
            "MS Power Point": pptx,
            "Text": text,
            "MS Excel Xls": excel1,
            "MS Excel Xlsx": excel2,
            "CSV Spreadsheet": csv,
            "PNG Image": png,
            "JPEG Image": jpeg,
            "IMG Image": img,
            "TIF Image": tif,
            "AutoCad Dwg": dwg,
            "ESRI Layer File": lyr,
            "ESRI Layer Package": lpk,
            "ESRI Map Package": mpk,
            "ESRI Map Document": mxd,
            "ZIP File": zip
        }

        self.FILE_VIEWER_TYPES = []
        for f in ["ZIP File", "MS Power Point", "PDF", "Open Office Doc", "MS Word Doc", "MS Word Docx", "Open Office Presentation", "Text"]:
            self.FILE_VIEWER_TYPES.append((list(self.file_type_choices[f].keys())[0], f))

        self.TABLE_VIEWER_TYPES = []
        for f in ["Open Office Sheet", "MS Excel Xls", "MS Excel Xlsx", "CSV Spreadsheet"]:
            self.TABLE_VIEWER_TYPES.append((list(self.file_type_choices[f].keys())[0], f))

        self.IMAGE_VIEWER_TYPES = []
        for f in ["PNG Image", "JPEG Image", "IMG Image", "TIF Image"]:
            self.IMAGE_VIEWER_TYPES.append((list(self.file_type_choices[f].keys())[0], f))

        self.GIS_VIEWER_TYPES = []
        for f in ["ESRI Layer Package", "AutoCad Dwg", "ESRI Layer File", "ESRI Map Package", "ESRI Map Document"]:
            self.GIS_VIEWER_TYPES.append((list(self.file_type_choices[f].keys())[0], f))

        self.ALL_FILE_TYPES = dict(self.FILE_VIEWER_TYPES)
        self.ALL_FILE_TYPES.update(dict(self.TABLE_VIEWER_TYPES))
        self.ALL_FILE_TYPES.update(dict(self.IMAGE_VIEWER_TYPES))
        self.ALL_FILE_TYPES.update(dict(self.GIS_VIEWER_TYPES))

        self.ALL_FILE_DOMAINS = self.FILE_VIEWER_TYPES[:]
        self.ALL_FILE_DOMAINS.extend(self.TABLE_VIEWER_TYPES)
        self.ALL_FILE_DOMAINS.extend(self.IMAGE_VIEWER_TYPES)
        self.ALL_FILE_DOMAINS.extend(self.GIS_VIEWER_TYPES)

        self.DOC_VIEWER_TYPES = document_types

        self.engineering_discipline_choices = engineering_discipline_choices

        self.engineering_sheet_types = engineering_sheet_types

        self.vendor_choices = vendor_choices

        self.airport_choices = airport_choices

        self.funding_choices = funding_choices

        return