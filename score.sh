#!/bin/bash

#declare -A score

usage() {
    echo "put this under the same directory of *.zip *.rar files"
    echo "put all the input files in input/1.txt, input/2.txt, etc."
    echo "a score.txt will be generated containing all the scores"
    echo "press any key to continue..."
    read 
}

usage

echo > score.txt

actions() {
    cd tmp
    for filename_ in *
    do
        echo $filename_
        sed -i 's/void main/int main/g' $filename_
        cat $filename_
        echo
        echo "press r to run, EOF for break:"
        while read command ; do
            case $command in 
                r) 
                echo "run"
                g++ $filename_
                echo
                echo "input in.txt id:"
                read input
                ./a.out < ../input/$input.txt
                ;;
            esac
            echo "press r to run, EOF for break:"
        done
    done
    cd ..
    rm -r tmp

    filename="${filename%.*}"
    ID=(${filename//_/ })

    echo "$ID score:"
    read point
    echo "$ID: $point" >> score.txt
}

for filename in *.zip
do
    unzip -o $filename -d tmp 
    actions
    #score+=(["$ID"]=$point)
done

for filename in *.rar
do 
    filename="${filename%.*}"
    ID=(${filename//_/ })

    echo "$ID score:"
    read point
    echo "$ID: $point" >> score.txt
    #score+=(["$ID"]=$point)
done

#echo > score.txt
#for i in "${!score[@]}"
#do
#    echo "$i: ${score[$i]}" >> score.txt
#done

less score.txt
