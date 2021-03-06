#!/usr/bin/env python3

import sys, os

def getClusterAddresses(eBlocBroker=None):
    if eBlocBroker is None: 
        sys.path.insert(1, os.path.join(sys.path[0], '..')) 
        from imports import connectEblocBroker
        eBlocBroker = connectEblocBroker()

    if eBlocBroker == 'notconnected':
        return eBlocBroker
    return eBlocBroker.functions.getClusterAddresses().call() 

if __name__ == '__main__':
    clusterList = getClusterAddresses()
    if clusterList == 'notconnected':
        print(clusterList)
        sys.exit()
    
    for i in range(0, len(clusterList)):
        print(clusterList[i])
