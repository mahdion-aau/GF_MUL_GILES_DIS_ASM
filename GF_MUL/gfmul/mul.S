@@@@ Galois field multiplication based on Log_Exp: GF(2^8)
  .syntax unified
  .text
  .thumb
  
  .extern table       @@@@ table is used for gfmult


@@@@@ uint8_t gfmul(uint8_t a, uint8_t b, uint8_t c); For calculating: c = a * b (a and b are one share)
@@@@@@@@ gfmul(in_reg0:a, in_reg1: b, out_reg2: return)
@ r0 = &a, @ r1 = &b, @ r2 = &c

.global gfmul
.func gfmul
gfmul:
    # SVC 1     @@@@ START Trigger
    push    {lr}
	  push    {r4-r6}
    # eors r3, r3
    # movs r3, #0
    SVC 1     @@@@ START Trigger
    ldr  r6, =table     @ The address of the  "table"
    # # nop
    ldrb r0, [r0, #0]   @ r0 = a
    # nop
    ldrb r1, [r1, #0]   @ r1 = b
    # nop
    ldrb r3, [r6, r0]   @ r3 = table[a]
    # nop
    # movs r4, #0 
    ldrb r4, [r6, r1]   @ r4 = table[b]

    adds r3, r4         @ r3 = s = table[a] + table[b]


    # @@@@ Get the antilog: s = table[s+256]: g ^ s 
    # @ adds rd, <#imm> --> #imm: 3 bits, 0-7
    # @ movs rd, <#imm> --> #imm: 0-255
    movs r5, #250      @ 256 is not possible split: 255 + 1
    adds r5, #6
    adds r3, r5         @ r3 = s + 256

    ldrb r4, [r6, r3]   @ r4 = s = table[s+256]
    
    # @@@@ Checking if a = 0 or b = 0, return 0; without conditional branch
    negs r5, r0         @ r5 = -a

    # @asrs r5, #32       @ r5 = -a >> 32
    movs r6, #32
    asrs r5, r6         @ r5 = -a >> 32

    ands r5, r1         @ r5 = tmp = b & (-a >> 32)
    negs r5, r5         @ r5 = -tmp

    # @asrs r5, #32       @ r5 = -tmp >> 32
    asrs r5, r6         @ r5 = -tmp >> 32

    ands r4, r5         @ r4 = s & (-tmp >> 32)
    strb r4, [r2, #0]   @ r4 = c: a * b

    SVC 0   @@@@ END Trigger
    pop {r4-r6}
    pop {pc}
    # SVC 0   @@@@ END Trigger

.endfunc


@@@@@@ This function clears registers r0-r3
.global Clear
.func Clear
Clear:
    push    {lr}
    eors r0, r0
    eors r1, r1
    eors r2, r2
    eors r3, r3
    pop {pc}
.endfunc


.end

