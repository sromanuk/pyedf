#!/usr/bin/env python
# encoding: utf-8
"""
pyedf.py

Created by Ray Slakinski on 2010-09-14.
Copyright (c) 2010 Ray Slakinski. All rights reserved.
"""
import sys
import getopt
import re


def read_edf_file(fileobj):
    data = fileobj.read()
    header = {}
    header['version'] = data[0:7].strip() # 8
    header['patient_id'] = data[7:88].strip() # 80
    header['rec_id'] = data[88:168].strip() # 80
    header['startdate'] = data[168:176].strip() # 8
    header['starttime'] = data[176:184].strip() # 8
    header['header_bytes'] = int(data[184:192].strip()) # 8
    header['num_items'] = int(data[236:244].strip())
    header['data_duration'] = float(data[244:252].strip())
    header['num_signals'] = int(data[252:256].strip())
    # more data 256 chars down. in header, but ignoring for now
    records = []
    records_a = records.append
    rec_pos = 512
    rec_size = 36
    # skip first rec
    rec_pos += rec_size
    for i in range(header['num_items']-1):
        record = {}
        record_split = data[rec_pos:rec_pos+rec_size].split('\x14')
        matches = re.findall(r'([\d]+)', record_split[2])
        record['type'] = record_split[3].strip()
        record['time'] = {
            'start': int(matches[0]),
            'durration': int(matches[1]),
        }
        records_a(record)
        rec_pos += rec_size
    return {'header': header, 'records': records}


def main():
    argv = sys.argv
    opts, args = getopt.getopt(argv[1:], "f", ["file="])
    # option processing
    for option, value in opts:
        if option == "-f" or option == '--file':
            f = open(value, 'r')
            data = read_edf_file(f)
            f.close()
            print data

if __name__ == '__main__':
    main()
