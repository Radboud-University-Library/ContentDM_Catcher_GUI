import pandas as pd
import os

def create_catcher_csv(df, alias, column_to_update, output_filename):
    output_data = []

    for index, row in df.iterrows():
        cdm_page_id = row.get('CONTENTdm number', '')
        value = row.get(column_to_update, '')

        output_data.append({
            'Alias': alias,
            'CDM_id': cdm_page_id,
            'CDM_field': column_to_update,
            'Value': value
        })

    output_df = pd.DataFrame(output_data)
    # Save the output CSV in the specified upload directory
    output_df.to_csv(os.path.join('UploadCSVs', output_filename), index=False)
