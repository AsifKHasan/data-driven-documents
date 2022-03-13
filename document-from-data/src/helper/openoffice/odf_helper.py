#!/usr/bin/env python3

from odf.opendocument import load
from odf import table, text
from odf.text import P

from helper.logger import *

''' load an open document file
'''
def load_document(document_path):
    doc = load(document_path)
    return doc


''' save an open document file
'''
def save_document(doc, document_path):
    doc.save(document_path)


''' get a named table from an odt
'''
def get_table(doc, table_name):
    all_tables = doc.getElementsByType(table.Table)

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
    return len(tbl.getElementsByType(table.TableRow))


''' populate table with data
'''
def populate_table(tbl, rows_for_data, columns, data_map):
    table_name = tbl.getAttribute('name')
    table_rows = tbl.getElementsByType(table.TableRow)
    data_start_at_table_row = rows_for_data[0]
    data_end_at_table_row = rows_for_data[1]

    # iterate over data list
    current_row_index = data_start_at_table_row
    data_item_count = 0
    for data_item in data_map:
        data_item_count = data_item_count + 1
        debug(f"populating data [{data_item_count}] in table {table_name} row [{current_row_index}]")

        # get the cells for the current row
        row_cells = table_rows[current_row_index].getElementsByType(table.TableCell)

        # each data_item is a dict
        for k, v in data_item.items():
            # from the key we know in which column the value to put
            for column in columns:
                if column['key'] == k:
                    column_index = column['cell']

                    cell = row_cells[column_index]

                    # get the first para of the cell
                    paras = cell.getElementsByType(text.P)
                    paras[0].addText(v)
                    pass

        current_row_index = current_row_index + 1

    return (current_row_index, data_end_at_table_row)


''' remove rows from a table
'''
def remove_rows(tbl, rows_to_remove):
    start_row_index, ends_at_row = rows_to_remove[0], rows_to_remove[1]
    table_name = tbl.getAttribute('name')
    table_rows = tbl.getElementsByType(table.TableRow)
    if ends_at_row < start_row_index:
        debug(f"no rows to remove from table {table_name} : rows {start_row_index}-{ends_at_row}")
    else:
        for i in range(start_row_index, ends_at_row + 1):
            table_row = table_rows[i]
            table_row.parentNode.removeChild(table_row)
            debug(f"rows {i} removed from table {table_name}")
