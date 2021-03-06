# sheet-sql

[![Build](https://github.com/andyh1203/sheet-sql/workflows/ci/badge.svg)](https://github.com/andyh1203/sheet-sql/actions?workflow=ci)
[![Codecov](https://codecov.io/gh/andyh1203/sheet-sql/branch/master/graph/badge.svg)](https://codecov.io/gh/andyh1203/sheet-sql)
[![PyPI](https://img.shields.io/pypi/v/sheet-sql.svg)](https://pypi.org/project/sheet-sql/)
[![Read the Docs](https://readthedocs.org/projects/sheet-sql/badge/)](https://sheet-sql.readthedocs.io/)

sheet-sql allows for writing SQL-style queries to query data from Google Sheets.
It makes use of Google's Table Query (tq) Language. See [here](https://developers.google.com/chart/interactive/docs/querylanguage) for more details.

    >>> from sheetsql import connect
    >>> gs = connect("service_account")
    >>> gs.spreadsheets
    [<Spreadsheet 'Test' id:1z2917zfaUqeE9-fMn-XAUvDwzQ8Q_2rEXHRst5KZC3I>, <Spreadsheet 'my new spreadsheet' id:1I4pfBHYoY_ajW13Tn8t2-AyqmWK1HzcJPccyRUefdyw>]
    >>> spreadsheet = gs['1z2917zfaUqeE9-fMn-XAUvDwzQ8Q_2rEXHRst5KZC3I']
    >>> spreadsheet
    <Spreadsheet 'Test' id:1z2917zfaUqeE9-fMn-XAUvDwzQ8Q_2rEXHRst5KZC3I>
    >>> spreadsheet.worksheets
    ['Sheet1', 'Sheet2']
    >>> worksheet = spreadsheet['Sheet1']
    >>> worksheet
    <Worksheet 'Sheet1' id:0>
    >>> worksheet.columns
    ['test', 'test2', 'test3']
    >>> query = worksheet.query("SELECT *")
    <generator object Worksheet._result_handler.<locals>.<genexpr> at 0x7fe86c3c2840>
    >>> for row in query:
    ...   print(row)
    ...
    {'test': 1.0, 'test2': 6.0, 'test3': 11.0}
    {'test': 2.0, 'test2': 7.0, 'test3': 12.0}
    {'test': 3.0, 'test2': 8.0, 'test3': 13.0}
    {'test': 4.0, 'test2': 9.0, 'test3': 14.0}
    {'test': 5.0, 'test2': 10.0, 'test3': 15.0}
    >>> worksheet.default_row_type
    <class 'dict'>
    >>> worksheet.default_row_type = list
    >>> worksheet.default_row_type
    <class 'list'>
    >>> query = worksheet.query("SELECT *")
    >>> for row in query:
    ...   print(row)
    ...
    [1.0, 6.0, 11.0]
    [2.0, 7.0, 12.0]
    [3.0, 8.0, 13.0]
    [4.0, 9.0, 14.0]
    [5.0, 10.0, 15.0]

To install, run

    pip install sheet-sql

Alternatively, install with [poetry](https://python-poetry.org/)

    poetry add sheet-sql
