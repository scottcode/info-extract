""" Utilities for scraping tables from HTML documents
"""

import re

import pandas as pd


cell_regex = re.compile(r't[hd]')

def parse_row(row, func=lambda x: x):
    """Parse HTML 'row' node into a list of strings

    :param row: bs4.Tag instance for an HTML 'row' tag
    :param func: function to apply to the text of each cell
    :return:  list of strings
    """
    return [func(cell.get_text()) for cell in row.find_all(cell_regex)]

def parse_table(table, **kwds):
    """Parse a 'table' Tag object into a row-major list of lists

    :param table:  bs4.Tag instance representing a table
    :param kwds:
    :return:
    """
    return [parse_row(row, **kwds) for row in table.find_all('tr')]

def html_table_to_frame(table, ixs_row_labels=(), ixs_col_labels=(), **kwds):
    """Convert a BeautifulSoup table node to a pandas DataFrame

    :param table:   bs4.Tag instance for tag 'table'
    :param ixs_row_labels:   column indices that contain the row labels (as a tuple)
    :param ixs_col_labels:   row indices that contain the column labels (as a tuple)
    :param kwds:
    :return:  pandas.DataFrame instance
    """
    list_of_lists = parse_table(table, **kwds)
    col_headers = zip(*[list_of_lists[c] for c in ixs_col_labels])
    list_of_lists_filtered = [j for i, j in enumerate(list_of_lists) if i not in ixs_col_labels]
    if col_headers:
        df = pd.DataFrame.from_records(list_of_lists_filtered, columns=col_headers)
    else:
        df = pd.DataFrame.from_records(list_of_lists_filtered)

    if ixs_row_labels:
        return df.set_index([df.columns[r] for r in ixs_row_labels])
    else:
        return df