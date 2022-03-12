#!/usr/bin/env python3

from odf import table, text

from pprint import pprint

from helper.openoffice.odf_helper import *

# ODT_PATH = "/home/asif/projects/asif@github/data-driven-documents/document-from-data/out/sscl/issued-invoice/tmp/sscl__issued-invoice__2022__0001.odt"
ODT_PATH = "D:/projects/asif@github/data-driven-documents/document-from-data/out/sscl/issued-invoice/tmp/sscl__issued-invoice__2022__0001.odt"

TABULAR_DATA = [
    {
        'table_name': 'TableItem',
        'rows_for_data': (2, 11),
        'column_map': {
            'seq': 0,
            'item': 1,
            'uom': 2,
            'qty': 3,
            'unitprice': 4,
            'itemtotal': 5,
        },
        'data_map': [
            {'seq': '01', 'item': 'IT Support Service and Software Maintenance', 'uom': 'Job', 'qty': '1', 'unitprice': '8,724,769.94', 'itemtotal': '8,724,769.94'},
            {'seq': '02', 'item': 'xyz', 'uom': 'Lot', 'qty': '2', 'unitprice': '3,000.00', 'itemtotal': '6,000.00'},
            {'seq': '03', 'item': 'pqr', 'uom': 'Pcs', 'qty': '100', 'unitprice': '500.00', 'itemtotal': '50,000.00'},
        ],
    },
]


if __name__ == '__main__':

    # open the odt
    odt = load_document(ODT_PATH)

    for tabular_date in TABULAR_DATA:
        table_name = tabular_date["table_name"]

        # get the table
        tbl = get_table(odt, table_name)

        if tbl is None:
            print(f'Table {table_name} not found')
            # return

        # get number of rows
        print(f'Table {table_name} has {number_of_rows(tbl)} rows')

        # put values in rows and columns
        rows_not_populated = populate_table(tbl, tabular_date["rows_for_data"], tabular_date["column_map"], tabular_date["data_map"])

        # remove unnecesary rows - from current_row_index to data_end_at_table_row
        remove_rows(tbl, rows_not_populated)

    # save odt
    save_document(odt, ODT_PATH)
