#!/usr/bin/env python3

import sys 

def isUserExist(userAddress,eBlocBroker=None, web3=None): #{
    if eBlocBroker is None and web3 is None:
        import os 
        sys.path.insert(1, os.path.join(sys.path[0], '..')) 
        from imports import connectEblocBroker
        from imports import getWeb3
        web3        = getWeb3() 
        eBlocBroker = connectEblocBroker(web3)
        
    userAddress = web3.toChecksumAddress(userAddress) 
    return eBlocBroker.functions.isUserExist(userAddress).call() 

if __name__ == '__main__':
    if len(sys.argv) == 2:
        userAddress = str(sys.argv[1]) 
    else:
        userAddress = "0x4E4A0750350796164d8defc442a712b7557BF282"  #POA
        # userAddress = "0x8642AF57Dc56d577276B5D6Bdb123ece429f093b"  #POW
    print(isUserExist(userAddress))   
