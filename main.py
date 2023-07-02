import pandas as pd
import numpy as np 
from pathlib import Path
import os
import pdfrw


ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


def fill_pdf(input_pdf_path, output_pdf_path, data_dict) -> None:
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    if key in data_dict.keys():
                        if type(data_dict[key]) == bool:
                            if data_dict[key]:
                                annotation.update(pdfrw.PdfDict(
                                    AS=pdfrw.PdfName('Yes')))
                        else:
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                            )
                            annotation.update(pdfrw.PdfDict(AP=''))
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

def read_form() -> None:
    local_csv_path = Path("./data.csv")
    df = pd.read_csv(local_csv_path)

    # Remove empty column  
    df["Inspection Number"].replace('', np.nan, inplace=True)
    df.dropna(subset=['Inspection Number'], inplace=True)

    for index, row in df.iterrows():
        data_dict = {
            'Client Code': row['Client Code'],
            'Inspection Number': int(row['Inspection Number']),
            'Occupant Name': row['Occupant Name'],
            'Street Address': row['Street Address'],
            'City': row['City'],
            'State': row['State'],
            'Zip': row['Zip'],
            'Lat': ' ' if np.isnan(row['LAT']) else row['LAT'],
            'Long': ' ' if np.isnan(row['LONG']) else row['LONG'],
        }

        reports_path = Path(f"../Reports/{data_dict['Client Code']}")

        # Create folder if not exist
        if not os.path.exists(reports_path):
            os.makedirs(reports_path)

        output_pdf_path = os.path.join(reports_path, f"./{data_dict['Client Code']}_{int(data_dict['Inspection Number'])}.pdf")
        input_pdf_path = Path('./Field Report.pdf')

        fill_pdf(input_pdf_path, output_pdf_path, data_dict)


if __name__ == "__main__":
    read_form()