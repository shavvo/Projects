#!/usr/bin/python

import json
import sqlite3
from datetime import timedelta
from contextlib import contextmanager
import sith

data = sith.Sith().process_smart_data()

def create_columns():
    columns = []
    for key in data.values()[0].keys():
        key = [i.replace("-", "_") for i in key]
        key = "".join(key)
        col = ",".join(["_%s VARCHAR(40)" % key])
        columns.append(col)
    return columns

def create_values():
    values = []
    for val in data.values():
        values.append(val.values())
    return values

create_query = "CREATE TABLE IF NOT EXISTS drivedata({0});"
create_query = create_query.format(", ".join(create_columns()))

@contextmanager
def smartdata_db():
    conn = sqlite3.connect('/home/aballens/sith/smartdata2.db')
    conn.execute(create_query)
    conn.commit()
    yield conn
    conn.close()


def insert_smartdata():
    columns = []
    for key in data.values()[0].keys():
        key = [i.replace("-", "_") for i in key]
        key = "".join(key)
        col = ",".join(["_%s" % key])
        columns.append(col)

    for item in create_values():
        item = ", ".join('"'+str(id)+'"' for id in item)
        insert_query =  "insert into drivedata({0}) VALUES ({1})"
        insert_query = insert_query.format(", ".join(columns), item)
        with smartdata_db() as conn:
            conn.execute(insert_query)
            conn.commit()

if __name__ == '__main__':
    insert_smartdata()
