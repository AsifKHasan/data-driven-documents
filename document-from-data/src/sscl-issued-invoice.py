#!/usr/bin/env python3
'''
    generate templated issued invoice from data
'''

import num2words
from helper.document_template import *

''' post process document data
'''
def post_process_data(processed_data):
    for item in processed_data['data']:
        item['totalinwords'] = num2words.num2words(item['invoicetotal'].replace(',', ''), to='currency', lang='en_IN').replace('euro', 'taka').replace('cents', 'paisa')

    if 'tabular_data' in processed_data['data_processor']:
        for i in range(0, len(processed_data['data_processor']['tabular_data'])):
            # sample test data
            data_map = [
                        {'seq': '01', 'item': 'IT Support Service and Software Maintenance', 'uom': 'Job', 'qty': '1', 'unitprice': '8,724,769.94', 'itemtotal': '8,724,769.94'},
                        {'seq': '02', 'item': 'xyz', 'uom': 'Lot', 'qty': '2', 'unitprice': '3,000.00', 'itemtotal': '6,000.00'},
                        {'seq': '03', 'item': 'pqr', 'uom': 'Pcs', 'qty': '100', 'unitprice': '500.00', 'itemtotal': '50,000.00'},
                    ]

            processed_data['data_processor']['tabular_data'][i]['data_map'] = data_map

    return processed_data


if __name__ == '__main__':
    org = 'SSCL'
    provider = 'google'
    document = 'issued-invoice'

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
