This [SAP-1](https://deeprajbhujel.blogspot.com/2015/12/sap-1-architecture.html) assembler is just a quick and dirty one.

Right now it has the souce code hard coded as if it had been parced into two 
segments.  One for code and another for data.  
The code segment has its origin at address zero.
The data segement's origin is at address 12

It is based on the file multipy.asm in the parent directory.

The assembler is for an **enhanced** [SAP-1](https://deeprajbhujel.blogspot.com/2015/12/sap-1-instructions-and-instruction-cycle.html) instruction set.  It understands the following OP Codes:
 - **NOP**       - No Operation
 - LDA &lt;A&gt;   - Load accumulator from address A
 - ADD &lt;A&gt;   - Add value in address A to the accumulator
 - SUB &lt;A&gt;   - Subtract value in address A from the accumulator
 - **STA &lt;A&gt;**   - Store the accumulator in address A
 - **LDI N**  - Load accumulatore with the value N
 - **JMP &lt;A&gt;** - Jump to address A
 - **JC &lt;A&gt;** - Jump if Carry flag set to address A
 - **JZ &lt;A&gt;** - Jump if Zero flag set to address A
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
* Address operands are enclosed in &lt; and &gt;, even if they refer to labels

