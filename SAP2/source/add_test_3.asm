	LDA (x)
	MOV B,A
	LDA (y)
	ADD B
	OUT 1
	HLT
x: .byte 15
y: .byte 29
