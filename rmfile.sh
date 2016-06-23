#!/bin/sh


path="/home/hepeng/Code/dbms"
echo $path
for file in ${path}/*
do
	temp=`basename $file`
	len=${#temp}
	base=5
	if [ "$len" -eq "$base" ]
	then
		rm -rf $temp
	fi
done

