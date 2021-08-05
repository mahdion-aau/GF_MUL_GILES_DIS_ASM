from TRS import TRS


# Testing the GF multiplication

def gf_mult(a, b):
    """ Multiplication in the Galois field GF(2^8) """
    p = 0  # The product of the multiplication
    over_f = 0
    for i in range(8):
        # if b is odd, then add the corresponding a to p (final product = sum of all a's corresponding to odd b's)
        if b & 1 == 1:
            p ^= a  # since we're in GF(2^m), addition is an XOR

        over_f = a & 0x80
        a <<= 1
        if over_f == 0x80:
            a ^= 0x1b  # GF modulo: if a >= 128, then it will overflow when shifted left, so reduce
        b >>= 1
    return p % 256


name = "r_4"
trs = TRS(name + ".trs")  # The name of the trs file (name.trs)

trs.plot_initial()

for i in range(trs.number_of_traces):

    # Checking the correctness of the gadget and printing on the screen
    #################################################
    data = trs.get_trace_data(i)
    data_byte = bytearray([j for j in data])

    a = data_byte[0]
    b = data_byte[1]
    out_of_ASM_gfmul = data_byte[2]
    out_of_C_gfMul_log_exp = data_byte[3]
    out_of_C_gmul_simple = data_byte[4]

    print('- in_data {}: {}'.format(i, data_byte.hex()))
    print('i={0}'.format(i))
    print('- a: {}'.format(hex(a)))
    print('- b: {}'.format(hex(b)))
    print('- c: {0}'.format(hex(out_of_ASM_gfmul)))
    print('- gfmult: {}'.format(hex(gf_mult(a, b))))

    if out_of_ASM_gfmul != out_of_C_gfMul_log_exp:
        print("out_of_ASM_gfmul != out_of_C_gfMul_log_exp")
        break

    if out_of_ASM_gfmul != out_of_C_gmul_simple:
        print("out_of_ASM_gfmul != out_of_C_gmul_simple")
        break

    if out_of_C_gfMul_log_exp != out_of_C_gmul_simple:
        print("out_of_C_gfMul_log_exp != out_of_C_gmul_simple")
        break

    x = gf_mult(a, b)
    if x != out_of_ASM_gfmul:
        print("out_of_ASM_gfmul != gf_mult")
        break

    print('_________________________________________________________________________________________')
    trs.plot_trace(i)
trs.plot_show('Clock cycle', 'Power', name, 'Traces')
# plt.savefig(name + ".png")
print('-------> The trs file contains {} traces'.format(trs.number_of_traces))
print('[+] Each trace contains {:d} samples'.format(trs.number_of_samples))
