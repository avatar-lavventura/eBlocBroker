#!/bin/bash

preInstall=0;
newRpcPort="8545"; # Please change it if you have different RPC_PORT number.

# Update repository with the latest update
# git fetch --all && git reset --hard origin/master

# Pre-installation:-----------------------------------------
if [ $preInstall -eq 1 ]; then
    ## Python3 setup, required for all clusters! ========================================================
    sudo apt-get install python3-dev
    sudo apt-get install python3-venv
    python3 -m venv venv
    . venv/bin/activate
    pip install web3==4.4.1 # pip install --upgrade web3
    pip install colored
    pip install pyocclient==0.4
    pip install typing==3.6.4  # (https://github.com/ethereum/web3.py/issues/736#issuecomment-378679295)
    pip install --pre --upgrade web3
    pip install -U python-dotenv
    pip install sphinx_rtd_theme
    pip install google
    pip install google-cloud-storage
        
    ## npm
    wget -qO- https://deb.nodesource.com/setup_7.x | sudo bash -
    sudo npm install -g n # npm install --save
    sudo n latest
    npm install web3
    npm install web3_ipc
    npm install dotenv
    #==================================================================================================
    machineOS=$(bash $HOME/eBlocBroker/scripts/machine.sh)
    if [ "$machineOS" == "Mac" ]; then
        # Mac Packages
        brew install realpath
    else
        echo 'alper'
        ## Linux Packages
        sudo apt-get install davfs2 mailutils
        sudo apt-get install python-psutil
        sudo apt-get install -y nodejs
        sudo apt-get install munge
        sudo apt-get install bc
        sudo apt-get install realpath        
    fi

    ## Install google-drive:
    go get github.com/prasmussen/gdrive
    gopath=$(go env | grep 'GOPATH' | cut -d "=" -f 2 | tr -d '"')
    echo 'export PATH=$PATH:'$(echo $gopath)'/bin' >> $HOME/.profile
    source $HOME/.profile
    gdrive about
    echo 'export PATH=$PATH:$gopath/bin' >> ~/.profile

    ## gdfuse
    # shared_with_me=true to have read-only access to all your "Shared with me" files under ./.shared.
    sed -i.bak "s/^\(download_docs=\).*/\1false/" $HOME/.gdfuse/me/config
    # https://github.com/astrada/google-drive-ocamlfuse/issues/499#issuecomment-430269233
    # download_docs=false  
    sed -i.bak "s/^\(shared_with_me=\).*/\1true/" $HOME/.gdfuse/me/config    
fi
# IPFS check
# nc IP PORT
# Should return: /multistream/1.0.0

currentDir=$PWD;
# Folder Setup:========================================================
if [ ! -d $HOME/.eBlocBroker ]; then
    mkdir -p $HOME/.eBlocBroker;
fi

cd $HOME/.eBlocBroker

if [ ! -d transactions ]; then
    mkdir -p transactions
fi

if [ ! -d endCodeAnalyse ]; then
    mkdir -p endCodeAnalyse 
fi

if [ ! -d cache ]; then
    mkdir -p cache
fi

touch $HOME/.eBlocBroker/transactions/clusterOut.txt

sudo chmod +x $currentDir/slurmScript.sh
#======================================================================
cd $currentDir

# LOG_PATH path setup
lineNew=$HOME/.eBlocBroker
var=$(echo $lineNew | sed 's/\//\\\//g')
sed -i.bak "s/^\(LOG_PATH=\).*/\1\"$var\"/" .env
rm -f .env.bak

# GDRIVE path setup
sudo chown $(whoami) -R $HOME/.gdrive 
lineNew=$(which gdrive | sed 's/\//\\\//g')
sed -i.bak "s/^\(GDRIVE=\).*/\1\"$lineNew\"/" .env
rm -f .env.bak

# EBLOCPATH setup
eBlocBrokerPath="$PWD"
var=$(echo $eBlocBrokerPath | sed 's/\//\\\//g')
sed -i.bak "s/^\(EBLOCPATH=\).*/\1\"$var\"/" .env
rm .env.bak

