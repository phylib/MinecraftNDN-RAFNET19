#!/bin/bash

download () {
  if [ -f $1 ]; then
     echo "File $1 already exists."
  else
     echo "File $1 does not exist, downloading it."
     wget -qO- $2 | tar xvz || curl -s $2 | tar xvz
  fi
}


FILE="networkTrace.pcap"
URL="http://www-itec.aau.at/ftp/icn/minecraft-ndn/RAFNET-19/networkTrace.tar.gz"
download $FILE $URL

FILE="gameStateChanges.txt"
URL="http://www-itec.aau.at/ftp/icn/minecraft-ndn/RAFNET-19/gameStateChanges.tar.gz"
download $FILE $URL
