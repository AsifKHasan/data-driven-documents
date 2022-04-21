#!/usr/bin/env python3
'''
    generate templated separation letter from data
'''

from helper.document_template import *

if __name__ == '__main__':
    org = 'spectrum'
    unit = 'hrm'
    provider = 'google'
    document = 'separation-letter'

    # get the appropriate data-connector
    data_connector = authenticate_to_data_service(org, provider)

    # get raw data from source
    source_data = acquire_data(org, unit, document, data_connector)

    # get processed data from the raw data
    processed_data = process_data(org, unit, document, source_data)

    # serialize final output from data
    output_data(org, unit, document, processed_data)
