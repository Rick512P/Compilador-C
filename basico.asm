sw $t0, 1 # n
sw $t1, x
sw $t2, 0
seq $t3, $t1, $t2
beq $t0, $t1, label_0
label_0:
    j END
j label_1
label_1:
END: