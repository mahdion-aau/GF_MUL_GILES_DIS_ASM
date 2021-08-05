# GF_MUL_GILES_DIS_ASM
This file is related to the **Galois field multiplication based on Log_Exp: GF(2^8)**
c = a * b, where a, b and c are one share.
The function gfmul is used in all gadget for computing a[i] * b[i].\
**mul.S** is the implementation of GF(2^8) (gfmul(a,b,c), c = a * b)
for ARM Cortex-M0/3 in GNU assembly, 
with THUMB-16 instructions. The multiplication 
is based on Log_Ex with table.

Download [sumb-sim](https://github.com/sca-research/thumb-sim)

Copy the **GF_MUL** file in **thumb-sim**\
From **thumb-sim/GF_MUL** directory, Via terminal run `./t_test_one_gfmul.sh`.\
Note: If after running  `./t_test_one_gfmul.sh` in terminal,
you receive **Permission denied**,
 for solving: `chmod +x ./t_test_one_gfmul.sh`, 
and then for running: `./t_test_one_gfmul.sh`.

There are 4 arguments for `./t_test_one_gfmul.sh` command:
1) The file included the codes (.c, .S, ...)
2) The name of the file that you want to save fixed traces in. 
3) The name of the file that you want to save random traces in.
4) The number of traces for each fixed and random traces.\
`./t_test_one_gfmul.sh gfmul fix rnd 1000`.\
By default: If you just run `./t_test_one_gfmul.sh`, your fixed traces are inside **fix_traces.trs**, random traces are inside **rnd_traces.trs**, and each file contains 1000 traces.  


This means:
1) At the first, it compiles THUMB_SIM.
Go to the **gfmul** file (thumb-sim/GF_MUL/gfmul)
2) Compiles the gfmul for fix data (make f_vs_r=1 -C  GF_MUL/gfmul), then generating fix traces by using GILES.
3) copies **fix_traces.trs** in **T_test_GFMUL_python** file (thumb-sim/GF_MUL/T_test_GFMUL_python).
4) Compiles the gfmul for random data (make f_vs_r=0 -C  GF_MUL/gfmul), then generating random traces by using GILES.
5) copies **rnd_traces.trs** in **T_test_GFMUL_python** file (thumb-sim/GF_MUL/T_test_GFMUL_python).   

After running `./t_test_one_gfmul.sh`, in **T_test_GFMUL_python** file, the two **.trs** file must be there.

**Analysis.py**: For checking the correctness of **.trs** files.
**T_test.py**, for performing the T_TEST on **fix_traces.trs** and **rnd_traces.trs**







