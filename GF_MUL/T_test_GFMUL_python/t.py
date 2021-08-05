def GILES_disassemble(giles_dis_asm, sorted_dis_asm):
    number_of_lines = 0

    with open(giles_dis_asm) as dis_asm:
        counting_line = dis_asm.read().split("\n")
        for line in counting_line:
            if line:
                number_of_lines += 1
        print("lines", number_of_lines)
    dis_asm.close()

    with open(giles_dis_asm) as dis_asm:

        clock_cycle = dis_asm.read().splitlines()
    dis_asm.close()
    repeat = []
    with open(sorted_dis_asm, "w") as sorted_f:
        for i in range(number_of_lines):
            print("i", i)
            for j in range(number_of_lines):
                print("j", j)
                print("clock", clock_cycle[i][0:4])

                if int(clock_cycle[i][0:4]) == j:
                    if j not in repeat:
                        repeat.append(j)
                        sorted_f.write(clock_cycle[i][5:] + "\n")

    sorted_f.close()
GILES_disassemble("GILES_disassemble.txt", "tg.txt")
