# distributed-file-system
Distributed File System project in python

## Overview
File sharding in a distributed system requires careful planning and implementation to ensure proper functioning and fault tolerance. The methodology involves several steps, including analyzing the file, selecting a sharding algorithm, partitioning the file, assigning shards to nodes, replicating the shards, ensuring consistency, and accessing and retrieving the file. By following this methodology, a distributed system can efficiently store and retrieve large files while maintaining fault tolerance and scalability.

## How to run the code 
```
git clone https://github.com/Sanj24Dev/distributed-file-system.git
cd distributed-file-system
```
### For running the client:
```
cd client
```
* Change the dfc.conf file according to the systems used and run the python script
```
python dfc.py dfc.conf
```
### For running the server:
```
cd server1
```
* Change the dfs.conf file according to the systems used and run the python script
```
python dfs1.py 11000
```
