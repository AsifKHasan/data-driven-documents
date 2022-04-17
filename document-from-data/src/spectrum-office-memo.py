#!/usr/bin/env python3
'''
    generate templated office memo from data
'''

from helper.document_template import *


if __name__ == '__main__':
    provider = 'google'
    org = 'spectrum'
    document = 'office-memo'

    # get the appropriate data-connector
    data_connector = authenticate_to_data_service(org, provider)

    # get raw data from source
    source_data = acquire_data(org, document, data_connector)

    # get processed data from the raw data
    processed_data = process_data(org, document, source_data)

    # serialize final output from data
    output_data(org, document, processed_data)
