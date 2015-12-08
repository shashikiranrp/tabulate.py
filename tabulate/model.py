#!usr/bin/python

#
# Data structure to model Table
#

from common import log_msg

import sys

DEFAULT_NA_VALUE = "N/A"

class Table:
  
  #
  # self._columns = ["col1", "col2", ... , "coln"]
  # self.__column_defaults = {"col1": "val1", "col2": "val2", ... , "coln" : "valn"}
  # self._rows = {"rowkey1": {row1}, "rowkey2": {row2}, ... , "rowkeym" : {rowm}}
  #     rowi = {"col1" : "val1i", "col2" : "val2i", ... , "coln" : "valni"}
  #
  #
  # type of col,rowkey should be string
  # type of val can be anything
  #
  def __init__(self, columns = None, rows = None, column_defaults = None):
    self._columns = [] if columns is None else columns[:]
    self._column_defaults = dict([(col, DEFAULT_NA_VALUE) for col in self._columns]) if column_defaults is None else column_defaults
    self._rows = {} if rows is None else rows.copy()

    # verify state after init
    self._verify_state("init")

  def _verify_state(self, state_msg):
    # type invariants
    assert type(self._columns) == list, "after %s: columns should be a list" % state_msg
    assert all((type(col) == str for col in self._columns)), "after %s: each column should be string" % state_msg
    assert type(self._column_defaults) == dict, "after %s: column defaults should be a dictionary" % state_msg
    assert type(self._rows) == dict, "after %s: rows should be a dictionary" % state_msg
    assert all((type(row) == dict for row in self._rows.values())), "after %s: each row should be a dictionary" % state_msg
    assert all((type(rowkey) == str for rowkey in self._rows.keys())), "after %s: each row should be a dictionary" % state_msg

    # dimension invariants
    assert len(self._columns) == len(self._column_defaults), "after %s: too less column defaults!" % state_msg
    assert all((len(self._columns) == len(row) for row in self._rows.values())), "after %s: missing values for some columns in one or more rows!" % state_msg
    cols_set = set(self._columns)
    assert all((cols_set == set(row.keys()) for row in self._rows.values())), "after %s: invalid columns in some rows" % state_msg 


  def insert_column(self, index, column_name, row_vals = None, column_default_val = DEFAULT_NA_VALUE):
    # sanitize row_vals
    row_vals = {} if row_vals is None else row_vals

    # insert new column
    self._columns.insert(index, column_name)

    # add default value for the same
    self._column_defaults[column_name] = column_default_val

    # update for all other columns
    [row.update({column_name : row_vals.get(rowkey, column_default_val)}) for (rowkey, row) in self._rows.iteritems()]

    # verify the state
    self._verify_state("insert_column")


  def append_column(self, column_name, row_vals = None, column_default_val = DEFAULT_NA_VALUE):
    self.insert_column(len(self._columns), column_name, row_vals, column_default_val)

  def set_row(self, rowkey, row = None):
    row = {} if row is None else row
    # check for nay new columns and append them to the table
    [self.append_column(new_col) for new_col in set(row.keys()) - set(self._columns)]

    # add a new row
    self._rows[rowkey] = dict(((column_name, row.get(column_name, self._column_defaults.get(column_name))) for column_name in self._columns))

    # verify state
    self._verify_state("set_row with row_key: " + str(rowkey))

  def delete_column(self, column_name):
    if column_name in self._columns:
      # remove from column
      self._columns.remove(column_name)

      # remove the defualt entry
      del self._column_defaults[column_name]

      # pop all entries from all rows
      [row.pop(column_name) for row in self._rows.values()]

    self._verify_state("delete column => " + str(column_name))

  def delete_row(self, row_key):
    if self._rows.has_key(row_key):
      self._rows.pop(row_key)

    self._verify_state("delete row => " + str(row_key))

  def column_keys(self):
    return self._columns[:]
  
  def row_keys(self):
    return self._rows.keys()[:]

  def row(self, key):
    return self._rows[key].copy()

  # iter methods of the table
  def iter_row(self, row_key, action = lambda r_key, col, val : sys.stderr.write(str(val) + "\t")):
    if self._rows.has_key(row_key):
      return [action(row_key, col, val) for (col, val) in ((c, self._rows[row_key][c]) for c in self._columns)]

  def iter_column(self, column_name, action = lambda r_key, col, val : sys.stderr.write(str(val) + "\n")):
    if column_name in self._columns:
      return [action(row_key, column_name, row[column_name]) for (row_key, row) in self._rows.iteritems()]

  def iter_row_x_column(self, action = lambda r_key, col, val : sys.stderr.write(str(val) + "\t"), next_iter_action = lambda r_key: sys.stderr.write('\n')):
    for rowkey in self._rows.keys():
      next_iter_action(rowkey)
      self.iter_row(rowkey, action)

  def iter_column_x_row(self, action = lambda r_key, col, val : sys.stderr.write(str(val) + "\n"), next_iter_action = lambda col: sys.stderr.write('\n\n')):
    for column in self._columns:
      next_iter_action(column)
      self.iter_column(column, action)

  def __str__(self):
    return "COLUMNS: %s\nCOL_DEFAULTS: %s\nROWS: %s\n" % (str(self._columns), str(self._column_defaults), str(self._rows)) 