# User Name Setup:======================================================
lineOld="whoami";
lineNew=$(logname);

sed -i.bak "s/^\(WHOAMI=\).*/\1\"$lineNew\"/" .env
rm -f .env.bak

# RPC PORT Setup:======================================================
lineOld="8545";

sed -i.bak "s/^\(RPC_PORT=\).*/\1$newRpcPort/" .env
rm .env.bak

# PATH Name Setup:===================================================
lineOld="EBLOCBROKER_PATH";
lineNew=$(echo $currentDir | sed 's/\//\\\//g')

sed -i.bak 's/'$lineOld'/'$lineNew'/' .env
rm .env.bak
sed -i.bak "s/^\(EBLOCBROKER_PATH=\).*/\1\"$lineNew\"/" slurmScript.sh
rm slurmScript.sh.bak

# COINBASE Address Setup:==============================================
lineOld='0xffffffffffffffffffffffffffffffffffffffff';
lineNew=$(echo $COINBASE);

sed -i.bak "s/^\(CLUSTER_ID=\).*/\1\"$lineNew\"/" .env && rm .env.bak
#======================================================================
if [[ ! -v COINBASE ]]; then
    echo "COINBASE is not set";
    echo "Type your cluster Ethereum Address, followed by [ENTER]:"
    read clusterID 
    echo 'export COINBASE="'$clusterID'"' >> $HOME/.profile   
elif [[ -z "$COINBASE" ]]; then
    echo "COINBASE is set to the empty string"
    echo "Type your cluster Ethereum Address, followed by [ENTER]:"
    read clusterID 
    echo 'export COINBASE="'$clusterID'"' >>~/.profile   
else
    echo "COINBASE is: $COINBASE"
    check=$(contractCalls/isAddress.py $COINBASE);
    if [ "$check" != "True" ]; then
       echo "Ethereum address is not valid, please use a valid one.";
       exit
    fi
fi

source $HOME/.profile

# SLURM Setup:======================================================================
sudo killall slurmctld slurmdbd slurmd
var=$(echo $currentDir | sed 's/\//\\\//g')
# With JobRequeue=0 or --no-requeue,
# the job will not restart automatically, please see https://stackoverflow.com/a/43366542/2402577
sudo sed -i.bak "s/^\(.*JobRequeue=\).*/\10/" /usr/local/etc/slurm.conf 
sudo rm -f /usr/local/etc/slurm.conf.bak

sudo sed -i.bak "s/^\(MailProg=\).*/\1$var\/slurmScript.sh/" /usr/local/etc/slurm.conf
sudo rm -f /usr/local/etc/slurm.conf.bak

# MinJobAge assingned to '1' day,
# The minimum age of a completed job before its record is purged from Slurm's active database.
sudo sed -i.bak "s/^\(.*MinJobAge=\).*/\186400/" /usr/local/etc/slurm.conf 
sudo rm /usr/local/etc/slurm.conf.bak
grep "MailProg" /usr/local/etc/slurm.conf

# IPFS setups
l=$(logname)
sudo chown -R "$l:$l" $HOME/.ipfs/

echo -e "Note: Update the following file 'eudatPassword.txt' with your EUDAT account's password. \nBest to make sure the file is not readable or even listable for anyone but you. You achieve this with:\n 'chmod 700 eudatPassword.txt'"

echo -e "\nUpdate the following file 'miniLockPassword.txt' with your Minilock accounts password."
echo -e "Please enter your miniLock password,"
read -s PASSWORD
echo $PASSWORD > miniLockPassword.txt
chmod 700 miniLockPassword.txt

sudo chmod 700 /home/*


# Setup
# sudo ln -s /usr/bin/node /usr/local/bin/node
# gdrive initialize
# rm -rf $HOME/.gdrive/

## pip install
# sudo apt-get install python3-pip
# sudo pip3 install virtualenv 
# once:
# $ virtualenv -p python3 ~/.venv-py3
# each session:
# $ source ~/.venv-py3/bin/activate
