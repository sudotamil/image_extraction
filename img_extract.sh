#/bin/bash

filePath=$1
cre_filePath=$2
sudo mkdir -p $cre_filePath
sudo chmod 777 -R $cre_filePath
cd $cre_filePath
sudo pdfimages $filePath image -j -p
sudo chmod 777 -R $cre_filePath
echo "$cre_filePath"

















