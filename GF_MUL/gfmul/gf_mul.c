#include <stdio.h>
#include <stdlib.h>
#include "gf_mul.h"
#include "elmo-funcs.h"

void init_lfsrs(uint seed1, uint seed2);
uint8_t getRand(void);

// Computing c = a * b such as: a and b are one share
// C implementation of the simple Galois field multiplication in GF(2^8)
uint8_t gmul(uint8_t a, uint8_t b);

void Clear();  // This function clears registers r0-r3

//  C implementation of Galois field multiplication based on Log_Exp in GF(2^8)
uint8_t gfMul(uint8_t a, uint8_t b);

//  ASM implementation of  Galois field multiplication based on Log_Exp in GF(2^8)
//extern void gfmul(uint8_t* input_a, uint8_t* input_b, uint8_t* output_c);

// Aim: gmul(a, b) = gfMul(a, b) = gfmul(a, b)
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
int main(void) {

// Initializing lfsr for RNG_based_LFSR
    init_lfsrs(get_rand(), get_rand()); // get_rand() function is in elmo-funcs.h
    uint8_t in_a;
    uint8_t in_b;

    if (fix_vs_rnd)
    {
        in_a = 0x23;
        in_b = 0x12;
       // in_a = getRand();
       // in_b = getRand();
    }
    else{
        in_a = get_rand() & 0xff;
        in_b = get_rand() & 0xff;
//        in_a = 0x04;
//        in_b = 0x85;
    }

    uint8_t  a[2];
    uint8_t  b[2];
    uint8_t  c[2]; 
//    a[0]=getRand();
    a[0]= get_rand() & 0xff;
//    a[1]=a[0]^in_a;
//    b[0]=getRand();
    b[0]= get_rand() & 0xff;
//    b[1]=b[0]^in_b;

    //in_a=0;
    //in_b=0;

    // This function clears registers r0-r3
   Clear(); // Clearing r3 (Leaky)
//    start_trigger();
        gfmul(&a[0], &b[0], &c[0]);
//    pause_trigger();


    uint8_t g_mul = gmul(a[0], b[0]);
    uint8_t g_Mul = gfMul(a[0], b[0]);

    //add_byte_to_trace(((uint32_t)table)&0xff);
    add_byte_to_trace(a[0]);
    add_byte_to_trace(b[0]);
    add_byte_to_trace(c[0]);
    add_byte_to_trace(g_mul);
    add_byte_to_trace(g_Mul);

    // In trs file, the length of data must be even. There are added 5 bytes to trs file, one more is needed:
    uint8_t extra_byte = 0x00;
    add_byte_to_trace(extra_byte);
}


// This random number generator shifts the 32-bit LFSR
// twice before XORing it with the 31-bit LFSR.
//the bottom 16 bits are used for the random number
void init_lfsrs(uint seed1, uint seed2) {
    lfsr32 = seed1;
    lfsr31 = seed2;
}

uint8_t getRand(void) {
    int feedback;
    feedback = lfsr32 & 1;
    lfsr32 >>= 1;
    if(feedback == 1) {
        lfsr32 ^= (uint volatile)POLY_MASK_32;
    } else {
        retrand ^= (uint volatile)POLY_MASK_32;
    }
    feedback = lfsr32 & 1;
    lfsr32 >>= 1;
    if(feedback == 1) {
        lfsr32 ^= POLY_MASK_32;
    } else {
        retrand ^= POLY_MASK_32;
    }
    feedback = lfsr31 & 1;
    lfsr31 >>= 1;
    if(feedback == 1) {
        lfsr31 ^= POLY_MASK_31;
    } else {
        retrand ^= POLY_MASK_31;
    }
    return (lfsr32 ^ lfsr31) & 0xffff;
}

uint8_t gmul(uint8_t a, uint8_t b) {
    uint8_t p = 0; /* the product of the multiplication */
    while (a && b) {
        if (b & 1) /* if b is odd, then add the corresponding a to p (final product = sum of all a's corresponding to odd b's) */
            p ^= a; /* since we're in GF(2^m), addition is an XOR */

        if (a & 0x80) /* GF modulo: if a >= 128, then it will overflow when shifted left, so reduce */
            a = (a << 1) ^ 0x11b; /* XOR with the primitive polynomial x^8 + x^4 + x^3 + x + 1 (0b1_0001_1011) – you can change it but it must be irreducible */
        else
            a <<= 1; /* equivalent to a*2 */
        b >>= 1; /* equivalent to b // 2 */
    }
    return p;
}


uint8_t gfMul(uint8_t a, uint8_t b)
{
    int s = 0;
    s = table[a] + table[b];
    /* Get the antilog */
    s = table[s+256];
/*
    Checking a=0 or b=0, without conditional branch: if (a==0 or b==0){return 0;} else{return s;}
     Countermeasure for Power analysis attacks
*/
    uint8_t tmp = 0;
    tmp = b & (-a >> 8);
    s = s & (-tmp >> 8);
    return s;
}