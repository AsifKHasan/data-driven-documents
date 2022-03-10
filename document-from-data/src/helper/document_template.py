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
    'spectrum' : {
        'google': {
            'credential-json': '../conf/credential.json'
        },
    },
    'celloscope' : {
        'google': {
            'credential-json': '../conf/credential.json'
        },
    },
}

DATA_SOURCES = {
    'spectrum' : {
        'appointment-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'appointment',
            'data-range': 'A3:N'
        },
        'experience-certificate': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'experience-certificate',
            'data-range': 'A3:K'
        },
        'introduction-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'introduction',
            'data-range': 'A3:M'
        },
        'offer-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'offer',
            'data-range': 'A3:L'
        },
        'release-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'release',
            'data-range': 'A3:J'
        },
        'salary-certificate': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'salary-certificate',
            'data-range': 'A3:Q'
        },
        'salary-enhancement-letter': {
            'sheet': 'spectrum__salary-revision__2022',
            'worksheet': 'spectrum-2022',
            'data-range': 'A5:V'
        },
        'separation-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'separation',
            'data-range': 'A3:I'
        },
        'transfer-letter': {
            'sheet': 'HR__letters-certificates',
            'worksheet': 'transfer',
            'data-range': 'A3:M'
        },
    },
    'celloscope' : {
        'salary-enhancement-letter': {
            'sheet': 'celloscope__salary-revision__2022',
            'worksheet': 'celloscope-2022',
            'data-range': 'A5:V'
        },
    },
}

