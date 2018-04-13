#!/usr/bin/env python

import sys, os, constants, time

def startCall( jobKey, index ): #{
   os.environ['eblocPath'] = constants.EBLOCPATH;
   os.environ['index']     = str(index);
   os.environ['jobKey']    = jobKey;
   statusId                = str(constants.job_state_code['RUNNING']);
   os.environ['statusId']  = statusId;   
   unixTime                = str(int(os.popen('date +%s').read()) + 1);
   os.environ['unixTime']  = unixTime;
   
   txHash = os.popen('node $eblocPath/eBlocBrokerNodeCall.js setJobStatus $jobKey $index $statusId $unixTime').read().rstrip('\n').replace(" ", "");
   
   while(True):
      if not(txHash == "notconnected" or txHash == ""): 
         break;      
      else:
         os.environ['unixTime'] = unixTime;
         txHash = os.popen('node $eblocPath/eBlocBrokerNodeCall.js setJobStatus $jobKey $index $statusId $unixTime').read().rstrip('\n').replace(" ", "");         
      time.sleep(5);
      
   txFile = open(constants.LOG_PATH + '/transactions/' + constants.CLUSTER_ID + '.txt', 'a');
   txFile.write(txHash + "| setJobStatus_started" +  " " + unixTime + "\n");
   txFile.close();
#}

if __name__ == '__main__': #{
   jobKey   = sys.argv[1];
   index    = sys.argv[2];
   startCall(jobKey, index);
#}
