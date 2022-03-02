#!/usr/bin/env python3
'''
    generate templated transfer document (letter) from data
'''

from helper.document_template import *

if __name__ == '__main__':
    # get the appropriate data-connector
    data_connector = authenticate_to_data_service('google')

    # get raw data from source
    source_data = acquire_data('gsheet-transfer-letter', data_connector)

    # get processed data from the raw data
    processed_data = process_data('transfer-letter', source_data)

    # serialize final output from data
    output_data('transfer-letter', processed_data)
