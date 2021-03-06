import os, time, math, random, sys
from random import randint

from os.path import expanduser
home = expanduser("~")

sys.path.append(home + "/eBlocBroker")
sys.path.insert(0, './contractCalls') 
from contractCalls.submitJob   import submitJob
from contractCalls.blockNumber import blockNumber


def log(strIn, path): #{
   print(strIn)
   txFile = open(path + '/clientOutput.txt', 'a'); 
   txFile.write( strIn + "\n" ); 
   txFile.close();
#}

def testFunc(path, readTest, workloadTest, testType, clusterID): #{
  jobKeyNum = {} #create a dictionary called jobKeyNum
  lineNumCounter = 0;
  with open(path + '/' + readTest) as test: #{
      for line in test: #{
          jobKeyNum[lineNumCounter] = line.rstrip(); # Assign value to key counter.
          lineNumCounter += 1
      #}
  #}
  
  f            = open(path + "/" + workloadTest); #put fixed file name.
  line1        = f.readline();
  line1_in     = line1.split(" ")
  counter      = 0;
  printCounter = counter;
  skippedLines = 0;

  while True: #{
    if counter >= 0:
        if counter >= (len(jobKeyNum)-1): #{
           log("Exceed hashOutput.txt's limit Total item number: " + str(len(jobKeyNum)), path)
           break;
        #}
        line2          = f.readline();
        line2_splitted = line2.split(" ")
        jobKey = jobKeyNum[counter].split(" ");

        if str(jobKey[1]) != '0' and (line2_splitted[0] != line2_splitted[1]) and (int(jobKey[2]) != 0): # Requested core shouldn't be 0.
           if not line2:
              break;  # EOF
           line2_in = line2.split(" ")
           sleepTime = str(int(line2_in[0]) -  int(line1_in[0])); # time to sleep in seconds

           blockNumber = blockNumber()
           log("\n------------------------------------------", path)
           log("Job: " + str(counter-skippedLines) + "| Current Time: " + time.ctime() +"| BlockNumber: " + blockNumber, path);
           log("Nasa Submit range: " + line2_splitted[0] + " " + line2_splitted[1], path)
           log("Sleep Time to submit next job: " + sleepTime, path)

           eudatFlag = 0;
           if (testType == 'eudat'):
              storageID = 1;
           elif (testType == 'eudat-nas'):
              storageID = 1;
              eudatFlag = 1;
           elif (testType == 'ipfs'):
              storageID = 0;
           elif (testType == 'ipfsMiniLock'):
              storageID = 2;
           elif (testType == 'gdrive'):
              storageID = 4;
              
           jobKey = str(jobKey[0]);
           coreNum  = int(jobKey[2])
           jobDescription = 'Science';

           if eudatFlag == 0:
              coreMinuteGas = int(math.ceil(float(jobKey[1]) / 60));           
              log("RunTimeInMinutes: " + str(val), path)
           else:
              log("RunTimeInMinutes: " + '360', path)
              coreMinuteGas   = 360 # 6 hours for nasEUDAT simulation test.
           
           accountID = randint(0, 9);

           log("hash: " + jobKey[0] + "| TimeToRun: " + str(coreMinuteGas) + "| Core: " + str(coreNum) + "| accountID: " + str(accountID), path)

           sourceCodeHash     = '00000000000000000000000000000000'
           log('submitJob(' + clusterID + ', ' + jobKey + ', ' + str(coreNum) + ', ' + str(coreMinuteGas) + ', ' + jobDescription + ', ' + str(storageID) + ', ' + sourceCodeHash + ', ' + str(accountID) + ')', path)
           tx = submitJob(clusterID, jobKey, coreNum, coreMinuteGas, jobDescription, storageID, sourceCodeHash, accountID);                     
           log(tx, path)

           txFile     = open(path + '/' + clusterID + '.txt', 'a');
           txFile.write(tx + " " + str(accountID) + "\n");
           txFile.close();

           sleepSeconds = int(sleepTime);
           for remaining in range(sleepSeconds, 0, -1): #{
              sys.stdout.write("\r")
              sys.stdout.write("{:2d} seconds remaining...".format(remaining))
              sys.stdout.flush()
              time.sleep(1)
           #}

           sys.stdout.write("\rSleeping is done!               \n")
           line1    = line2;
           line1_in = line2_in;
        else:
           skippedLines = skippedLines + 1;
    else: #{
       line1   = f.readline();
       line1_in = line1.split(" ")
    #}
    counter += 1;
  #}
  log("END");
  log(".");
  f.close();
#}
