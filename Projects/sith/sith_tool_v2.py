#!/usr/bin/python

import json
import sqlite3
from contextlib import contextmanager
import sith


data_table = '''
CREATE TABLE IF NOT EXISTS prefail_drivedata
(serial VARCHAR(40),
 reallocated_event_cnt INTEGER,
 reallocated_sect_cnt INTEGER,
 current_pending_sect INTEGER,
 offline_uncorrectable INTEGER,
 CreateDate timestamp default (strftime('%s', 'now')));

CREATE TABLE IF NOT EXISTS all_drivedata
(serial VARCHAR(40),
 attribute_name VARCHAR(40),
 attribute_value VARCHAR(40),
 CreateDate timestamp default (strftime('%s', 'now')));
'''

data = sith.Sith().process_smart_data()

@contextmanager
def smartdata_db():
    conn = sqlite3.connect('/home/aballens/sith/smartdata3.db')
    conn.executescript(data_table)
    conn.commit()
    yield conn
    conn.close()


def insert_smartdata():
    with smartdata_db() as conn:
        for key, val in data.iteritems():
            for attr, rval in val.iteritems():
                #insert all data into DB
                conn.execute("insert into all_drivedata(serial, attribute_name, "
                             "attribute_value) VALUES (?, ?, ?)",
                             (key, attr, rval))
                conn.commit()


            if int(val['Reallocated_Event_Count']) != 0 or \
                int(val['Reallocated_Sector_Ct']) != 0 or \
                int(val['Current_Pending_Sector']) != 0 or \
                int(val['Offline_Uncorrectable']) != 0:
                    conn.execute("insert into prefail_drivedata(serial, reallocated_event_cnt, "
                                 "reallocated_sect_cnt, current_pending_sect, offline_uncorrectable) "
                                 "VALUES (?, ?, ?, ?, ?)",
                                 (key, int(val['Reallocated_Event_Count']),
                                  int(val['Reallocated_Sector_Ct']),
                                  int(val['Current_Pending_Sector']),
                                  int(val['Offline_Uncorrectable'])))
                    conn.commit()


if __name__ == '__main__':
    insert_smartdata()
