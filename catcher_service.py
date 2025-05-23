import logging.config
from zeep import Client, Settings
from zeep.transports import Transport
from requests import Session
from requests.auth import HTTPBasicAuth
import csv
import os
from datetime import datetime

# Import settings
from settings import CONTENTDM_URL, USERNAME, PASSWORD, LICENSE, WSDL

# Enable logging
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    }
})

# Create a settings object with raw_response=True
settings = Settings(raw_response=True)


def process_metadata_updates(csv_path, cisonick):
    session = Session()
    session.auth = HTTPBasicAuth(USERNAME, PASSWORD)
    client = Client(WSDL, transport=Transport(session=session))

    # Assuming the metadataWrapper and metadata are correctly defined in your WSDL
    metadata_wrapper_type = client.get_type('ns0:metadataWrapper')
    metadata_type = client.get_type('ns0:metadata')

    completed_dir = 'Completed'
    if not os.path.exists(completed_dir):
        os.makedirs(completed_dir)

    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        transactions = []

        for row in reader:
            alias = row['Alias']
            cdm_id = row['CDM_id']
            field = row['CDM_field']
            value = row['Value']

            # Create metadata entries
            metadata_entries = [
                metadata_type(field="dmrecord", value=cdm_id), #dmrecord is the unique identifier for the record
                metadata_type(field=cisonick, value=value) # field name is at the end of the field property url in the admin interface
            ]

            print(metadata_entries)

            # Package into metadataWrapper
            metadata_wrapper = metadata_wrapper_type(metadataList={'metadata': metadata_entries})

            # Perform SOAP request
            try:
                response = client.service.processCONTENTdm(
                    action='edit',
                    cdmurl=CONTENTDM_URL,
                    username=USERNAME,
                    password=PASSWORD,
                    license=LICENSE,
                    collection=alias,
                    metadata=metadata_wrapper
                )
                transaction_status = f'Success: {response}'
            except Exception as e:
                transaction_status = f'Failed: {str(e)}'
                print(transaction_status) # Print the error message

            transactions.append((alias, cdm_id, field, transaction_status))

        timestamp = datetime.now().strftime('%Y-%m-%d--%H-%M')
        with open(os.path.join(completed_dir, f'Transactions_{timestamp}.csv'), 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Alias', 'CDM_id', 'CDM_field', 'Transaction'])
            writer.writerows(transactions)
