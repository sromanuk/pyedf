#!/usr/bin/env python
# encoding: utf-8

"""
pyedf.py

Created by Slavik Romanuk on 2011-04-30.
Copyright (c) 2011 Slavik Romanuk. All rights reserved.
"""

import re

def parse_int(string):
        data = re.findall(r'(\d+)', string)[0]
        return int(data)
        
def parse_float(string):
        data = re.findall(r'(\d+)', string)[0]
        return float(data)