#!/usr/bin/env python3

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import lib

def getJobInfo(clusterAddress, jobKey, index, eBlocBroker=None, web3=None):
    if eBlocBroker is None and web3 is None: 
        import os 
        sys.path.insert(1, os.path.join(sys.path[0], '..')) 
        from imports import connectEblocBroker
        from imports import getWeb3        
        web3        = getWeb3()
        if web3 == 'notconnected':
            return 'notconnected'
        eBlocBroker = connectEblocBroker(web3)
      
    clusterAddress = web3.toChecksumAddress(clusterAddress)
    job = None
    try:
        job = eBlocBroker.functions.getJobInfo(clusterAddress, jobKey, int(index)).call()
        jobDict = {'status':        job[0],
                   'core':          job[1],
                   'startTime':     job[2],
                   'received':      job[3],
                   'coreMinuteGas': job[4],
                   'jobOwner':      job[5]}
    except Exception as e:
        return e.__class__.__name__
        # return 'Exception: web3.exceptions.BadFunctionCallOutput'
    return jobDict

if __name__ == '__main__': 
    if len(sys.argv) == 4:
        clusterAddress = str(sys.argv[1]) 
        jobKey         = str(sys.argv[2]) 
        index          = int(sys.argv[3]) 
    else:
        clusterAddress = "0x4e4a0750350796164d8defc442a712b7557bf282" 
        # jobKey         = "153802737479941507912962421857730686964" 
        index          = 0
        jobKey         = 'QmRsaBEGcqxQcJbBxCi1LN9iz5bDAGDWR6Hx7ZvWqgqmdR' # Long job which only sleeps
        index          = 0
        
    jobInfo = getJobInfo(clusterAddress, jobKey, index)

    if str(jobInfo['core']) == '0':
        print('Out of index.')
        sys.exit()

    if type(jobInfo) is dict:        
        print('{0: <16}'.format('status:') + lib.inv_job_state_code[jobInfo['status']])
        print('{0: <16}'.format('status:') + str(jobInfo['status']))
        print('{0: <16}'.format('core') + str(jobInfo['core']))
        print('{0: <16}'.format('startTime') + str(jobInfo['startTime']))
        print('{0: <16}'.format('received:') + str(jobInfo['received']))
        print('{0: <16}'.format('coreMinuteGas:') + str(jobInfo['coreMinuteGas']))
        print('{0: <16}'.format('jobInfoOwner:') + jobInfo['jobOwner'])
    else:
        print(jobInfo)
