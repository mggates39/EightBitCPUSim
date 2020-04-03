###############
# Test Carry and Zero Flags
###############
	.corg 0
	MVI B,1
	LDA (x)
	OUT 2
	ADD B
	OUT 2
	SUB B
	SUB B
	OUT 2
	HLT

	.dorg 16
# Variables
x:	.byte 255

	.end
