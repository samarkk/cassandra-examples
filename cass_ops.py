import pandas as pd
import datetime

from cassandra.cluster import Cluster
from datetime import datetime
from os import path

clustter_ip = '127.0.0.1'
cluster = Cluster([clustter_ip])
session = cluster.connect()

user_rows = session.execute('''
select * from my_keyspace.user
''')

[(x.first_name, x.last_name) for x in user_rows.current_rows]

fo_file_location = 'D:/findataf/201819/fo/fo01JAN2018bhav.csv'
test_cass_df = pd.read_csv(fo_file_location)

test_cass_df.columns

test_cass_df.loc[:3, ['SYMBOL', 'EXPIRY_DT', 'INSTRUMENT', 'TIMESTAMP',
                      'OPTION_TYP', 'CLOSE', 'OPEN_INT']]

month_dict = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10,
              'NOV': 11, 'DEC': 12}

def convertStringToDateTime(x):
    dt = int(x[:2])
    mnth = month_dict[x[3:6]]
    year = int(x[7:11])
    return datetime(year, mnth, dt, 0, 0, 0)


convertStringToDateTime('31-OCT-2018')

month_str_dict = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
                  'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}


def tstoDate(x):
    dt = int(x[:2])
    mnth = month_str_dict[x[3:6]]
    year = int(x[7:11])
    return x[7:11] + '-' + mnth + '-' + x[:2]


print(tstoDate('31-OCT-2019'))

test_df_rows = test_cass_df.shape[0]

test_df_rows

for x in range(10):
    print(test_cass_df.loc[x, 'SYMBOL'], ',', test_cass_df.loc[x, 'INSTRUMENT'], ',',
          convertStringToDateTime(test_cass_df.loc[x, 'TIMESTAMP']))

cm_create_tbl_sttmnt = '''
    CREATE TABLE IF NOT EXISTS FINKS.CMTABLE(
        SYMBOL TEXT,
        SERIES TEXT,
        CPR DECIMAL,
        QTY INT,
        VLU DECIMAL,
        TRDATE DATE,
        TSTAMP TIMEUUID,
        PRIMARY KEY (SYMBOL, TRDATE)
    )
'''
session.execute(cm_create_tbl_sttmnt)

month_str_dict

mno_to_mname_dict = {v: k for k, v in month_dict.items()}
mno_to_mname_dict

cm_base_path = '/home/samar/data/201819/cm/cm'

mno = 1
yno = 2018
mnostr = ''
# print(month_dict)
# for x in os.walk('/home/samar/Downloads/201819/cm'):
#     print (x)
while yno < 2020:
    while mno < 13:
        for x in range(1, 32):
            if x < 10:
                datestr = '0' + str(x)
            else:
                datestr = str(x)
            mname = mno_to_mname_dict[mno]
            fnameToCheck = cm_base_path + datestr + mname + str(yno) + 'bhav.csv'
            if path.exists(fnameToCheck):
                for lno, line in enumerate(open(fnameToCheck)):
                    vals = line.split(',')
                    if lno != 0:
                        single_entry_command = '''
                            insert into finks.cmtable(symbol, series, trdate, cpr, qty, vlu, tstamp)
                            values ('{}', '{}', '{}', {}, {}, {}, now())
                        '''.format(vals[0], vals[1], tstoDate(vals[10].upper()), vals[5], vals[8],
                                   vals[5], vals[8])
                        session.execute(single_entry_command)
                        print(fnameToCheck, lno, 'written')
        mno += 1
    yno += 1
