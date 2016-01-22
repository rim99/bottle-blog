#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rim99'

from blogpost.manage import saveFile
import sys

print("file name：", sys.argv[0])
print("tag: ", i, sys.argv[1])

file = sys.argv[1]
category = sys.argv[2]

try:
    saveFile(file, category)
    print('Successfully posted')
except:
    print('Error when posting')

