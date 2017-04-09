#!/bin/bash

#declare -A score

BASEDIR=$(pwd)

usage() {
    echo "put this shell script at the same level of *.zip *.rar files"
    echo "put all the possible input files in data/1.in, data/2.in, etc."
    echo "a score.txt will be generated containing all the scores"
    echo "press any key to continue..."
    read -n1 
    clear
}

input_info() {
    echo
    echo "0: stdin"
    echo "2.in: 3"
    echo "3.in: 24 32"
    echo "5.in: this is a test"
    echo "input id.in id:"
}

command_info() {
    echo 
    echo $filename_
    echo $ID
    echo
    echo "press r to run, c for continue:"
}

compile_and_run() {
    for filename_ in *.c*
    do
        clear
        echo $filename_
        sed -i 's/#include "stdafx.h"//g' "$filename_"
        sed -i 's/int _tmain(int argc, _TCHAR\* argv\[\])/int main()/g' "$filename_"
        sed -i 's/void main/int main/g' "$filename_"
        sed -i 's/scanf_s/scanf/g' "$filename_"
        sed -i 's/gets_s/gets/g' "$filename_"
        cat "$filename_"
        command_info
        while read -n1 command ; do
            case $command in 
                r) 
                echo "run"
                g++ "$filename_"
                input_info
                read input
                case $input in
                    0) ./a.out
                    ;;
                    *)
                    ./a.out < $BASEDIR/data/$input.in
                    ;;
                esac
                ;;
                c)
                break
            esac
            echo
            cat "$filename_"
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
    
    ID=(${filename//_/ })
    echo $ID" press any key to continue..."
    read
    compile_and_run

    cd $BASEDIR

    #echo "$ID score:"
    #read point
    #echo "$ID: $point" >> score.txt
}

#usage
rm -r tmp
echo > score.txt

for filename in *
do
    ext="${filename##*.}"
    echo $ext
    if [ $ext == "zip" ];
    then
        unzip -o $filename -d tmp 
        actions
        rm -r tmp
        rm $filename
    fi

    if [ $ext == "rar" ];
    then
        mkdir tmp
        unrar e $filename tmp
    
        actions
        rm -r tmp
        rm $filename
    fi
done
