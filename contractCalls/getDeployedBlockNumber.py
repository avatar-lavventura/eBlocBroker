#!/usr/bin/env python3

import sys 

def getDeployedBlockNumber(eBlocBroker=None):
    if eBlocBroker is None: 
        import os 
        sys.path.insert(1, os.path.join(sys.path[0], '..')) 
        from imports import connectEblocBroker        
        eBlocBroker = connectEblocBroker() 

    return eBlocBroker.functions.getDeployedBlockNumber().call() 

if __name__ == '__main__':
    print(getDeployedBlockNumber())
    
