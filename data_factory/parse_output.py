#!/usr/bin/python

import sys

def main(fname, pn):
    fi = open(fname, 'r')
    lines = fi.readlines()
    fi.close()
    pn = int(pn)
    fs = [] # files of secondaries
    ss = [] # columns of secondaries
    sc = 0
    for i in range(0, len(lines[0].split())):   # create output files
        if i != pn:
            fs.append(open('secondary_'+str(sc),'w'))
            sc = sc + 1
            ss.append(i)
    for l in lines:
        a = l.split()
        assert len(a) == len(lines[0].split()), 'one of the row is broken, \
        %s!' % l
        sc = 0
        for s in ss:
            fs[sc].write(a[s] + '\n')
            sc = sc + 1
    for f in fs:
        f.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print 'please specify the file name and primary col number'
    else:
        main(sys.argv[1], sys.argv[2])
