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
URL="https://raw.githubusercontent.com/phylib/MinecraftNDN-RAFNET19/master/LICENSE"
download $FILE $URL

FILE="gamestatechanges.tar.gz"
URL="domain.com/file.txt"
download $FILE $URL
