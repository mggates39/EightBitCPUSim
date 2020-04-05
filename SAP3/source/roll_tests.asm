	.org	0
t_rrc:	ORI 0
	MVI A, 0FEH	;Comment
	RRC
	CC bad
	RRC
	CNC bad
	RRC
	CNC bad
	RRC
	CNC bad
	CPI 0EFH
	CNZ bad

t_rar:	ORI 0
	MVI A, 0FEH
	RAR
	CC bad
	RAR
	CNC bad
	RAR
	CNC bad
	RAR
	CNC bad
	CPI 0CFH
	CNZ bad
	
t_rlc:	ORI 0
	MVI A,0FEH
	RLC
	CNC bad
	RLC
	CNC bad
	RLC
	CNC bad
	RLC
	CNC bad
	CPI 0EFH
	CNZ bad

t_ral:	ORI 0
	MVI A,0FEH
	RAL
	CNC bad
	RAL
	CNC bad
	RAL
	CNC bad
	RAL
	CNC bad
	CPI 0E7H
	CNZ bad
	

good:	OUT 3
	HLT

bad:	OUT 2
	HLT
	.end
