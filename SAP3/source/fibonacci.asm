###############
# Fibonacci
###############
	.org 0
top:	LXI BC,256
loop:	MOV A,C
	OUT 2
	ADD B
	MOV B,C
	MOV C,A
	JC (top)
	JMP (loop)
	.end

