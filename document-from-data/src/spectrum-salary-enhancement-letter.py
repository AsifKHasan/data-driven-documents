#!/usr/bin/env python3
'''
    generate templated salary enhancement document (letter) from data
'''

from helper.document_template import *


''' generate documents from data
'''
def post_process_data(processed_data):
    # data = processed_data['data']

    for item in processed_data['data']:
        print(item)
        if item["promotion"] == 'yes':
            item["promotion"] = ' with promotion'
        else:
            item["promotion"] = ''
            item["grade"] = item["currentgrade"]

    # wrap the data in a processed-data object
    # processed_data = {'data': data}

    return processed_data


if __name__ == '__main__':
    # get the appropriate data-connector
    data_connector = authenticate_to_data_service('google')

    # get raw data from source
    source_data = acquire_data('spectrum-salary-enhancement', data_connector)

    # get processed data from the raw data
    processed_data = process_data('spectrum-salary-enhancement', source_data)

    # post process data
    processed_data = post_process_data(processed_data)

    # serialize final output from data
    output_data('spectrum-salary-enhancement', processed_data)
