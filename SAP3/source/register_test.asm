	.org 0
	MVI A,87
	MOV B,A
	MOV C,B
	MOV D,C
	MOV E,D
	MOV H,E
	MOV L,H
	PUSH DE
	LXI DE,(42838)
	POP DE
	HLT

	.end
