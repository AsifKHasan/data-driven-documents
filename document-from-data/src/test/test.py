#!/usr/bin/env python3

from odf.opendocument import load
from odf import table, text
from pprint import pprint

ODT_PATH = "/home/asif/projects/asif@github/data-driven-documents/document-from-data/out/sscl/issued-invoice/tmp/sscl__issued-invoice__2022__0001.odt"

TABULAR_DATA = {
    "table_name": "TableItem",
    "data_start_at_row": 2,
    "data_ends_at_row": 11,
    "column_map": {
        "seq": 0,
        "item": 1,
        "uom": 2,
        "qty": 3,
        "unitprice": 4,
    },
    "data": [
        {"seq": 1, "item": "IT Support Service and Software Maintenancec", "uom": "Job", "qty": "1", "unitprice": "8,724,769.94"},
        {"seq": 2, "item": "xyz", "uom": "Lot", "qty": "2", "unitprice": "3,000.00"},
        {"seq": 3, "item": "pqr", "uom": "Pcs", "qty": "100", "unitprice": "500.00"},
    ],
}


''' load and odt file
'''
def open_odt(odt_path):
    odt = load(odt_path)
    return odt


''' get a named table from an odt
'''
def get_table(odt, table_name):
    all_tables = odt.getElementsByType(table.Table)

    # get the specific table
    for t in all_tables:
        if hasattr(t, 'attributes'):
            t_name = t.getAttribute('name')
            if t_name == table_name:
                return t

    return None


''' get the number of rows of a table
'''
def number_of_rows(tbl):
    the_table_rows = the_table.getElementsByType(table.TableRow)
    return len(the_table_rows)


''' populate table with data
'''
def populate_table(tbl, tabular_data):
    table_name = tbl.getAttribute('name')
    table_rows = tbl.getElementsByType(table.TableRow)
    data_start_at_row = tabular_data["data_start_at_row"]
    data_ends_at_row = tabular_data["data_ends_at_row"]
    column_map = tabular_data["column_map"]

    # iterate over data list
    current_row_index = data_start_at_row
    data_item_count = 0
    for data_item in TABULAR_DATA["data"]:
        data_item_count = data_item_count + 1
        print(f"populating data [{data_item_count}] in table {table_name} row [{current_row_index}]")
        # each data_item is a dict
        for k, v in data_item.items():
            # from the key we know in which column the value to put
            column_index = column_map[k]
            # get the cell from row current_row_index and column_index

        current_row_index = current_row_index + 1

    return current_row_index, data_ends_at_row


''' remove rows from a table
'''
def remove_rows(tbl, start_row_index, ends_at_row):
    table_name = tbl.getAttribute('name')
    if ends_at_row < start_row_index:
        print(f"no rows to remove from table {table_name} : rows {start_row_index}-{ends_at_row}")
    else:
        # the_table_rows[8].parentNode.removeChild(the_table_rows[8])
        print(f"rows {start_row_index}-{ends_at_row} removed from table {table_name}")


if __name__ == '__main__':

    # open the odt
    odt = open_odt(ODT_PATH)

    table_name = TABULAR_DATA["table_name"]

    # get the table
    the_table = get_table(odt, table_name)

    if the_table is None:
        print(f'Table {table_name} not found')
        # return

    # get number of rows
    print(f'Table {table_name} has {number_of_rows(the_table)} rows')

    # put values in rows and columns
    current_row_index, data_ends_at_row = populate_table(the_table, TABULAR_DATA)

    # remove unnecesary rows - from current_row_index to data_ends_at_row
    remove_rows(the_table, current_row_index, data_ends_at_row)

    # save odt
    odt.save(ODT_PATH)
