###############
# Multipy two numbers x and y
###############
	.corg 0
	MVI	B,1
	LDA (y)
	MOV C,A
Top:	LDA (x)
	SUB B
	JC (Continue)
	LDA (product)
	OUT 2
	HLT
Continue:
	STA (x)
	LDA (product)
	ADD C
	STA (product)
	JMP (Top)

	.dorg 32
# Variables
product:
	.byte 0
x:	.byte 3
y:	.byte 29

	.end