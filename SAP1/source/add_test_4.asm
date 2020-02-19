###############
# Test Add             #
###############
	.org 0
start:	LDA (x)
	ADD (y)
	STA (z)
	LDI	0
	LDA (z)
	OUT
	HLT
# Variables
x:	.byte 15
y:	.byte 14
z:	.byte 0

	.end
