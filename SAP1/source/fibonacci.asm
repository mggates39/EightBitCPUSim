###############
# Fibonacci
###############
	.corg 0
top:	LDI 1
	STA (y)
	LDI 0
loop:	OUT
	ADD (y)
	STA (z)
	LDA (y)
	STA (x)
	LDA (z)
	STA (y)
	LDA (x)
	JC  (top)
	JMP (loop)

	.dorg 13
# Variables
x:	.byte 0
y:	.byte 0
z:	.byte 0

	.end

