###############
# Multipy two numbers x and y
###############
	.corg 0
Top:		LDA x
			SUB One
			JC Continue
			LDA product
			OUT
			HLT
Continue:	STA x
			LDA product
			ADD y
			STA product
			JMP Top

	.dorg 12
# Constant Data
One:		.byte 1
#
# Variables
product:	.byte 0
x:			.byte 3
y:			.byte 29

	.end