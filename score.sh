#!/bin/bash

#declare -A score

BASEDIR=$(pwd)

usage() {
    echo "put this shell script at the same level of *.zip *.rar files"
    echo "put all the possible input files in data/1.in, data/1.out, etc."
    echo "a score.txt will be generated containing all the scores"
    echo "press any key to continue..."
    read 
}

input_info() {
    echo
    echo "1.in: "
    echo "2.in: 8 employers"
    echo "3.in: aA1bB2cC3dD4"
    echo "input id.in id:"
}

command_info() {
    echo
    echo "press r to run, EOF for break:"
}

compile_and_run() {
    for filename_ in *.c*
    do
        echo $filename_
        sed -i 's/void main/int main/g' $filename_
        cat $filename_
        command_info
        while read command ; do
            case $command in 
                r) 
                echo "run"
                g++ $filename_
                input_info
                read input
                ./a.out < $BASEDIR/data/$input.in
                cat $BASEDIR/data/$input.out
                ;;
            esac
            command_info
        done
    done
}

actions() {
    cd tmp
    # there may be another level of dir
    if [ $(ls|wc -l) == 1 ];
    then
        cd $(ls)
    fi
    
    compile_and_run

    cd $BASEDIR

    filename="${filename%.*}"
    ID=(${filename//_/ })

    echo "$ID score:"
    read point
    echo "$ID: $point" >> score.txt
}

usage
echo > score.txt

for filename in *.zip
do
    unzip -o $filename -d tmp 
    actions
    rm -r tmp
done

for filename in *.rar
do 
    mkdir tmp
    unrar e $filename tmp
    
    actions
    rm -r tmp
done

less score.txt
