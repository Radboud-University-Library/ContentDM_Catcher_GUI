# ContentDM Metadata Bulk Update Tool

## Overview
This tool provides a streamlined interface for bulk updating metadata fields in ContentDM collections. It works by:
1. Creating a properly formatted CSV file for the ContentDM catcher service
2. Processing the updates through ContentDM's web services

## Features
- User-friendly web interface built with Streamlit
- Bulk update capability for ContentDM metadata fields
- CSV file generation for catcher service
- Transaction logging for update operations
- Preview of uploaded CSV data

## Requirements
Install the required dependencies:

    pip install -r requirements.txt

## Setup
1. Clone this repository
2. Create a `settings.py` file with your ContentDM credentials:

## Usage

### 1. Preparing Your Input CSV
Your input CSV should contain:
- A column named 'CONTENTdm number' containing the item IDs
- The field(s) you want to update

### 2. Using the Web Interface

1. **Upload CSV File**
    - Click "Choose a CSV file" to upload your input CSV
    - A preview of your data will be shown

2. **Enter Required Information**
    - **Collection Alias**: Found in the collection profile in ContentDM Administration
    - **CISONICK**: The field identifier from ContentDM
        - Can be found in the URL when editing a field in ContentDM Admin
        - Example: In `https://server21010.contentdm.oclc.org/cgi-bin/admin/editfield.exe?CISODB=/Handschriften&CISONICK=music`
        - The CISONICK would be `music`
    - **Select Field to Update**: Choose from dropdown menu of available fields in your CSV
    - **Output Filename**: Name for the generated catcher service CSV file

3. **Process Updates**
    - Click "Create Catcher CSV" to generate the properly formatted CSV file
    - Click "Process Metadata Updates" to send the updates to ContentDM

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.