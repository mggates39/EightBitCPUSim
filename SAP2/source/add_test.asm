###############
# Test Add
###############
	.corg 0
	LDA (x)
	MOV B,A
	LDA (y)
	ADD B
	OUT 2
	HLT

	.dorg 17
# Variables
x:	.byte 28
y:	.byte 14

	.end
