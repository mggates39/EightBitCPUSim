	LDA (x)
	MOV B,A
	LDA (y)
	ADD B
	OUT 2
	HLT
x: .byte 15
y: .byte 29
