	.org 0
	JMP start
	
	.org 8
rs1:	MVI A,10
	OUT 2
	RET

	.org 50
start:
	MVI A,255
	RST 1
	HLT
	.end
