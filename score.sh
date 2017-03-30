#!/bin/bash

#declare -A score

BASEDIR=$(pwd)

usage() {
    echo "put this shell script at the same level of *.zip *.rar files"
    echo "put all the possible input files in data/1.in, data/2.in, etc."
    echo "a score.txt will be generated containing all the scores"
    echo "press any key to continue..."
    read 
}

input_info() {
    echo
    echo "0: stdin"
    echo "1.in: "
    echo "2.in: 8 employers"
    echo "3.in: aA1bB2cC3dD4"
    echo "input id.in id:"
}

command_info() {
    echo $filename_
    echo $ID
    echo
    echo "press r to run, c for continue:"
}

compile_and_run() {
    for filename_ in *.c*
    do
        echo $filename_
        sed -i 's/void main/int main/g' "$filename_"
        sed -i 's/scanf_s/scanf/g' "$filename_"
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

    echo "$ID score:"
    read point
    echo "$ID: $point" >> score.txt
}

#usage
rm -r tmp
echo > score.txt

for filename in *.zip
do
    unzip -o $filename -d tmp 
    actions
    rm -r tmp
    rm $filename
done

for filename in *.rar
do 
    mkdir tmp
    unrar e $filename tmp
    
    actions
    rm -r tmp
    rm $filename
done

less score.txt
