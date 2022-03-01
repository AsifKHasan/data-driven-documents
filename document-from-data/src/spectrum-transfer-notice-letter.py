#!/usr/bin/env python3
'''
    generate templated transfer document (letter) from data
'''

import os
from pprint import pprint

from helper.google.google_helper import *
from helper.openoffice.odt.odt_helper import *
from helper.logger import *

DATA_CONNECTORS = {
    'Google': {
        'credential-json': '../conf/credential.json'
    }
}

DATA_SOURCES = {
    'gsheet': {
        'sheet': 'HR__recruitment-confirmation-transfer-separation',
        'worksheet': 'transfer',
        'data-range': 'A3:M'
    }
}

DATA_PROCESSORS = {
    'transfer-notice': {
        'columns': [
            {'column': 0, 'key': 'sequence'},
            {'column': 1, 'key': 'salutation'},
            {'column': 2, 'key': 'name'},
            {'column': 3, 'key': 'effective-from'},
            {'column': 4, 'key': 'address'},
            {'column': 7, 'key': 'from-unit'},
            {'column': 8, 'key': 'to-unit'},
            {'column': 9, 'key': 'supervisor'},
            {'column': 10, 'key': 'supervisor-designation'},
            {'column': 12, 'key': 'letter-date'},
        ],
        'filter-column': 11,
        'filter-value': 'yes',
    }
}

DATA_SERIALIZERS = {
    'transfer-notice': {
        'input-template': '../template/spectrum/transfer-notice/HR__transfer-notice-template__2022.odt',
        'output-dir': '../out/spectrum/transfer-notice',
        'output-file-pattern': 'spectrum__transfer-notice__2022__{0}__{1}.odt',
        'pdf-output-for-files': True,
        'merge-files': True,
        'merged-file-pattern': 'spectrum__transfer-notice__2022.odt',
        'pdf-output-for-merged-file': True,
    }
}

''' authenticate to data service
'''
def authenticate_to_data_service(provider):
    google_data_connector_spec = DATA_CONNECTORS[provider]

    debug(f'authenticating with {provider}')
    client = connector_client(google_data_connector_spec)
    debug(f'authenticating with {provider} ... done')

    # wrap the connector in a data-connector object
    data_connector = {'client': client}

    return data_connector


''' acquire data from data source
'''
def acquire_data(source, data_connector):
    gsheet_data_source_spec = DATA_SOURCES[source]

    debug(f'acquiring data from {source}')
    values = gsheet_data(data_connector['client'], gsheet_data_source_spec)
    debug(f'acquiring data from {source} ... done')

    # wrap the data in a source-data object
    source_data = {'data': values}

    return source_data


''' process, transform, prepare data
'''
def process_data(data_processor, source_data):
    se_data_processor_spec = DATA_PROCESSORS[data_processor]

    raw_data = source_data['data']

    debug(f'processing data for [{data_processor}]')
    # the data is in a list (rows) of list (columns)
    data = []
    for row in raw_data:
        columns = {}
        # filter rows as specified
        if row[se_data_processor_spec['filter-column']] == se_data_processor_spec['filter-value']:
            for col_spec in se_data_processor_spec['columns']:
                columns[col_spec['key']] = row[col_spec['column']]

            data.append(columns)

    debug(f'processing data for [{data_processor}] ... done')

    # wrap the data in a processed-data object
    processed_data = {'data': data}

    return processed_data


''' generate documents from data
'''
def output_data(output_processor, processed_data):
    se_output_spec = DATA_SERIALIZERS[output_processor]

    data = processed_data['data']
    tmp_dir = se_output_spec['output-dir'] + '/tmp'

    # crete directories in case they do not exist
    os.makedirs(tmp_dir, exist_ok=True)

    debug(f'generating output for [{output_processor}]')

    # generate files for each data row
    temp_files = []
    for item in data:
        temp_file_path = tmp_dir + '/' + se_output_spec['output-file-pattern'].format(item['sequence'], item['name'].lower().replace(' ', '-'))
        temp_files.append(temp_file_path)

        # generate the file
        fields = {"sequence": item["sequence"], "salutation": item["salutation"], "name": item["name"], "effectivefrom": item["effective-from"], "address": item["address"], "fromunit": item["from-unit"], "tounit": item["to-unit"], "supervisor": item["supervisor"], "superdesignation": item["supervisor-designation"], "letterdate": item["letter-date"]}
        replace_fields(se_output_spec['input-template'], temp_file_path, fields)
        debug(f'.. generating odt for {item["name"]} ... done')

        # generate pdf if instructed to do so
        if se_output_spec['pdf-output-for-files']:
            debug(f'.. generating pdf from {temp_file_path}')
            generate_pdf(temp_file_path, tmp_dir)
            debug(f'.. generating pdf from {temp_file_path} ... done')

    # merge files if instructed to do so
    if se_output_spec['merge-files']:
        output_file_path = se_output_spec['output-dir'] + '/' + se_output_spec['merged-file-pattern'].format()
        debug(f'merging odt files')
        merge_files(temp_files, output_file_path)
        debug(f'merging odt files ... done')

    # generate pdf if instructed to do so
    if se_output_spec['pdf-output-for-merged-file']:
        debug(f'generating pdf from merged odt')
        generate_pdf(output_file_path, se_output_spec["output-dir"])
        debug(f'generating pdf from merged odt ... done')

    debug(f'generating output for [{output_processor}] ... done')

    return


if __name__ == '__main__':
    # get the appropriate data-connector
    data_connector = authenticate_to_data_service('Google')

    # get raw data from source
    source_data = acquire_data('gsheet', data_connector)

    # get processed data from the raw data
    processed_data = process_data('transfer-notice', source_data)

    # serialize final output from data
    output_data('transfer-notice', processed_data)
