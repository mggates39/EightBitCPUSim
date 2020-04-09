	ORG	0
start:	JMP Test

;
;************************************************************
;           MESSAGE TABLE FOR OPERATIONAL CPU TEST
;************************************************************
;
OKCPU:	DB	0CH,0DH,0AH,' CPU IS OPERATIONAL$'
;
NGCPU:	DB	0CH,0DH,0AH,' CPU HAS FAILED!    ERROR EXIT=$'
;
;


Test:	HLT
	END
