#! /bin/bash
# If you modify the GILES, you need to compile that again. 
# This script re-complies the GILES

# If after running "./compiling_GILES.sh" in terminal, you receive "Permission denied"
# For solving run this command: chmod +x ./compiling_GILES.sh, and then for running: ./compiling_GILES.sh



# git clone --recurse-submodules https://github.com/bristol-sca/GILES
# cd GILES
# mkdir build
# cd build
# cmake -G "Unix Makefiles" ..
# cmake --build .



rm -r build
mkdir build
cd build
cmake -G "Unix Makefiles" ..
cmake --build .
echo $' \n [+] New GILES in build/bin is ready ----------------------\n'


printf "\033[42m\033[1;30m[+] GILES in build/bin is generated --------------------------------------------\033[0m"
printf "\n"

build_dir=$(pwd) # saving the build directory
# echo $build_dir

# echo $' \n [+] Removing previous GILES from usr/bin ----------------------\n'
# cd /usr/bin
# pwd
# sudo rm GILES

cd $build_dir/bin
sudo cp GILES /usr/bin 
echo $' \n [+] Now, GILES can be used -----------------------------\n'


printf "\033[42m\033[1;30m[+] GILES can be used -----------------------------------------------\033[0m"
printf "\n"


