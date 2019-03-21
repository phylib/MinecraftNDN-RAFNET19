#!/bin/bash

download () {
  echo $1
  if [ -f $1 ]; then
     echo "File $1 already exists."
  else
     echo "File $1 does not exist, downloading it."
     wget -O $1 $2
  fi
}


FILE="networkTrace.pcap"
URL="http://www-itec.aau.at/ftp/icn/minecraft-ndn/RAFNET-19/networkTrace.pcap"
download $FILE $URL

FILE="gamestatechanges.tar.gz"
URL="http://www-itec.aau.at/ftp/icn/minecraft-ndn/RAFNET-19/gamestatechanges.tar.gz"
download $FILE $URL
