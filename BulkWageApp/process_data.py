import pandas as pd
from transmitter import Transmitter


def write_first_line(transmitter, report):
    open(report, 'a')


def ingest_data(filename, report_file):
    company = pd.read_csv(filename, nrows=1, usecols=[0, 1], names=['Company', 'UBI'])
    totals = pd.read_csv(filename, usecols=[3, 4], names=['wages', 'pfml']).tail(2).head(1)

    whole_file = pd.read_csv(filename, usecols=[0, 1, 2, 3, 4], names=['Full Name', 'SSN', 'Hours', 'Wages', 'PFML'], skiprows=2)
    employees = whole_file.head(len(whole_file) - 2)
    # print('Totals:\n', totals)
    # print('Employees:\n', employees)

    return employees['PFML'].sum()


