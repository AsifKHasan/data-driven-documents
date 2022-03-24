#!/usr/bin/env python3
'''
    generate templated claim adjustment from data
'''

import num2words
from helper.document_template import *

''' post process document data
'''
def post_process_data(processed_data):
    for item in processed_data['data']:
        item['claiminwords'] = num2words.num2words(item['claimtotal'].replace(',', ''), to='currency', lang='en_IN').replace('euro', 'taka').replace('cents', 'paisa')

        outstanding_float = float(item['outstanding'].replace(',', ''))
        if outstanding_float >= 0.00:
            item['payreceive'] = 'Pays'
        else:
            item['payreceive'] = 'Receives'
            item['outstanding'] = item['outstanding'].replace('-', '')

        item['outstandinginwords'] = num2words.num2words(item['outstanding'].replace(',', ''), to='currency', lang='en_IN').replace('euro', 'taka').replace('cents', 'paisa')

    return processed_data


if __name__ == '__main__':
    org = 'SSCL'
    provider = 'google'
    document = 'claim-adjustment'

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
