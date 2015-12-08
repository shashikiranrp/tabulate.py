#!/usr/bin/python

from model import Table

def t_print(table, \
            table_name = None, \
            footer_str = None, \
            corner = '+', \
            column_sep = '|', \
            row_sep = '-', \
            box_width = 0, \
            col_width_adjust = 2, \
            title_row_sep = '=', \
            show_col = False,\
            col_sort_function = None):
  # get the columns
  col_keys = table.column_keys()

  # sort the columns, if requested
  if col_sort_function is not None:
    col_keys.sort(cmp = col_sort_function)

  # calulate max width per column
  col_min_width_map = dict(((col, max(reduce(max, table.iter_column(col, lambda _, _1, v: len(str(v)))), len(col) if show_col else -1)) for col in col_keys))


  # get stateless lines
  inter_row_line = reduce(lambda acc, next_str : acc + next_str, map(lambda width: corner + row_sep * (width + col_width_adjust), map(col_min_width_map.get, col_keys)), "") + corner
  title_line = reduce(lambda acc, next_str : acc + next_str, map(lambda width: corner + title_row_sep * (width + col_width_adjust), map(col_min_width_map.get, col_keys)), "") + corner
  intra_row_line = reduce(lambda acc, next_str : acc + next_str, map(lambda width: column_sep + " " * (width + col_width_adjust), map(col_min_width_map.get, col_keys)), "") + column_sep

  # format for each row
  row_line = reduce(lambda acc, next_str : acc + next_str, map(lambda (col, width): column_sep + "{%s!s:^%ds}" % (col, width + col_width_adjust), map(lambda col: (col, col_min_width_map.get(col)), col_keys)), "") + column_sep
  
  # print the title
  if table_name is not None:
    print title_line
    print ("|{table_name:^%ds}|" % (len(inter_row_line) - 2)).format(table_name=table_name)
    print title_line
  else:
    print inter_row_line

  # show column names if requested
  if show_col:
    print row_line.format(**dict(((col, col) for col in col_keys)))
    print inter_row_line

  # print the rows
  for rowkey in table.row_keys():
    print row_line.format(**table.row(rowkey))
    print inter_row_line

  # print the footer
  if footer_str is not None:
    print ("|{footer:^%ds}|" % (len(inter_row_line) - 2)).format(footer=footer_str)
    print title_line

def dumpll(data, table_name = None, footer_str = None):
  t = Table()
  for (row_index, row) in enumerate(data):
    t.set_row('row' + str(row_index), dict(map(lambda (col_index, col_val): ('col' + str(col_index), col_val), enumerate(row))))

  t_print(t, table_name, footer_str, show_col = True, col_sort_function = lambda c1, c2: int(c1[3:]) - int(c2[3:]))
