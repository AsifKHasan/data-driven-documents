#!/usr/bin/env python3
'''
    common template code for document generation
'''

import os
from pprint import pprint

from helper.google.google_helper import *
from helper.openoffice.odt.odt_helper import *
from helper.logger import *

DATA_CONNECTORS = {
    'google': {
        'credential-json': '../conf/credential.json'
    }
}

DATA_SOURCES = {
    'spectrum-offer-letter': {
        'sheet': 'HR__appointment-confirmation-transfer-separation',
        'worksheet': 'offer',
        'data-range': 'A3:L'
    },
    'spectrum-transfer-letter': {
        'sheet': 'HR__appointment-confirmation-transfer-separation',
        'worksheet': 'transfer',
        'data-range': 'A3:M'
    },
    'spectrum-separation-letter': {
        'sheet': 'HR__appointment-confirmation-transfer-separation',
        'worksheet': 'separation',
        'data-range': 'A3:I'
    },
    'spectrum-salary-enhancement': {
        'sheet': 'spectrum__salary-revision__2022',
        'worksheet': 'spectrum-2022',
        'data-range': 'A5:V'
    },
    'celloscope-salary-enhancement': {
        'sheet': 'celloscope__salary-revision__2022',
        'worksheet': 'celloscope-2022',
        'data-range': 'A5:V'
    },
}

DATA_PROCESSORS = {
    'spectrum-offer-letter': {
        'columns': [
            {'column': 0, 'key': 'sequence'},
            {'column': 1, 'key': 'salutation'},
            {'column': 2, 'key': 'name'},
            {'column': 3, 'key': 'address'},
            {'column': 4, 'key': 'effectivefrom'},
            {'column': 5, 'key': 'designation'},
            {'column': 6, 'key': 'grade'},
            {'column': 7, 'key': 'wing'},
            {'column': 8, 'key': 'unit'},
            {'column': 9, 'key': 'remuneration'},
            {'column': 10, 'key': 'letterdate'},
        ],
        'filter-column': 11,
        'filter-value': 'yes',
    },
    'spectrum-transfer-letter': {
        'columns': [
            {'column': 0, 'key': 'sequence'},
            {'column': 1, 'key': 'salutation'},
            {'column': 2, 'key': 'name'},
            {'column': 3, 'key': 'effectivefrom'},
            {'column': 4, 'key': 'address'},
            {'column': 7, 'key': 'fromunit'},
            {'column': 8, 'key': 'tounit'},
            {'column': 9, 'key': 'supervisor'},
            {'column': 10, 'key': 'superdesignation'},
            {'column': 11, 'key': 'letterdate'},
        ],
        'filter-column': 12,
        'filter-value': 'yes',
    },
    'spectrum-separation-letter': {
        'columns': [
            {'column': 0, 'key': 'sequence'},
            {'column': 1, 'key': 'salutation'},
            {'column': 2, 'key': 'name'},
            {'column': 3, 'key': 'address'},
            {'column': 4, 'key': 'effectivefrom'},
            {'column': 5, 'key': 'clause'},
            {'column': 6, 'key': 'reasontext'},
            {'column': 7, 'key': 'letterdate'},
        ],
        'filter-column': 8,
        'filter-value': 'yes',
    },
    'spectrum-salary-enhancement': {
        'columns': [
            {'column': 0, 'key': 'sequence'},
            {'column': 1, 'key': 'salutation'},
            {'column': 2, 'key': 'name'},
            {'column': 3, 'key': 'wing'},
            {'column': 4, 'key': 'unit'},
            {'column': 5, 'key': 'supervisor'},
            {'column': 11, 'key': 'salary'},
            {'column': 12, 'key': 'increment'},
            {'column': 15, 'key': 'currentgrade'},
            {'column': 16, 'key': 'promotion'},
            {'column': 17, 'key': 'grade'},
            {'column': 18, 'key': 'designation'},
            {'column': 19, 'key': 'effectivefrom'},
            {'column': 20, 'key': 'letterdate'},
        ],
        'filter-column': 21,
        'filter-value': 'yes',
    },
    'celloscope-salary-enhancement': {
        'columns': [
            {'column': 0, 'key': 'sequence'},
            {'column': 1, 'key': 'salutation'},
            {'column': 2, 'key': 'name'},
            {'column': 7, 'key': 'designation'},
            {'column': 16, 'key': 'salary'},
            {'column': 17, 'key': 'increment'},
            {'column': 19, 'key': 'effectivefrom'},
            {'column': 20, 'key': 'letterdate'},
        ],
        'filter-column': 21,
        'filter-value': 'yes',
    },
}

DATA_SERIALIZERS = {
    'spectrum-offer-letter': {
        'input-template': '../template/spectrum/offer-letter/HR__offer-letter-template__2022.odt',
        'output-dir': '../out/spectrum/offer-letter',
        'output-file-pattern': 'spectrum__offer-letter__2022__{0}__{1}.odt',
        'pdf-output-for-files': True,
        'merge-files': True,
        'merged-file-pattern': 'spectrum__offer-letter__2022.odt',
        'pdf-output-for-merged-file': True,
    },
    'spectrum-transfer-letter': {
        'input-template': '../template/spectrum/transfer-letter/HR__transfer-letter-template__2022.odt',
        'output-dir': '../out/spectrum/transfer-letter',
        'output-file-pattern': 'spectrum__transfer-letter__2022__{0}__{1}.odt',
        'pdf-output-for-files': True,
        'merge-files': True,
        'merged-file-pattern': 'spectrum__transfer-letter__2022.odt',
        'pdf-output-for-merged-file': True,
    },
    'spectrum-separation-letter': {
        'input-template': '../template/spectrum/separation-letter/HR__separation-letter-template__2022.odt',
        'output-dir': '../out/spectrum/separation-letter',
        'output-file-pattern': 'spectrum__separation-letter__2022__{0}__{1}.odt',
        'pdf-output-for-files': True,
        'merge-files': True,
        'merged-file-pattern': 'spectrum__separation-letter__2022.odt',
        'pdf-output-for-merged-file': True,
    },
    'spectrum-salary-enhancement': {
        'input-template': '../template/spectrum/salary-enhancement/HR__salary-enhancement-template__2022.odt',
        'output-dir': '../out/spectrum/salary-enhancement',
        'output-file-pattern': 'spectrum__salary-enhancement__2022__{0}__{1}.odt',
        'pdf-output-for-files': True,
        'merge-files': True,
        'merged-file-pattern': 'spectrum__salary-enhancement__2022.odt',
        'pdf-output-for-merged-file': True,
    },
    'celloscope-salary-enhancement': {
        'input-template': '../template/celloscope/salary-enhancement/celloscope__salary-enhancement-template__2022.odt',
        'output-dir': '../out/celloscope/salary-enhancement',
        'output-file-pattern': 'celloscope__salary-enhancement__2022__{0}__{1}.odt',
        'pdf-output-for-files': True,
        'merge-files': True,
        'merged-file-pattern': 'celloscope__salary-enhancement__2022.odt',
        'pdf-output-for-merged-file': True,
    },
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
    se_data_processor_spec = DATA_PROCESSORS[output_processor]
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

        # dictionary of fields
        fields = {}
        for col_spec in se_data_processor_spec['columns']:
            key = col_spec['key']
            fields[key] = item[key]

        # generate the file
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
