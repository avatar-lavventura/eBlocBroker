#!/usr/bin/env python

from imports import *

if __name__ == '__main__': #{
    if(len(sys.argv) == 2):
        clusterAddress = str(sys.argv[1]);
    else:        
        clusterAddress = "0x4e4a0750350796164D8DefC442a712B7557BF282"; #POA
        # clusterAddress = "0x6af0204187a93710317542d383a1b547fa42e705"; #POW

    clusterAddress = web3.toChecksumAddress(clusterAddress);
    
    if str(eBlocBroker.functions.isClusterExist(clusterAddress).call()) == "False":
        print("Cluster is not registered. Please try again with registered Ethereum Address as cluster.")
        sys.exit();

    blockReadFrom, coreNumber, coreMinutePrice = eBlocBroker.functions.getClusterInfo(clusterAddress).call();
    my_filter = eBlocBroker.eventFilter('LogCluster',{'fromBlock': int(blockReadFrom),'toBlock': int(blockReadFrom) + 1})
           
    print('{0: <17}'.format('blockReadFrom: ')   + str(blockReadFrom));
    print('{0: <17}'.format('coreNumber: ')      + str(coreNumber));
    print('{0: <17}'.format('coreMinutePrice: ') + str(coreMinutePrice));
    print('{0: <17}'.format('clusterEmail: ')    + my_filter.get_all_entries()[0].args['clusterEmail']);
    print('{0: <17}'.format('miniLockID: ')      + my_filter.get_all_entries()[0].args['miniLockID']);
    print('{0: <17}'.format('ipfsAddress: ')     + my_filter.get_all_entries()[0].args['ipfsAddress']);   
    print('{0: <17}'.format('fID: ')             + my_filter.get_all_entries()[0].args['fID']);
    print('.');
#}
