#!/usr/bin/env python3

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from imports import connectEblocBroker
from imports import getWeb3
    
def updateCluster():
    web3        = getWeb3() 
    eBlocBroker = connectEblocBroker(web3)
    # USER Inputs----------------------------------------------------------------
    account            = web3.eth.accounts[0]  # Cluster's Ethereum Address
    coreNumber         = 128 
    clusterEmail       = "alper.alimoglu@gmail.com" 
    federationCloudId  = "ee14ea28-b869-1036-8080-9dbd8c6b1579@b2drop.eudat.eu" 
    miniLockId         = "9VZyJy1gRFJfdDtAjRitqmjSxPjSAjBR6BxH59UeNgKzQ" 
    corePriceMinuteWei = 100 
    ipfsAddress        = "/ip4/79.123.177.145/tcp/4001/ipfs/QmWmZQnb8xh3gHf9ZFmVQC4mLEav3Uht5kHJxZtixG3rsf" 
    # ----------------------------------------------------------------------------
    #os.environ['ipfs'] = ipfs 
    #ipfsID=os.popen('node bs58.js encode $ipfs').read().replace("\n", "") 
    #ipfsIDbytes = web3.toBytes(hexstr=ipfsID) 

    if len(federationCloudId) < 128 and len(clusterEmail) < 128 and (len(miniLockId) == 0 or len(miniLockId) == 45):
        tx = eBlocBroker.transact({"from":account, "gas": 4500000}).updateCluster(coreNumber, clusterEmail, federationCloudId, miniLockId, corePriceMinuteWei, ipfsAddress) 
        print('Tx_hash: ' + tx.hex()) 

if __name__ == '__main__':
    updateCluster()
