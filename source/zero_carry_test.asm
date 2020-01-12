###############
# Test Carry and Zero Flags
###############
	.corg 0
	LDA <x>
	OUT
	ADD <y>
	OUT
	HLT

	.dorg 14
# Variables
x:		.byte 255
y:		.byte 1

	.end
