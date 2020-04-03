###############
# Test Add    #
###############
	.org 0
start:	LDA (x)
	MOV B,A
	LDA (y)
	ADD B
	STA (z)
	MVI A,0
	LDA (z)
	OUT 2
	HLT
# Variables
x:	.byte 15
y:	.byte 14
z:	.byte 0

	.end
