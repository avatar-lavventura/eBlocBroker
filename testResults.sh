#!/bin/bash

readFrom=1846988
readTo=1843615

clusterID="0xcc8de90b4ada1c67d68c1958617970308e4ee75e"; # awsIpfs
#clusterID="0xe056d08f050503c1f068dc81fc7f7b705fc2c503"; # awsIpfsMiniLock
#clusterID="0xda1e61e853bb8d63b1426295f59cb45a34425b63"; # ebloc
#clusterID="0xf2129928bd1e6f4aa1ad131a37db2e55810cbbff"; # gDrive-Tetam

node log.js      $readFrom $clusterID
node log1.js     $readFrom $clusterID
node logPrint.js $clusterID

#clusterID="0xf20b4c9068a3945ce5cd73d50fdabbf04412e421"; # gDrive
