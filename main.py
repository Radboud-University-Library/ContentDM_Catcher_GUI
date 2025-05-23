import streamlit as st
import pandas as pd
import os
import catcher_csv as cc
import catcher_service as cs

# Directory for uploaded CSV files
upload_dir = 'UploadCSVs'

# Check if the directory exists and if not, create it
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

def main():
    st.title("ContentDM Metadata Update Tool")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    data_frame = pd.DataFrame()

    if uploaded_file is not None:
        data_frame = pd.read_csv(uploaded_file, delimiter=';')
        st.write("Preview of Uploaded CSV:")
        st.dataframe(data_frame.head())

    alias = st.text_input("Collection Alias:")

    cisonick = st.text_input("ContentDM field (CISONICK):")

    if not data_frame.empty:
        column_to_update = st.selectbox("Select CDM_field to Update:", data_frame.columns)
    else:
        column_to_update = st.text_input("CDM_field to Update from CSV:")

    output_filename = st.text_input("Output CSV Filename:")

    if st.button("Create Catcher CSV"):
        if not data_frame.empty and alias and column_to_update and cisonick and output_filename:
            cc.create_catcher_csv(data_frame, alias, column_to_update, output_filename)
            st.success(f"CSV file `{output_filename}` has been created")

        else:
            st.error("Please upload a CSV file and fill in all parameters.")

    if st.button("Process Metadata Updates"):
        if not data_frame.empty and alias and column_to_update and cisonick and output_filename:
            csv_file_path = os.path.join(upload_dir, output_filename)
            cs.process_metadata_updates(csv_file_path, cisonick=cisonick)
            st.success("Metadata updates have been processed.")
        else:
            st.error("Please upload a CSV file and fill in all parameters.")

if __name__ == "__main__":
    main()
