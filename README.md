# slowmo
MongoDB sync delay monitor based on pymongo.

The key function implements the logic of mongo javascript function rs.printSlaveReplicationInfo(). 

To use it, simply type 
  ./slowmo.py <connection string> <monitoring length> <sampling_interval(s)> <output file> 
sampling interval is suggested to be 2 sec, since the default heartbeat interval is 2 sec, meaning the delay info is updated every 2 sec.
