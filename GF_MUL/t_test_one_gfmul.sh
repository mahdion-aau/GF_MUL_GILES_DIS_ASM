#! /bin/bash


# ./run in terminal: Permission denied, solving: chmod +x ./run.sh, and then for running: ./run
# variable: name of file
file1=${1:-gfmul}   # 1  argument
name1=${2:-fix_traces}     # 2  argument: name of the fix.trs
name2=${3:-rnd_traces}     # 3 argument: name of the rnd.trs
trace=${4:-1000}    # 4  argument Number of traces
echo $'\033[4;35mSTART                                                                    \033[0m \n'

pwd
cd ..

printf "\033[46m\033[1;30m[+] Making thumb-sim ready ----------------------------------------------\033[0m"
printf "\n"
rm -r build
mkdir build 
cd build
cmake ..
make clean all
make
cmake --build .
cd ..

printf "\033[46m\033[1;30m[+] Compiling FIX -------------------------------------------------------\033[0m"
printf "\n"
cd GF_MUL/$file1
make clean
cd ../..
# This means data is fix
make f_vs_r=1 -C  GF_MUL/$file1
cd GF_MUL/$file1/


#rm *.trs

printf "\033[46m\033[1;30m[+] Generating FIX traces -----------------------------------------------\033[0m"
printf "\n"
GILES example.bin -r "$trace" -o "$name1".trs --model Power
# GILES example.bin -r "$trace" -o "$name1".trs 

cp  "$name1".trs    ~/Documents/thumb-sim/GF_MUL/T_test_GFMUL_python

cd ../..

pwd

printf "\033[46m\033[1;30m[+] Compiling RND -------------------------------------------------------\033[0m"
printf "\n"

cd GF_MUL/$file1
make clean
cd ../..
# This means data is random
make f_vs_r=0  -C GF_MUL/$file1
cd GF_MUL/$file1/

pwd


printf "\033[46m\033[1;30m[+] Generating RND traces -----------------------------------------------\033[0m"
printf "\n"
GILES example.bin -r "$trace" -o "$name2".trs   --model Power
# GILES example.bin -r "$trace" -o "$name2".trs 

cp  "$name2".trs    ~/Documents/thumb-sim/GF_MUL/T_test_GFMUL_python
pwd
cp   GILES_disassemble.txt   ~/Documents/thumb-sim/GF_MUL/T_test_GFMUL_python
cd ..
pwd


echo $'\033[4;35mTHE END                                                                  \033[0m \n'



# color: https://gist.github.com/vratiu/9780109
