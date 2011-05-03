#!/usr/bin/env python
# encoding: utf-8

"""
pyedf.py

Created by Ray Slakinski on 2010-09-14.
Copyright (c) 2010 Ray Slakinski. All rights reserved.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath( __file__ )))

import argparse
import re
import edfutils


class edfreader:
    header = {}
    records_header = {}
        
        
    def read_header(self, data):
        # Parse header information based on the EDF/EDF+ specs
        # http://www.edfplus.info/specs/index.html
        self.header['version'] = edfutils.parse_int(data[0:7].strip())
        self.header['patient_id'] = data[7:88].strip()
        self.header['rec_id'] = data[88:168].strip()
        self.header['startdate'] = data[168:176].strip()
        self.header['starttime'] = data[176:184].strip()
        self.header['header_bytes'] = edfutils.parse_int(data[184:192].strip())
        self.header['num_items'] = edfutils.parse_int(data[236:244].strip())
        self.header['data_duration'] = edfutils.parse_float(data[244:252].strip())
        self.header['num_signals'] = edfutils.parse_int(data[252:256].strip())
        return self.header
    
    
    def read_records_header(self, data):
        position = 256
        items_count = self.header['num_signals']
        
        for i in range (items_count):
            self.records_header[i] = {}
        
        for i in range (items_count):
            self.records_header[i]['leads_type'] = data[position:position+16].strip()
            position += 16
        
        for i in range (items_count):
            self.records_header[i]['electrodes_type'] = data[position:position+80].strip()
            position += 80
        
        for i in range (items_count):
            self.records_header[i]['dimension'] = data[position:position+8].strip()
            position += 8
            
        for i in range (items_count):
            self.records_header[i]['phisical_minimum'] = edfutils.parse_float(data[position:position+8])
            position += 8
            
        for i in range (items_count):
            self.records_header[i]['phisical_maximum'] = edfutils.parse_float(data[position:position+8])
            position += 8
            
        for i in range (items_count):
            self.records_header[i]['numeric_minimum'] = edfutils.parse_int(data[position:position+8])
            position += 8
            
        for i in range (items_count):
            self.records_header[i]['numeric_maximum'] = edfutils.parse_int(data[position:position+8])
            position += 8
        
        for i in range (items_count):
            self.records_header[i]['filters_params'] = data[position:position+80].strip()
            position += 80
            
        for i in range (items_count):
            self.records_header[i]['data_counter'] = edfutils.parse_int(data[position:position+8])
            position += 8
            
        return self.records_header
    
    
    def read_data_records(self, data):
        blocks_count = self.header['num_items']
        signal_count = self.header['num_signals']
        
        rec_pos = self.header['header_bytes']+1
        rec_size = 2
        
        for i in range (signal_count):
            self.records_header['data'] = []
        
        for block in range(blocks_count):
            for i in range(signal_count):
                self.records_header[i]['data'] = edfutils.parse_int(data[rec_pos:rec_pos+rec_size])
                rec_pos += rec_size
        return self.records_header


    def read_edf_file(self, fileobj):
        data = fileobj.read()
        
        self.header = self.read_header(data)
        self.records_header = self.read_records_header(data)
        self.read_data_records(data)
        
        return {'header': self.header, 'records_header': self.records_header}



def main():
    # create the parser
    parser = argparse.ArgumentParser(description='Process a given EDF File.')
    parser.add_argument(
        '-f',
        '--file',
        type=argparse.FileType('r'),
        help='EDF File to be processed.',
    )
    
    args = parser.parse_args()
    parser = edfreader()
    data = parser.read_edf_file(args.file)
    args.file.close()
    print data

if __name__ == '__main__':
    main()
