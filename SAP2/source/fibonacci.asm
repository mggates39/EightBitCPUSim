###############
# Fibonacci
###############
	.corg 0
top:	MVI C,0
	MVI B,1
loop:	MOV A,C
	OUT 2
	ADD B
	MOV B,C
	MOV C,A
	JC  (top)
	JMP (loop)

	.dorg 17
# Variables
x:	.byte 0
y:	.byte 0
z:	.byte 0

	.end

