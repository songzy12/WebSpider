#!/bin/bash

declare -A score

for filename in *.zip
do
    filename="${filename%.*}"
    ID=(${filename//_/ })
    score+=(["$ID"]=0)
done

for filename in *.rar
do 
    filename="${filename%.*}"
    ID=(${filename//_/ })
    score+=(["$ID"]=0)
done

for i in "${!score[@]}"
do
    echo "$i: ${score[$i]}"
done
