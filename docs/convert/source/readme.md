# How to Use eBlocBroker 

## About
**eBlocBroker** is a blockchain based autonomous computational resource broker.

- **Website:** [http://ebloc.cmpe.boun.edu.tr](http://ebloc.cmpe.boun.edu.tr) or [http://ebloc.org](http://ebloc.cmpe.boun.edu.tr).
- [Documentation](http://ebloc.cmpe.boun.edu.tr:3003/index.html).

## Build dependencies

[Geth](https://github.com/ethereum/go-ethereum/wiki/geth), [IPFS](https://ipfs.io/docs/install/), [Slurm](https://github.com/SchedMD/slurm).

## How to connect into Private Ethereum Blockchain (eBloc) 

- Connect into [eBlocPOA](https://github.com/ebloc/eblocPOA)
- Connect into [eBlocPOW](https://github.com/ebloc/eblocPOW)

## How to use eBlocBroker inside an Amazon EC2 Instance


An Amazon image (**AMI Name:** `eBloc`, **AMI ID:** `ami-f5c47f8a`) is also available that contains
`geth` setup to connect to our local Ethereum based blockchain system.  

### Create an Ethereum Account

**Creating an account:**

```bash
$ cd eblocPOA
$ eblocPath="$PWD"
$ geth --datadir="$eblocPath" account new
Your new account is locked with a password. Please give a password. Do not forget this password.
Passphrase:
Repeat passphrase:
Address: {a0a50a64cac0744dea5287d1025b8ef28aeff36e}
```

Your new account is locked with a password. Please give a password. Do not forget this password. Please enter a difficult passphrase for your account. 

You should see your `Keystore File (UTC / JSON)`under `keystore` directory. 

```bash
[~/eblocPOA]$ ls keystore
UTC--2018-02-14T10-46-54.423218000Z--a0a50a64cac0744dea5287d1025b8ef28aeff36e
```

**On the console, use:**

You can also create your Ethereum account inside your `geth-client`. Here your `Keystore File` will be created with root permission, `eBlocWallet` will not able to unlock it.

```bash
> personal.newAccount()
Passphrase:
Repeat passphrase:
"0x7d334606c71417f944ff8ba5c09e3672066244f8"
> eth.accounts
["0x7d334606c71417f944ff8ba5c09e3672066244f8"]
```

Now you should see your `Keystore File (UTC / JSON)`under `private/keystore` directory. 

```bash
[~/eblocPOA]$ ls private/keystore
UTC--2018-02-14T11-00-59.995395000Z--7d334606c71417f944ff8ba5c09e3672066244f8
```

To give open acccess to the keystore file:

```bash
sudo chown -R $(whoami) private/keystore/UTC--...
```

- Afterwards, open the following file: `$HOME/eBlocBroker/.profile` and set `COINBASE` with your created Ethereum Address.

-------

Laater, please do following inside your Amazon instance.

```bash
# To run eBloc Etheruem Node
$ eblocServer          

# To run eBlocBroker Driver
$ cd $HOME/eBlocBroker 
$ bash initialize.sh # Do it only once.
$ sudo ./Driver.sh
```

## Start Running Cluster using eBlocBroker

### Slurm Setup:
Slurm should run on the background. Please run: 

```bash 
sudo ./runSlurm.sh
```

Following example should successfully submit the job:

```bash
cd eBlocBroker/slurmJobExample
sbatch -N1 run.sh
Submitted batch job 1
```

### Cluster Side: How to register a cluster

Please note the following: 

- If you do not have any `Federated Cloud ID` or `MiniLock ID` give an empty string: `""`. You can use `./registerCluster.py` to submit your jobs. 

```python
coreNumber         = 128;
clusterEmail       = "ebloc@gmail.com";
federationCloudId  = "ee14ea28-b869-1036-8080-9dbd8c6b1579@b2drop.eudat.eu";
miniLockId         = "9VZyJy1gRFJfdDtAjRitqmjSxPjSAjBR6BxH59UeNgKzQ"
corePriceMinuteWei = 100; 
ipfsID             = "/ip4/79.123.177.145/tcp/4001/ipfs/QmWmZQnb8xh3gHf9ZFmVQC4mLEav3Uht5kHJxZtixG3rsf"; 

./registerCluster.py $coreNumber $clusterEmail $federationCloudId $miniLockId $corePriceMinuteWei $ipfsID
```

#### **How to return all available Clusters Addresses**

```
./getClusterAddresses.py
```

### Client Side: How to obtain IPFS Hash of the job:

It is important that first you should run IPFS daemon on the background: `ipfs daemon &`. If it is not running, cluster is not able to get the IPFS object from the client's node.

Example code could be seen under `eBlocBroker/slurmJobExample` directory:

Client should put his Slurm script inside a file called `run.sh`. Please note that you do not have to identify `-n` and `-t` parameters, since they will be overritten with arguments provided by the client on the cluster end

Target into the folder you want to submit and do: `ipfs add -r .` You will see something similiar with following output:

```bash
added QmYsUBd5F8FA1vcUsMAHCGrN8Z92TdpNBAw6rMxWwmQeMJ simpleSlurmJob/helloworld.cpp
added QmbTzBprmFEABAWwmw1VojGLMf3nv7Z16eSgec55DYdbiX simpleSlurmJob/run.sh
added QmXsCmg5jZDvQBYWtnAsz7rukowKJP3uuDuxfS8yXvDb8B simpleSlurmJob
```

- Main folder's IPFS hash (for example:`QmWmyoMoctfbAaiEs2G46gpeUmhqFRDW6KWo64y5r581Vd`) would be used as key to the submitted `jobKey` to the `eBlocBroker` by the client.

-----------

### **How to submit a job using storageTypes**

In order to submit your job each user should already registered into eBlocBroker.You can use `./registerUser.py` to register. Please update followin arguments inside `registerUser.py` file.

`account`, `userEmail`, `federationCloudID`, `miniLockID`, and `ipfsAddress`.

After registiration is done,  each user should authenticate his ORCID id using following [link](http://ebloc.cmpe.boun.edu.tr/orcid-authentication/index.php).

-----------

Later, you can use `./submitJob.py` to submit your jobs.

#### **1. How to submit a job using IPFS**

Please update following arguments inside `submitJob.py` file.

```python
clusterAddress   = "0x6af0204187a93710317542d383a1b547fa42e705";  
ipfsHash         = "QmefdYEriRiSbeVqGvLx15DKh4WqSMVL8nT4BwvsgVZ7a5";
coreNum          = 1; 
coreGasDay       = 0;
coreGasHour      = 0;
coreGasMin       = 10;
jobDescription   = "Science"
storageType      = 0; # Please note that '0' stands for IPFS repository share. 
```

#### **2. How to submit a job using EUDAT**

Before doing this you have to be sure that you have shared your folder with cluster's FID. Please [follow](https://github.com/avatar-lavventura/someCode/issues/4). Otherwise your job will not be accepted. Please update following arguments inside `submitJob.py` file.

```python
clusterAddress = "0x6af0204187a93710317542d383a1b547fa42e705";
jobKey         = "folderName";
coreNum        = 1;
coreGasDay     = 0;
coreGasHour    = 0;
coreGasMin     = 10;
jobDescription = "Science";
storageType    = 1; # Please note that '1' stands for EUDAT repository share. 
```

#### **3. How to submit a job using IPFS+miniLock**

###### miniLock Setup

Please check following [tutorial](https://www.npmjs.com/package/minilock-cli). Do following code only to generate miniLock ID once and do not lose your passphrase:

```bash
$ mlck id alice@gmail.com --save --passphrase='bright wind east is pen be lazy usual'
```

You can look up your miniLock ID any time.

```bash
$ mlck id
Your miniLock ID: LRFbCrhCeN2uVCdDXd2bagoCM1fVcGvUzwhfVdqfyVuhi
```

###### How to decript your folder using miniLock

```bash
mlck decrypt -f fileName --passphrase="$(cat mlck_password.txt)" --output-file=./output.tar.gz
```
---------

Please update following arguments inside `submitJob.py` file.

```python
clusterID        = "0x6af0204187a93710317542d383a1b547fa42e705"; # clusterID you would like to submit. 
jobKey           = "QmefdYEriRiSbeVqGvLx15DKh4WqSMVL8nT4BwvsgVZ7a5"
coreNum          = 1; 
coreGasDay       = 0;
coreGasHour      = 0;
coreGasMin       = 10;
jobDescription   = "Science"
storageType      = 2; # Please note 2 stands for IPFS with miniLock repository share. 
```

#### **4. How to submit a job using GitHub**

If my github repository is `https://github.com/avatar-lavventura/simpleSlurmJob.git`. Please write your username followed by the folder name having '=' in between. Example: `avatar-lavventura=simpleSlurmJob`. Please update following arguments inside `submitJob.py` file. 

```python
clusterID        = "0x6af0204187a93710317542d383a1b547fa42e705"; # clusterID you would like to submit.
jobKey           = "avatar-lavventura=simpleSlurmJob" 
coreNum          = 1; 
coreGasDay       = 0;
coreGasHour      = 0;
coreGasMin       = 10;
jobDescription   = "Science"
storageType      = 3 ; # Please note that 3 stands for github repository share. 
```
-------------------------

#### **5. How to submit a job using Google-Drive**

##### [gdrive](https://github.com/prasmussen/gdrive) install:

```
$ go get github.com/prasmussen/gdrive
$ gopath=$(go env | grep 'GOPATH' | cut -d "=" -f 2 | tr -d '"')
$ echo 'export PATH=$PATH:$gopath/bin' >> ~/.profile
$ source .profile
$ gdrive about # This line authenticates the user only once on the same node.
Authentication needed
Go to the following url in your browser:
https://accounts.google.com/o/oauth2/auth?access_type=offline&client_id=...e=state
Enter verification code:
```

First you have to share your folder with the cluster:

```
folderPath='/home/prc/multiple/workingTestIpfs'
folderName='ipfs'
clusterToShare='aalimog1@binghamton.edu'
gdrive upload --recursive $folderPath/$folderName
jobKey=$(gdrive list | grep $folderName | awk '{print $1}')
echo $jobKey # This is jobKey
gdrive share $jobKey  --role writer --type user --email $clusterToShare
```

If your work is compressed under folder name such as folderPath/folderName/RUN.zip ; please name it `RUN.zip` or `RUN.tar.gz`.

---------

Please update following arguments inside `submitJob.py` file.

```python
clusterID        = "0xda1e61e853bb8d63b1426295f59cb45a34425b63"; # clusterID you would like to submit.
jobKey           = "1-R0MoQj7Xfzu3pPnTqpfLUzRMeCTg6zG" # Please write file-Id of the uploaded file
coreNum          = 1; 
coreGasDay       = 0;
coreGasHour      = 0;
coreGasMin       = 10;
jobDescription   = "Science"
storageType      = 4; # Please note that 4 stands for gdrive repository share.
```


### **How to obtain Submitted Job's Information:**

You can use `./getJobInfo.py` to submit your jobs. 

```python
clusterID = "0x6af0204187a93710317542d383a1b547fa42e705"; # clusterID that you have submitted your job.
jobKey    = "134633894220713919382117768988457393273"
index     = 0;   
./getJobInfo.py $clusterID $jobKey $index
```

- status of the job could be `QUEUED`, `REFUNDED`, `RUNNING`, `PENDING` or `COMPLETED`. 

-----------

### Events

#### Keep track of the log of receipts

```bash
fromBlock = eBlocBroker.getDeployedBlockNumber(); 
var event = eBlocBroker.LogReceipt({}, {fromBlock:fromBlock, toBlock:'latest'});
event.watch(function(error, result) {
  console.log(JSON.stringify(result));
});
```
#### Keep track of the log of submitted jobs

```bash
fromBlock = eBlocBroker.getDeployedBlockNumber(); 
var event = eBlocBroker.LogJob({}, {fromBlock:fromBlock, toBlock:'latest'});
event.watch(function(error, result) {
  console.log(JSON.stringify(result));
});
```
