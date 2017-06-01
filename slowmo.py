#!/usr/bin/python

# monitor the sync latency for a replica set
import sys, datetime, pymongo, time

# TODO: need to assert that the protocol is 1

usage = "./slowmo.py <host_ip> <host_port> <rs_id> <time_span(min)> \
<sampling_interval(s)> <output_file>\n"

def main(ip, port, rsid, span, it, output):
    client = pymongo.MongoClient(ip, int(port))
    span = 60*int(span) # calculate the total monitor time in seconds
    it = int(it)
    rsinfo = client['local']['system.replset']  # find the collection
                                                # containing the replset info
    box = []
    for i in range(0, span/it):
        mm = rsinfo.find_one( { '_id' : rsid } )['members']
        s = ''
        for m in mm:
            s = s + str(m['slaveDelay']) + ' '
        box.append(s)
        time.sleep(it)
    fo = open(output, 'w')
    for i in box:
        fo.write(i+'\n')
    fo.close()

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print usage
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],\
        sys.argv[6])
