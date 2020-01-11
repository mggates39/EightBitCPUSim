This assempler is just a quick and dirty one.

Right now it has the souce code hard coded as if it had been parced into two 
segments.  One for code and another for data.  
The code segment has its origin at address zero.
The data segement's origin is at address 12

It is based on the file multipy.asm in the parent directory.

* Any line starting with a pound sign # is ignored.
* The .corg directive sets the starting address for the code segment
* Labels are identified with a traling colon :
* The .dorg directive sets the starting addres for the data segment
* The .byte directive reserves and populates a single byte in memory
* The .end directive is the last line of the file
* Whitespace is required between lables, operators, and operands
* Witespace should be infront of directives as well as between directives and any arguments

