#!/usr/bin/env python
# encoding: utf-8

"""
pyedf.py

Created by Slavik Romanuk on 2011-04-30.
Copyright (c) 2011 Slavik Romanuk. All rights reserved.
"""

import re
import struct

def parse_int(string):
        try:
                string = string.strip()
                data = re.findall(r'(\d+)', string)[0]
                return int(data)
        except:
                try:
                        return int(string)
                except:
                        try:
                                if string.__len__() < 2:
                                        return struct.unpack(">b", string.strip())[0]
                                else:
                                        return struct.unpack(">h", string.strip())[0]
                        except:
                                return 0
        
        
def parse_float(string):
        try:
                return float(string.strip())
        except:
                parse_int(string.strip())