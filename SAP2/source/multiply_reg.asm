###############
# Multipy two numbers x and y
###############
	.corg 0
	LDA (x)
	MOV B,A
	LDA (y)
	MOV C,A
	MVI A,0
Loop:	ADD C
	DCR B
	JNZ (Loop)

	STA (product)
	OUT 2
	HLT

# Variables
product:
	.byte 0
x:	.byte 3
y:	.byte 29

	.end