#!/usr/bin/python

# monitor the sync latency for a replica set
import sys, datetime, pymongo, time

# TODO: need to assert that the protocol is 1

usage = "./slowmo.py <connection_uri> <time_span(min)> \
<sampling_interval(s)> <output_file>\n"

starttime = time.time()

class AbnormalState(Exception):
    def __init__(self, message):
        self.message = message

def main(uri, span, it, output):
    client = pymongo.MongoClient(uri)
    span = 60*int(span) # calculate the total monitor time in seconds
    it = int(it)
    mm = client.admin.command("replSetGetStatus")['members']
    n = len(mm)     # the number of replicas in the set
    box = []
    for i in range(0, span/it):
        start = time.time()
        mm = client.admin.command("replSetGetStatus")['members']
        try:
            box.append(get_lag(mm))
        except AbnormalState:
            # flush the good data
            fo = open(output, 'w')
            for i in box:
                fo.write(i+'\n')
            fo.close()
        time.sleep(it - (time.time() - start))
    fo = open(output, 'w')
    for i in box:
        fo.write(i+'\n')
    fo.close()

def get_lag(mm):    # return the replication lag of replicas as well as prim id
    n = len(mm)
    prim = -1
    for j in range(0,n):    # locate the primary
        if mm[j]['stateStr'] == 'PRIMARY':
            prim = j
            primt = mm[j]['optimeDate']
            break
        elif mm[j]['stateStr'] != 'SECONDARY':
            print "ALERT: member {} enters {} mode {} seconds from \
            begnining\n".format(j, mm[j]['stateStr'], time.time() - starttime)
            raise AbnormalState(mm[j]['stateStr'])
    assert prim >= 0, "LOST PRIMARY, MONITORING STOPS..."
    s = ""
    for j in range(0,n):
        s = s + str((primt - mm[j]['optimeDate']).total_seconds()) + ' '
    s = s + str(prim)
    return s

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print usage
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
