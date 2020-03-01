###############
# Fibonacci
###############
	.corg 0
top:	MVI A,1
	STA (y)
	MVI A,0
loop:	OUT 2
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

