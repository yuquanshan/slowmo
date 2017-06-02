#!/usr/bin/python

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys

# plot the first <span> minutes of latency, given a sampling interval
usage = './plot_the_latency.py <interval(s)> <span(m)> <plot_title> \
<fname1> [(optional)<fname2>...]'

def main(it, span, title, fnames):
    it = int(it)
    span = int(span)
    colorpool = ['red', 'blue', 'green', 'yellow', 'black']
    fc = 0     # file counter
    for fname in fnames:
        box = []
        fi = open(fname, 'r')
        lines = fi.readlines()
        fi.close()
        n = span*60/it
        count = 0
        for l in lines:
            count = count + 1
            if count > n:
                break;
            a = l.split()
            if len(a) > 0:
                box.append(float(a[0]))
        plt.plot(np.linspace(it,it*len(box),len(box)), \
        np.array(box), color=colorpool[fc], label='replica '+str(fc+1))
        fc = fc + 1

    plt.legend(loc = 'upper right')
    plt.xlabel('sec')
    plt.ylabel('replication delay (sec)')
    plt.title(title)
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print usage
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
