###############
# Test Add
###############
	.corg 0
	LDA (x)
	ADD (y)
	OUT
	HLT

	.dorg 14
# Variables
x:	.byte 28
y:	.byte 14

	.end
