#!/usr/bin/env python3
'''
    generate templated contract renewal from data
'''

import num2words
from helper.document_template import *

''' post process document data
'''
def post_process_data(processed_data):
    for item in processed_data['data']:
        if item['currency'] == 'BDT':
            item['totalinwords'] = num2words.num2words(item['remuneration'].replace(',', ''), to='currency', lang='en_IN').replace('euro', 'taka').replace('cents', 'paisa')
        else:
            item['totalinwords'] = num2words.num2words(item['remuneration'].replace(',', ''), to='currency', lang='en_US').replace('euro', 'dollars')

    return processed_data


if __name__ == '__main__':
    org = 'SSCL'
    unit = 'hrm'
    provider = 'google'
    document = 'contract-renewal'

    # get the appropriate data-connector
    data_connector = authenticate_to_data_service(org, provider)

    # get raw data from source
    source_data = acquire_data(org, unit, document, data_connector)

    # get processed data from the raw data
    processed_data = process_data(org, unit, document, source_data)

    # post process data
    processed_data = post_process_data(processed_data)

    # serialize final output from data
    output_data(org, unit, document, processed_data)
