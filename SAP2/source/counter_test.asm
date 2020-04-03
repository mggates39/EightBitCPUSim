###############
# Count up and down test OUT display
###############
	.corg 0
	MVI	A,0
	MVI	B,1
top:	CALL	(sub)
	ADD	B
	JC	(cont)
	JMP	(top)
cont:	SUB	B
	CALL	(sub)
	JZ	(top)
	JMP	(cont)

	.org 36
sub:	OUT 2
	RET

	.end
