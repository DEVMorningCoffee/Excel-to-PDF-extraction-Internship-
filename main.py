import pandas as pd
import numpy as np 
from pathlib import Path
import os


def read_form() -> None:
    local_csv_path = Path("./data.csv")
    df = pd.read_csv(local_csv_path)

    # Remove empty column  
    df["Inspection Number"].replace('', np.nan, inplace=True)
    df.dropna(subset=['Inspection Number'], inplace=True)

    sheet_data = dict()

    for index, row in df.iterrows():
        sheet_data = {
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

        reports_path = Path(f"../Reports/{sheet_data['Client Code']}")

        # Create folder if not exist
        if not os.path.exists(reports_path):
            os.makedirs(reports_path)

        
        output_file = os.path.join(reports_path, f"./{sheet_data['Client Code']}_{int(sheet_data['Inspection Number'])}.pdf")

    

if __name__ == "__main__":
    read_form()