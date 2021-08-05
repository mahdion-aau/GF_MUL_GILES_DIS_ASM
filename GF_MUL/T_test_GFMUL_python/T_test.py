# in GILES, the rand and fix traces are stored in two deferrent trs files.
# 


from TRS import TRS
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.stats import ttest_ind
import math

step = 10
start_time = time.time()


class Traces:
    def __init__(self, filename):
        self.filename = filename
        self.trs = TRS(self.filename)
        self.n_t = self.trs.number_of_traces
        self.n_s = self.trs.number_of_samples
        self.len_p = self.trs.cryptolen

    # Extracting traces from TRS file
    ##################################################################
    def traces(self):
        """ This function extracts all traces from TRS file"""
        print("- n_traces: {}".format(self.n_t))
        print("- n_samples: {} (0 - {}: In Model_Power SVC1/0 Insts are not considered)".format(self.n_s, self.n_s))
        print("- n_clock_cycles: {}".format(self.n_s + 3))

        print("-------------------------------------------------------------------")
        all_trace = np.zeros((self.n_t, self.n_s), np.float64)  # Array of samples of each trace
        for i in range(self.n_t):
            all_trace[i] = self.trs.get_trace_sample(i)
        return all_trace


#####################################################
def TVLA(fix_set, rnd_set):
    # Output of ttest_ind = [t_value, p_value], just first element is needed, [0]
    t_test = ttest_ind(rnd_set, fix_set, axis=0, equal_var=False)[0]

    return t_test


def Leakage_points(t_values):
    leakage_point = []
    for i in range(len(t_values)):
        if abs(t_values[i]) > 4.5:
            leakage_point.append(i)
    return np.array(leakage_point, np.int32)


# A .txt file contained disassembled instruction with the corresponding clock
def GILES_disassemble(giles_dis_asm, sorted_dis_asm):
    # Finding the number of clock cycles in giles_dis_asm.txt file
    number_of_lines = 0
    with open(giles_dis_asm) as dis_asm:
        counting_line = dis_asm.read().split("\n")
        for line in counting_line:
            if line:
                number_of_lines += 1
    dis_asm.close()

    # Creating a pure file to have the disassembled instruction with the corresponding clock
    with open(giles_dis_asm) as dis_asm:
        clock_cycle = dis_asm.read().splitlines()
    dis_asm.close()
    repeat = []
    with open(sorted_dis_asm, "w") as sorted_f:
        # for i in range(number_of_lines):
        for i in range(1000):
            # for j in range(number_of_lines):
            for j in range(1000):
                if int(clock_cycle[i][0:4]) == j:
                    if j not in repeat:
                        repeat.append(j)
                        sorted_f.write(clock_cycle[i][5:] + "\n")
    sorted_f.close()


# Finding the related instruction to the leaky point
def leaky_instruction(leaky_points, dis_asm_file):
    if len(leaky_points) == 0:
        print("[+] No leaky Instructions")
        return

    with open(dis_asm_file, "r") as dis_asm_f:
        inst = dis_asm_f.read().splitlines()
        for point in leaky_points:
            print("[+] {}: {}".format(point, inst[point - 1][0:]))

            # print(inst[point][0:])
        dis_asm_f.close()


if __name__ == "__main__":
    fix_data = "f_4"
    rnd_data = "r_4"
    fix_d = Traces(fix_data + ".trs")
    rnd_d = Traces(rnd_data + ".trs")

    if fix_d.n_s != rnd_d.n_s:
        print("ERROR: fix_d.ns != rnd_d.ns")

    fix_traces = fix_d.traces()
    rnd_traces = rnd_d.traces()

    t = TVLA(rnd_traces, fix_traces)

    for i in range(fix_d.n_s):
        if math.isnan(t[i]):
            t[i] = 0
        if math.isinf(t[i]):
            t[i] = 100
    # #
    # for i in range(fix_d.n_s):
    #     print("t_value {}".format(t[i]))

    leakage_p = Leakage_points(t)

    GILES_disassemble("GILES_disassemble.txt", "disassemble.txt")

    print("- Number of leaky points: {} \n- Leaky points: {}".format(len(leakage_p), leakage_p))
    t_l_p = [t[leakage_p] for elm in leakage_p]
    # print("- T_value_l_p:  {}".format(np.array(t_l_p, np.int32)[0]))
    print("-------------------------------------------------------------------")
    print("leaky Instruction (according to the cycle):")

    leaky_instruction(leakage_p, "disassemble.txt")

    print("[+] The percentage of leaky points: {}%".format(len(leakage_p) / fix_d.n_s * 100))

    # for i in leakage_p:
    #     print("[point, t_value]: [{}, {}]".format(i, t[i]))
    # Plotting T_test result
    #####################################################
    plt.plot(t)

    plt.axhline(y=4.5, color='r', linestyle='dashed', linewidth=1)
    plt.axhline(y=-4.5, color='r', linestyle='dashed', linewidth=1)

    plt.title("T-test result")
    plt.xlabel("Clock cycle")
    plt.ylabel("t-value")
    plt.grid()
    plt.show()
    # plt.savefig("T_test result_" + name + ".png")
# print("\nDuration of acquisition (sec):", (time.time() - start_time))
# print("Duration of acquisition (min):", (time.time() - start_time)/60)
