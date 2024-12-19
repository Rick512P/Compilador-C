sw $t0, 1 # n
sw $t1, x
sw $t2, 0
seq $t3, $t1, $t2
beq $t0, $zero, label_0
j label_1
label_0:
    sw $t0, 0 # n
    sw $t1, 1 # x
    sw $t2, n
    sw $t3, x
    add $t4, $t2, $t3
    sw $t5, $t4
    sw $t6, x
    sw $t7, 1
    add $t8, $t6, $t7
    sw $t9, $t8
    j END
label_1:
END: