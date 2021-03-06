#!/usr/bin/env python3

import sys

def authenticateORCID(orcID, eBlocBroker=None, web3=None):
    if eBlocBroker is None and web3 is None:
        import os;
        sys.path.insert(1, os.path.join(sys.path[0], '..'))
        from imports import connectEblocBroker
        from imports import getWeb3
        web3        = getWeb3()
        eBlocBroker = connectEblocBroker(web3)
    
    account = web3.eth.accounts[0]     
    if eBlocBroker.functions.isOrcIDVerified(orcID).call() == 0:
        tx = eBlocBroker.transact({"from":account, "gas": 4500000}).authenticateOrcID(orcID) 
        return('Tx_hash: ' + tx.hex()) 
    else:
        return('OrcID: ' + orcID + ' is already authenticated.')    
    
if __name__ == '__main__': 
    # USER Inputs----------------------------------------------------------------
    if len(sys.argv) == 2:
        orcID = str(sys.argv[1]) 
    else:
        orcID = '0000-0001-7642-0552'
    # ----------------------------------------------------------------------------
    print(authenticateORCID(orcID))
