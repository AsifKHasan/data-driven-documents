#!/usr/bin/env python3
'''
    generate templated clearance certificate from data
'''

from helper.document_template import *


''' generate documents from data
'''
def post_process_data(processed_data):
    for item in processed_data['data']:
        if item["reason"] == 'discontinuation':
            item["reason"] = 'has been discontinued from the services of the company as decided by the management'
        elif item["reason"] == 'resignation':
            item["reason"] = 'has resigned from the services of the company which has been accepted by the management'

    return processed_data


if __name__ == '__main__':
    provider = 'google'
    org = 'spectrum'
    document = 'clearance-certificate'

    # get the appropriate data-connector
    data_connector = authenticate_to_data_service(org, provider)

    # get raw data from source
    source_data = acquire_data(org, document, data_connector)

    # get processed data from the raw data
    processed_data = process_data(org, document, source_data)

    # post process data
    processed_data = post_process_data(processed_data)

    # serialize final output from data
    output_data(org, document, processed_data)
