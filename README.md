# tabulate.py
Pretty print tables.

Example:
--------
    $ python -c 'import tabulate; tabulate.dumplol([[1,2,3,4,5], ["one", "two", "three"], ["a", "b", "c", "d"]])'
    +------+------+-------+------+------+
    | col0 | col1 | col2  | col3 | col4 |
    +------+------+-------+------+------+
    |  1   |  2   |   3   |  4   |  5   |
    +------+------+-------+------+------+
    | one  | two  | three | N/A  | N/A  |
    +------+------+-------+------+------+
    |  a   |  b   |   c   |  d   | N/A  |
    +------+------+-------+------+------+