DATA_PROCESSORS = {
    'spectrum' : {
        'appointment-letter': {
            'columns': [
                {'column': 0, 'key': 'seq'},
                {'column': 1, 'key': 'salutation'},
                {'column': 2, 'key': 'name'},
                {'column': 3, 'key': 'address'},
                {'column': 4, 'key': 'effectivefrom'},
                {'column': 5, 'key': 'designation'},
                {'column': 6, 'key': 'grade'},
                {'column': 7, 'key': 'wing'},
                {'column': 8, 'key': 'unit'},
                {'column': 9, 'key': 'supervisor'},
                {'column': 10, 'key': 'remuneration'},
                {'column': 11, 'key': 'site'},
                {'column': 12, 'key': 'letterdate'},
            ],
            'filter-column': 13,
            'filter-value': 'yes',
        },
        'experience-certificate': {
            'columns': [
                {'column': 0, 'key': 'seq'},
                {'column': 1, 'key': 'salutation'},
                {'column': 2, 'key': 'name'},
                {'column': 3, 'key': 'designation'},
                {'column': 4, 'key': 'unit'},
                {'column': 5, 'key': 'joiningdate'},
                {'column': 6, 'key': 'separationdate'},
                {'column': 7, 'key': 'employmenttype'},
                {'column': 8, 'key': 'signatory'},
                {'column': 9, 'key': 'letterdate'},
            ],
            'filter-column': 10,
            'filter-value': 'yes',
        },
        'introduction-letter': {
            'columns': [
                {'column': 0, 'key': 'seq'},
                {'column': 1, 'key': 'name'},
                {'column': 2, 'key': 'birthdate'},
                {'column': 3, 'key': 'citizenship'},
                {'column': 4, 'key': 'presentaddress'},
                {'column': 5, 'key': 'permanentaddress'},
                {'column': 6, 'key': 'joiningdate'},
                {'column': 7, 'key': 'designation'},
                {'column': 8, 'key': 'employmenttype'},
                {'column': 9, 'key': 'remuneration'},
                {'column': 10, 'key': 'signatory'},
                {'column': 11, 'key': 'letterdate'},
            ],
            'filter-column': 12,
            'filter-value': 'yes',
        },
        'offer-letter': {
            'columns': [
                {'column': 0, 'key': 'seq'},
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
        'release-letter': {
            'columns': [
                {'column': 0, 'key': 'seq'},
                {'column': 1, 'key': 'salutation'},
                {'column': 2, 'key': 'name'},
                {'column': 3, 'key': 'address'},
                {'column': 4, 'key': 'effectivefrom'},
                {'column': 5, 'key': 'designation'},
                {'column': 6, 'key': 'unit'},
                {'column': 7, 'key': 'signatory'},
                {'column': 8, 'key': 'letterdate'},
            ],
            'filter-column': 9,
            'filter-value': 'yes',
        },
        'salary-certificate': {
            'columns': [
                {'column': 0, 'key': 'seq'},
                {'column': 1, 'key': 'salutation'},
                {'column': 2, 'key': 'name'},
                {'column': 3, 'key': 'designation'},
                {'column': 4, 'key': 'unit'},
                {'column': 5, 'key': 'joiningdate'},
                {'column': 6, 'key': 'employmenttype'},
                {'column': 7, 'key': 'basic'},
                {'column': 8, 'key': 'houserent'},
                {'column': 9, 'key': 'medical'},
                {'column': 10, 'key': 'conveyance'},
                {'column': 11, 'key': 'gross'},
                {'column': 12, 'key': 'tax'},
                {'column': 13, 'key': 'net'},
                {'column': 14, 'key': 'signatory'},
                {'column': 15, 'key': 'letterdate'},
            ],
            'filter-column': 16,
            'filter-value': 'yes',
        },
        'salary-enhancement-letter': {
            'columns': [
                {'column': 0, 'key': 'seq'},
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
        'separation-letter': {
            'columns': [
                {'column': 0, 'key': 'seq'},
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
        'transfer-letter': {
            'columns': [
                {'column': 0, 'key': 'seq'},
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
    },
    'celloscope' : {
        'salary-enhancement-letter': {
            'columns': [
                {'column': 0, 'key': 'seq'},
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
    },
}

DATA_SERIALIZERS = {
    'spectrum' : {
        'appointment-letter': {
            'input-template': '../template/spectrum/appointment-letter/HR__appointment-letter-template__2022.odt',
            'output-dir': '../out/spectrum/appointment-letter',
            'output-file-pattern': 'spectrum__appointment-letter__2022__{0}__{1}.odt',
            'pdf-output-for-files': True,
            'merge-files': False,
            'merged-file-pattern': 'spectrum__appointment-letter__2022.odt',
            'pdf-output-for-merged-file': False,
        },
        'experience-certificate': {
            'input-template': '../template/spectrum/experience-certificate/HR__experience-certificate-template__2022.odt',
            'output-dir': '../out/spectrum/experience-certificate',
            'output-file-pattern': 'spectrum__experience-certificate__2022__{0}__{1}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__experience-certificate__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'introduction-letter': {
            'input-template': '../template/spectrum/introduction-letter/HR__introduction-letter-template__2022.odt',
            'output-dir': '../out/spectrum/introduction-letter',
            'output-file-pattern': 'spectrum__introduction-letter__2022__{0}__{1}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__introduction-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'offer-letter': {
            'input-template': '../template/spectrum/offer-letter/HR__offer-letter-template__2022.odt',
            'output-dir': '../out/spectrum/offer-letter',
            'output-file-pattern': 'spectrum__offer-letter__2022__{0}__{1}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__offer-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'release-letter': {
            'input-template': '../template/spectrum/release-letter/HR__release-letter-template__2022.odt',
            'output-dir': '../out/spectrum/release-letter',
            'output-file-pattern': 'spectrum__release-letter__2022__{0}__{1}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__release-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'salary-certificate': {
            'input-template': '../template/spectrum/salary-certificate/HR__salary-certificate-template__2022.odt',
            'output-dir': '../out/spectrum/salary-certificate',
            'output-file-pattern': 'spectrum__salary-certificate__2022__{0}__{1}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__salary-certificate__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'salary-enhancement-letter': {
            'input-template': '../template/spectrum/salary-enhancement-letter/HR__salary-enhancement-letter-template__2022.odt',
            'output-dir': '../out/spectrum/salary-enhancement-letter',
            'output-file-pattern': 'spectrum__salary-enhancement-letter__2022__{0}__{1}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__salary-enhancement-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'separation-letter': {
            'input-template': '../template/spectrum/separation-letter/HR__separation-letter-template__2022.odt',
            'output-dir': '../out/spectrum/separation-letter',
            'output-file-pattern': 'spectrum__separation-letter__2022__{0}__{1}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__separation-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
        'transfer-letter': {
            'input-template': '../template/spectrum/transfer-letter/HR__transfer-letter-template__2022.odt',
            'output-dir': '../out/spectrum/transfer-letter',
            'output-file-pattern': 'spectrum__transfer-letter__2022__{0}__{1}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'spectrum__transfer-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
    },
    'celloscope' : {
        'salary-enhancement-letter': {
            'input-template': '../template/celloscope/salary-enhancement-letter/celloscope__salary-enhancement-letter-template__2022.odt',
            'output-dir': '../out/celloscope/salary-enhancement-letter',
            'output-file-pattern': 'celloscope__salary-enhancement-letter__2022__{0}__{1}.odt',
            'pdf-output-for-files': True,
            'merge-files': True,
            'merged-file-pattern': 'celloscope__salary-enhancement-letter__2022.odt',
            'pdf-output-for-merged-file': True,
        },
    },
}

''' authenticate to data service
'''
def authenticate_to_data_service(org, provider):
    google_data_connector_spec = DATA_CONNECTORS[org][provider]

    debug(f'{org} : authenticating with {provider}')
    client = connector_client(google_data_connector_spec)
    debug(f'{org} : authenticating with {provider} ... done')

    # wrap the connector in a data-connector object
    data_connector = {'client': client}

    return data_connector


''' acquire data from data source
'''
def acquire_data(org, source, data_connector):
    gsheet_data_source_spec = DATA_SOURCES[org][source]

    debug(f'{org} : acquiring data from {source}')
    values = gsheet_data(data_connector['client'], gsheet_data_source_spec)
    debug(f'{org} : acquiring data from {source} ... done')

    # wrap the data in a source-data object
    source_data = {'data': values}

    return source_data


''' process, transform, prepare data
'''
def process_data(org, data_processor, source_data):
    se_data_processor_spec = DATA_PROCESSORS[org][data_processor]

    raw_data = source_data['data']

    debug(f'{org} : processing data for [{data_processor}]')
    # the data is in a list (rows) of list (columns)
    data = []
    for row in raw_data:
        columns = {}
        # filter rows as specified
        if row[se_data_processor_spec['filter-column']] == se_data_processor_spec['filter-value']:
            for col_spec in se_data_processor_spec['columns']:
                columns[col_spec['key']] = row[col_spec['column']]

            data.append(columns)

    debug(f'{org} : processing data for [{data_processor}] ... done')

    # wrap the data in a processed-data object
    processed_data = {'data': data}

    return processed_data


''' generate documents from data
'''
def output_data(org, output_processor, processed_data):
    se_output_spec = DATA_SERIALIZERS[org][output_processor]

    data = processed_data['data']
    tmp_dir = se_output_spec['output-dir'] + '/tmp'

    # crete directories in case they do not exist
    os.makedirs(tmp_dir, exist_ok=True)

    debug(f'{org} : generating output for [{output_processor}]')

    # generate files for each data row
    temp_files = []
    for item in data:
        temp_file_path = tmp_dir + '/' + se_output_spec['output-file-pattern'].format(item['seq'], item['name'].lower().replace(' ', '-'))
        temp_files.append(temp_file_path)

        # generate the file
        replace_fields(se_output_spec['input-template'], temp_file_path, item)
        debug(f'.. {org} : generating odt for {item["name"]} ... done')

        # generate pdf if instructed to do so
        if se_output_spec['pdf-output-for-files']:
            debug(f'.. {org} : generating pdf from {temp_file_path}')
            generate_pdf(temp_file_path, tmp_dir)
            debug(f'.. {org} : generating pdf from {temp_file_path} ... done')

    # merge files if instructed to do so
    if se_output_spec['merge-files']:
        output_file_path = se_output_spec['output-dir'] + '/' + se_output_spec['merged-file-pattern'].format()
        debug(f'{org} : merging odt files')
        merge_files(temp_files, output_file_path)
        debug(f'{org} : merging odt files ... done')

    # generate pdf if instructed to do so
    if se_output_spec['pdf-output-for-merged-file']:
        debug(f'{org} : generating pdf from merged odt')
        generate_pdf(output_file_path, se_output_spec["output-dir"])
        debug(f'{org} : generating pdf from merged odt ... done')

    debug(f'{org} : generating output for [{output_processor}] ... done')

    return
