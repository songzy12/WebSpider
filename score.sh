#!/bin/bash

#declare -A score

BASEDIR=$(pwd)

display_usage() {
    echo "put this shell script at the same level of *.zip *.rar files"
    echo "put all the standard input files in data/1.in, data/2.in, etc."
    echo "score.txt will be generated"
    echo "press enter to continue..."
    read -n1 
    clear
}

get_input_id() {
    echo
    echo "0: stdin"
    echo "2.in: 5"
    echo "3.in: 24 32"
    echo "5.in: this is a test"
    echo "input id.in id:"
    read -n1 input_id
}

get_command_id() {
    echo $cpp_file
    echo $student_id
    echo
    echo "press r to run, c for continue:"
    read -n1 command_id
}

get_question_id() {
    extension="${cpp_file##*.}"
    filename_="${cpp_file%.*}"
    question_id=(${filename_//_/ })
    question_id=${question_id[2]}
    if [[ ! "$question_id" ]]; then
        question_id=$filename_ 
    fi
}

preprocess() {
    iconv -f UTF-16 -t UTF-8 $cpp_file > $question_id.cpp
    sed -i 's/#include "stdafx.h"//g' "$question_id.cpp"
    sed -i 's/void main/int main/g' "$question_id.cpp"
    sed -i 's/scanf_s/scanf/g' "$question_id.cpp"
}

compile_and_run() {
    for cpp_file in *.c*
    do
        clear

        get_question_id
        echo $question_id
        preprocess 
        echo g++ $question_id".cpp"
        read
        g++ $question_id.cpp

        ./a.out < $BASEDIR/../data/$question_id.in > $question_id.out
        ans=$(diff $question_id.out $BASEDIR/../data/$question_id.out)
        echo "$student_id: $ans" >> score.txt
    done
}

actions() {
    cd tmp
    # there may be another level of dir
    if [ $(ls|wc -l) == 1 ];
    then
        cd $(ls)
    fi
    
    student_id=(${filename//_/ })
    echo $student_id
    compile_and_run

    cd $BASEDIR
}

rm -r tmp
echo > score.txt

for filename in *.zip
do
    echo $filename
    unzip -o $filename -d tmp 
    actions
    rm -r tmp
done

for filename in *.rar
do 
    echo $filename
    mkdir tmp
    unrar e $filename tmp
    
    actions
    rm -r tmp
done

less score.txt
