from __future__ import with_statement
import argparse
import os
import sys
import errno

from fuse import FUSE, FuseOSError, Operations

class opuslayer(Operations):

    def __init__(self, rt_pt):
	self.rt_pt = rt_pt

    def getattr(self, rt_pt, fh=None):
        st = os.lstat(rt_pt)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, rt_pt, fh):
        dirents = ['.', '..']
        if os.path.isdir(rt_pt):
            dirents.extend(os.listdir(rt_pt))
        for r in dirents:
            yield r
            
    def open(self, rt_pt, flags):
        return os.open(rt_pt, flags)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

def main():
    praser = argparse.ArgumentParser(description = 'FUSE filesystem for transparently encoding to opus.')
    praser.add_argument('rt_pt', metavar='root_point', help='Location of the node to be layered.')
    praser.add_argument('mt_pt', metavar='mount_point', help='Node where transparent filesystem is to be mounted.')
    args = praser.parse_args()
    mt_pt = args.__dict__.pop('mt_pt')
    rt_pt = args.__dict__.pop('rt_pt')

    FUSE(opuslayer(rt_pt), mt_pt)

if __name__ == "__main__":
    main()
