### Overview
This [SAP-1](https://deeprajbhujel.blogspot.com/2015/12/sap-1-architecture.html) assembler is just a quick and dirty one.

The assembler can be run from inside the associated pyChaarm project or
from the command line

#### Usage
    usage: assemble.py [-h] --file FILE_NAME
    
    Assemble a SAP-1 Assembler file to binary
    
    optional arguments:
    -h, --help        show this help message and exit.
    --file FILE_NAME  filename to assemble.

#### About

The assembler is for an **enhanced** [SAP-1](https://deeprajbhujel.blogspot.com/2015/12/sap-1-instructions-and-instruction-cycle.html) instruction set.  It understands the following OP Codes:
 - **NOP**       - No Operation
 - LDA (A)   - Load accumulator from address A
 - ADD (A)   - Add value in address A to the accumulator
 - SUB (A)   - Subtract value in address A from the accumulator
 - **STA (A)**   - Store the accumulator in address A
 - **LDI N**  - Load accumulatore with the value N
 - **JMP (A)** - Jump to address A
 - **JC (A)** - Jump if Carry flag set to address A
 - **JZ (A)** - Jump if Zero flag set to address A
 - OUT - Display accumulator in output port
 - HLT - Halt the processor

Assembler source file format notes:
* Any line starting with a pound sign # is ignored.
* The .corg directive sets the starting address for the code segment
* Labels are identified with a traling colon :
* The .dorg directive sets the starting address for the data segment
* The .byte directive reserves and populates a single byte in memory
* The .end directive is the last line of the file
* Whitespace is required between lables, operators, and operands
* Witespace should be infront of directives as well as between directives and any arguments
* Address operands are enclosed in ( and ), even if they refer to labels

#### Sample File
This is a sample assembler file, multiply.asm.

	###############
	# Multipy two numbers x and y
	###############
		.corg 0
	Top:	LDA (x)
		SUB (One)
		JC (Continue)
		LDA (product)
		OUT
		HLT
	Continue:
		STA (x)
		LDA (product)
		ADD (y)
		STA (product)
		JMP (Top)

		.dorg 12
	# Constant Data
	One:	.byte 1
	#
	# Variables
	product:
		.byte 0
	x:	.byte 3
	y:	.byte 29

		.end

When assembled, it  generates the following output, sutiable for inserting into the CPU Simulator memory block.

	C:\Dev\CPU\Assembler\venv\Scripts\python.exe C:/Dev/CPU/Assembler/assemble.py --file ../source/multiply.asm
	
	Assemble ../source/multiply.asm
    0b01010001,  // top: LDI 1
    0b01001110,  //   STA (14) ; y
    0b01010000,  //   LDI 0
    0b11100000,  // loop: OUT 
    0b00101110,  //   ADD (14) ; y
    0b01001111,  //   STA (15) ; z
    0b00011110,  //   LDA (14) ; y
    0b01001101,  //   STA (13) ; x
    0b00011111,  //   LDA (15) ; z
    0b01001110,  //   STA (14) ; y
    0b00011101,  //   LDA (13) ; x
    0b01110000,  //   JC (0) ; top
    0b01100011,  //   JMP (3) ; loop
    0b00000000,  // x: 0
    0b00000000,  // y: 0
    0b00000000,  // z: 0

	Process finished with exit code 0
