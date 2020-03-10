###############
# Multipy two numbers x and y
###############
	.corg 0
	LDA (x)
	MOV B,A
	LDA (y)
	MOV C,A

	CALL (Mult)

	STA (product)
	OUT 2
	HLT

# Variables
product:
	.byte 0
x:	.byte 3
y:	.byte 29


Mult:	PUSH BC
	MVI A,0
mlp:	ADD C
	DCR B
	JNZ (mlp)
	POP BC
	RET

	.end