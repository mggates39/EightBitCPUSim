###############
# Count up and down test OUT display
###############
	.corg 0
	MVI	A,0
	MVI	B,1
top:	OUT	2
	ADD	B
	JC	(cont)
	JMP	(top)
cont:	SUB	B
	OUT	2
	JZ	(top)
	JMP	(cont)

	.end
