###############
# Test Add             #
###############
	.org 0
start:	LDA (x)
	ADD (y)
	OUT
	HLT
# Variables
x:	.byte 15
y:	.byte 14

	.end
