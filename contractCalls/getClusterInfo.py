#!/usr/bin/env python3

import sys

def getClusterInfo(clusterAddress, eBlocBroker=None, web3=None): 
    if eBlocBroker is None and web3 is None: 
        import os
        sys.path.insert(1, os.path.join(sys.path[0], '..'))
        from imports import connectEblocBroker
        from imports import getWeb3
        web3        = getWeb3()
        eBlocBroker = connectEblocBroker(web3)

    clusterAddress = web3.toChecksumAddress(clusterAddress) 
    
    if str(eBlocBroker.functions.isClusterExist(clusterAddress).call()) == "False":
        print("Cluster is not registered. Please try again with registered Ethereum Address as cluster.")
        sys.exit() 

    blockReadFrom, coreNumber, priceCoreMin, priceDataTransfer = eBlocBroker.functions.getClusterInfo(clusterAddress).call() 
    my_filter = eBlocBroker.eventFilter('LogCluster',{ 'fromBlock': int(blockReadFrom),
                                                      'toBlock': int(blockReadFrom) + 1})
    '''
    my_filter = eBlocBroker.events.LogCluster.createFilter(
        fromBlock=int(blockReadFrom),       
        toBlock=int(blockReadFrom) + 1,
        argument_filters={'clusterAddress': str(clusterAddress)}
    )    
    loggedJobs = my_filter.get_all_entries()
    print(loggedJobs[0])
    '''
    # print(my_filter.get_all_entries()[0])
    
    return('{0: <19}'.format('blockReadFrom: ')    + str(blockReadFrom)  + '\n' +
           '{0: <19}'.format('coreNumber: ')       + str(coreNumber) + '\n' +
           '{0: <19}'.format('priceCoreMin: ')     + str(priceCoreMin)  + '\n' +
           '{0: <19}'.format('priceDataTransfer: ') + str(priceDataTransfer)  + '\n' +    
           '{0: <19}'.format('clusterEmail: ')     + my_filter.get_all_entries()[0].args['clusterEmail'] + '\n' +
           '{0: <19}'.format('miniLockID: ')       + my_filter.get_all_entries()[0].args['miniLockID'] + '\n' +
           '{0: <19}'.format('ipfsAddress: ')      + my_filter.get_all_entries()[0].args['ipfsAddress'] + '\n' +
           '{0: <19}'.format('fID: ')              + my_filter.get_all_entries()[0].args['fID'] + '\n' +
           '{0: <19}'.format('whisperPublicKey: ') + my_filter.get_all_entries()[0].args['whisperPublicKey']);

if __name__ == '__main__':
    if len(sys.argv) == 2:
        clusterAddress = str(sys.argv[1]) 
    else:        
        clusterAddress = "0x4e4a0750350796164D8DefC442a712B7557BF282"  #POA
        # clusterAddress = "0x6af0204187a93710317542d383a1b547fa42e705"  #POW
    print(getClusterInfo(clusterAddress))
