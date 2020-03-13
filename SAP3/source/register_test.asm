	.org 0
	LXI SP,(Stack)
	MVI A,87
	INR A
	MOV B,A
	INR B
	MOV C,B
	INR C
	MOV D,C
	INR D
	MOV E,D
	INR E
	MOV H,E
	INR H
	MOV L,H
	INR L
	PUSH DE
	LXI DE,(42738)
	POP DE
	MVI H,0
	MVI L,0
	HLT
;
; Top of Stack
;
	.org 128
Stack:	
	.end
