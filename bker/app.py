#!/usr/bin/env python

import datetime
import os
import tarfile
import sys
import argparse

BK_DEST = "/var/local/bker/"
BK_SUCCESS = 0
BK_FAIL = 1

def build_name(root_name, comp_type, ts):
    if ts:
        return BK_DEST + root_name + '_' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.' + comp_type
    else:
        return BK_DEST + root_name + '.' + comp_type

def backup(src, name, comp_type):
    """Returns -1 if error, or size of resulting compressed file"""
    with tarfile.open(build_name(name, 'tar.' + comp_type), 'w:' + comp_type) as tar:
        tar.add(src)

parser = argparse.ArgumentParser(description='Backup Utility\n\tDefault target location = ' + BK_DEST)
parser.add_argument('src', type=str, help='target file or directory to backup')
parser.add_argument('name', type=str, help='name to give backup file')
parser.add_argument('-t', '--timestamp', help='add timestamp to end of filename')
parser.add_argument('-v', '--verbose', help='prints extra data about compression activity')
parser.add_argument('-c', '--compression-type', type=str, default='gz', help='compression type (gz, bz2, or xz)')
args = parser.parse_args()

try:
    if not os.path.isdir(BK_DEST):
        os.mkdir(BK_DEST)
except:
    print("Couldn't make storage directory " + BK_DEST)
    sys.exit(BK_FAIL)

try:
