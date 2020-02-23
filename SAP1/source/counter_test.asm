###############
# Count up and down test OUT display
###############
	.corg 0
top:	OUT
	ADD	(data)
	JC	(cont)
	JMP	(top)
cont:	SUB	(data)
	OUT
	JZ	(top)
	JMP	(cont)

	.dorg 15
# Variables
data:	.byte 1

	.end
