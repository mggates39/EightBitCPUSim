/**
 * SAP-1 Simulator
 */
"use strict";

let canvas = document.querySelector("canvas");
let ctx = canvas.getContext("2d", {alpha: false});
let cpuState = [];
let cpuStateIndex = 0;
let autoTick = false;
let halted = false;

let initialCPU = {
    clock: false,
    currentCycle: 0,
    totalTicks: 0,
    ringCounter: 0,
    bus: 0b00000000,
    controlPins: 0b00000000000000000,
    flagsEnabled: false,
    carryFlag: false,
    zeroFlag: false,
    carryBit: false,
    zeroBit: false,
    pc: 0b0000,
    alu: 0b00000000,
    reg_acc: 0b00000000,
    reg_tmp: 0b00000000,
    reg_ins: 0b00000000,
    reg_out: 0b00000000,
    mar: 0b00000000,
    memory: [],
	speed: 300
};

let initialProgram = {
    memory: [
        // LABEL: Top
        0b00011110, // LDA <14>
        0b00111100, // SUB <12>
        0b01110110, // JC <6> - Continue
        0b00011101, // LDA <13>
        0b11100000, // OUT
        0b11110000, // HLT
        // LABEL: Continue
        0b01001110, // STA <14>
        0b00011101, // LDA <13>
        0b00101111, // ADD <15>
        0b01001101, // STA <13>
        0b01100000, // JMP 0 - Top
        0b00000000, //
        // Data
        0b00000001, // 1
        // Variables
        0b00000000, // product
        0b00000011, // x
        0b00011101, // y
    ],
};

/******************************************************
 * Pull memory definition from the memory GET parameter
 ******************************************************/
var urlParams = new URLSearchParams(window.location.search);
var str = urlParams.get('memory');
var memory = initialProgram.memory;
if (str != null) {
	memory = JSON.parse('[' + str + ']');
}

let cpu = deepCopy(initialCPU);
cpu.memory = memory;

/*****************************************************************************
 * CPU Functions
 ****************************************************************************/
const DEF = 0b00000000000000000; // Null Values
const HLT = 0b10000000000000000; // Halt clock
const MI  = 0b01000000000000000; // Memory address register in
const RI  = 0b00100000000000000; // RAM data in
const RO  = 0b00010000000000000; // RAM data out
const IO  = 0b00001000000000000; // Instruction register out
const II  = 0b00000100000000000; // Instruction register in
const AI  = 0b00000010000000000; // A register in
const AO  = 0b00000001000000000; // A register out
const EO  = 0b00000000100000000; // ALU out
const SU  = 0b00000000010000000; // ALU subtract
const BI  = 0b00000000001000000; // B register in
const OI  = 0b00000000000100000; // Output register in
const CE  = 0b00000000000010000; // Program counter enable
const CO  = 0b00000000000001000; // Program counter out
const J   = 0b00000000000000100; // Jump (program counter in)
const FI  = 0b00000000000000010; // Flags in
const RCR = 0b00000000000000001; // RCR - Ring Counter Reset

const OP_JC = 0b0111
const OP_JZ = 0b1000

const CTRL_LOGIC = [
    [MI|CO,  RO|II|CE,  RCR,    RCR,    RCR,          RCR, RCR, RCR],   // 0000 - NOP
    [MI|CO,  RO|II|CE,  IO|MI,  RO|AI,  RCR,          RCR, RCR, RCR],   // 0001 - LDA <A>
    [MI|CO,  RO|II|CE,  IO|MI,  RO|BI,  EO|AI|FI,     RCR, RCR, RCR],   // 0010 - ADD <A>
    [MI|CO,  RO|II|CE,  IO|MI,  RO|BI,  EO|AI|SU|FI,  RCR, RCR, RCR],   // 0011 - SUB <A>
    [MI|CO,  RO|II|CE,  IO|MI,  AO|RI,  RCR,          RCR, RCR, RCR],   // 0100 - STA
    [MI|CO,  RO|II|CE,  IO|AI,  RCR,    RCR,          RCR, RCR, RCR],   // 0101 - LDI
    [MI|CO,  RO|II|CE,  IO|J,   RCR,    RCR,          RCR, RCR, RCR],   // 0110 - JMP
    [MI|CO,  RO|II|CE,  RCR,    RCR,    RCR,          RCR, RCR, RCR],   // 0111 - JC
    [MI|CO,  RO|II|CE,  RCR,    RCR,    RCR,          RCR, RCR, RCR],   // 1000 - JZ
    [MI|CO,  RO|II|CE,  RCR,    RCR,    RCR,          RCR, RCR, RCR],   // 1001
    [MI|CO,  RO|II|CE,  RCR,    RCR,    RCR,          RCR, RCR, RCR],   // 1010
    [MI|CO,  RO|II|CE,  RCR,    RCR,    RCR,          RCR, RCR, RCR],   // 1011
    [MI|CO,  RO|II|CE,  RCR,    RCR,    RCR,          RCR, RCR, RCR],   // 1100
    [MI|CO,  RO|II|CE,  RCR,    RCR,    RCR,          RCR, RCR, RCR],   // 1101
    [MI|CO,  RO|II|CE,  AO|OI,  RCR,    RCR,          RCR, RCR, RCR],   // 1110 - OUT
    [MI|CO,  RO|II|CE,  HLT,    RCR,    RCR,          RCR, RCR, RCR],   // 1111 - HLT
];

function setControlPins() {
    let opCode = (cpu.reg_ins >> 4); // Only last 4 bits are opcode

    let tempLogic = deepCopy(CTRL_LOGIC[opCode]);
    // Modify base control logic if flags are set to allow jumps
    // This could be considered dynamic microcode. It's easier than
    // creating 4 instances of the above array.
    if (opCode == OP_JC && cpu.carryFlag) {
        tempLogic[2] = (IO|J);
    }
    if (opCode == OP_JZ && cpu.zeroFlag) {
        tempLogic[2] = (IO|J);
    }
    cpu.controlPins = (DEF | tempLogic[cpu.ringCounter]);
}

// Updates the CPU
function updateCpu() {
    cpu.clock = !cpu.clock;

    // HLT
    if (cpu.controlPins & HLT) {
        autoTick = false;
        halted = true;
    }

    // RCR
    if (cpu.controlPins & RCR) {
        cpu.ringCounter = 0;
        cpu.currentCycle += 1;
        return;
    }

    // Add or Subtract based on SU
    if (cpu.controlPins & SU) {
        cpu.alu = cpu.reg_acc - cpu.reg_tmp;

        if (cpu.reg_acc !== 0) {
            cpu.carryBit = true;
        } else {
            cpu.carryBit = false;
        }
    } else {
        cpu.alu = cpu.reg_tmp + cpu.reg_acc;
        // Overflow! Set Carry Flag and limit to 8 bits
        if (cpu.alu >= 255) {
            cpu.alu = cpu.alu & 0b11111111;
            cpu.carryBit = true;
        } else {
            cpu.carryBit = false;
        }
    }

    if (cpu.alu <= 0) {
        cpu.zeroBit = true;
        cpu.alu = cpu.alu & 0b11111111;
    } else {
        cpu.zeroBit = false
    }

    // Flags!
    if (cpu.controlPins & FI) {
        cpu.carryFlag = cpu.carryBit;
        cpu.zeroFlag = cpu.zeroBit;
    }

    // Bus Output (Write) Operations
    // Only output highest 4 bits
    if (cpu.controlPins & IO) {
        cpu.bus = (cpu.reg_ins & 0b00001111);
    }
    if (cpu.controlPins & CO) {
        cpu.bus = cpu.pc
    }
    if (cpu.controlPins & AO) {
        cpu.bus = cpu.reg_acc
    }
    if (cpu.controlPins & EO) {
        cpu.bus = cpu.alu
    }
    if (cpu.controlPins & RO) {
        cpu.bus = cpu.memory[cpu.mar]
    }
    if (cpu.controlPins & CE) {
        cpu.pc += 1
    }

	// Bus Input (Read) Operations
    // Jump - Note that the dynamic microcode implements JZ / JC
    if (cpu.controlPins & J) {
        cpu.pc = cpu.bus
    }

    // Accumulator
    if (cpu.controlPins & AI) {
        cpu.reg_acc = cpu.bus
    } // Input from Bus

    // B Register
    if (cpu.controlPins & BI) {
        cpu.reg_tmp = cpu.bus
    } // Input from Bus

    // Memory Address Register
    if (cpu.controlPins & MI) {
        cpu.mar = cpu.bus
    } // Increment Program Counter

    // Memory
    if (cpu.controlPins & RI) {
        cpu.memory[cpu.mar] = cpu.bus
    } // Input from Bus - Lower 4 bits

    // Instruction Register
    if (cpu.controlPins & II) {
        cpu.reg_ins = cpu.bus;
    } // Input from Bus

    // Output Register
    if (cpu.controlPins & OI) {
        cpu.reg_out = cpu.bus
    } // Input from Bus

    cpu.ringCounter += 1;
    cpuStateIndex++;
}

async function executeTick() {
    if (halted) {
        return;
    }

    document.getElementById('container').removeAttribute('hidden');

    setControlPins();
    // Save the last 31 states in history.
    cpuState.push(deepCopy(cpu));
    if (cpuState.length > 31) {
        cpuState.splice( 0, cpuState.length - 31);
    }
    updateCpu();
    drawAll();

    cpu.totalTicks +=1;
    if(autoTick) {
        setTimeout(function(){
            executeTick();
        }, cpu.speed);
    }
}

function resetCpu() {
    cpu = deepCopy(initialCPU);
	cpu.memory = memory;
    cpuState = [];
    cpuStateIndex = 0;
    autoTick = false;
    halted = false;
//    executeTick();
    document.getElementById('container').removeAttribute('hidden');
    drawAll();
}

/*****************************************************************************
 * Rendering
 ****************************************************************************/
function drawAll() {
    erase();
    drawPins();
    drawMar();
    updateMemoryInputBoxes();
    drawBus(cpu.bus);
    updateDecimalValues();
    blinkenLights();
    drawHistory();
    drawClock();
}

function drawClock() {
    if (halted) {
        document.getElementById('cpu-halted').innerText = "HALTED";
    } else {
        document.getElementById('cpu-halted').innerText = "";
    }
    document.getElementById("clock-auto-tick").checked = autoTick;
	document.getElementById("clk-range").value = cpu.speed;
	document.getElementById("clk-rate").innerText = cpu.speed;
}

function drawHistory() {
    let newTableBody = document.createElement('tbody');
    newTableBody.id = 'history-table-body';
    cpuState.forEach((state, index) => {
        let pins = '';
        if (cpuState[index].controlPins & HLT) { pins = pins + ' HL'}
        if (cpuState[index].controlPins & MI) { pins = pins + ' MI'}
        if (cpuState[index].controlPins & RI) { pins = pins + ' RI'}
        if (cpuState[index].controlPins & RO) { pins = pins + ' RO'}
        if (cpuState[index].controlPins & IO) { pins = pins + ' IO'}
        if (cpuState[index].controlPins & II) { pins = pins + ' II'}
        if (cpuState[index].controlPins & AI) { pins = pins + ' AI'}
        if (cpuState[index].controlPins & AO) { pins = pins + ' AO'}
        if (cpuState[index].controlPins & EO) { pins = pins + ' EO'}
        if (cpuState[index].controlPins & SU) { pins = pins + ' SU'}
        if (cpuState[index].controlPins & BI) { pins = pins + ' BI'}
        if (cpuState[index].controlPins & OI) { pins = pins + ' OI'}
        if (cpuState[index].controlPins & CE) { pins = pins + ' CE'}
        if (cpuState[index].controlPins & CO) { pins = pins + ' CO'}
        if (cpuState[index].controlPins & J) { pins = pins + ' J'}
        if (cpuState[index].controlPins & FI) { pins = pins + ' FI'}
        if (cpuState[index].controlPins & RCR) { pins = pins + ' RCR'}

        let row = newTableBody.insertRow(0);
        row.insertCell(0).innerHTML = cpuState[index].totalTicks;
        row.insertCell(1).innerHTML = cpuState[index].currentCycle;
        row.insertCell(2).innerHTML = cpuState[index].ringCounter;
        row.insertCell(3).innerHTML = pins;
    });
    let tableBody = document.getElementById('history-table-body');
    tableBody.parentNode.replaceChild(newTableBody, tableBody)
}

function updateMemoryInputBoxes() {
    let encodedMem = '';
    for (let i = 0; i < cpu.memory.length; i++) {
        document.getElementById('mem-input-' + i).value = printBinary(cpu.memory[i], 8);
        encodedMem = encodedMem += cpu.memory[i].toString(16).padStart(2, '0');
    }
    document.getElementById('memQuickLoad').value = encodedMem;

}

function blinkenLights() {
    drawLights(document.getElementById('pc-lights'), printBinary(cpu.pc).split(''), 'blue');
    drawLights(document.getElementById('acc-lights'), printBinary(cpu.reg_acc, 8).split(''), 'green');
    drawLights(document.getElementById('mar-lights'), printBinary(cpu.mar).split(''));
    drawLights(document.getElementById('ins-lights-data'), printBinary(cpu.reg_ins & (0b00001111), 4).split(''));
    drawLights(document.getElementById('ins-lights-opcode'), printBinary((cpu.reg_ins >> 4), 4).split(''), 'orange');
    drawLights(document.getElementById('tmp-lights'), printBinary(cpu.reg_tmp, 8).split(''), 'green');
    drawLights(document.getElementById('alu-lights'), printBinary(cpu.alu, 8).split(''));
    drawLights(document.getElementById('out-lights'), printBinary(cpu.reg_out, 8).split(''), 'blue');
    drawLights(document.getElementById('control-lights'), printBinary(cpu.controlPins, 17).split(''), 'blue', 18);
    drawLights(document.getElementById('flag-carry-lights'), printBinary(cpu.carryFlag, 1).split(''), 'orange', 1);
    drawLights(document.getElementById('flag-zero-lights'), printBinary(cpu.zeroFlag, 1).split(''), 'orange', 1);

    let display1 = document.getElementById('display-1');
    let display2 = document.getElementById('display-2');
    let display3 = document.getElementById('display-3');
    let baseClass = 'display-container display-size-12 display-no-';
    display1.className = baseClass + Math.floor(cpu.reg_out/100 % 10);
    display2.className = baseClass + Math.floor(cpu.reg_out/10 % 10);
    display3.className = baseClass + Math.floor(cpu.reg_out % 10);
}

function updateDecimalValues() {
    // Program Counter
    document.getElementById('value-pc').innerText = cpu.pc;
    document.getElementById('value-acc-reg').innerText = cpu.reg_acc;
    document.getElementById('value-tmp-reg').innerText = cpu.reg_tmp;
    document.getElementById('value-alu').innerText = cpu.alu;
    document.getElementById('carry-bit').innerText = cpu.carryBit;
    document.getElementById('zero-bit').innerText = cpu.zeroBit;

    // Register Pretty Print
    let opcode = [
        "NOP",
        "LDA <A>",
        "ADD <A>",
        "SUB <A>",
        "STA",
        "LDI",
        "JMP",
        "JC",
        "JZ",
        "NOP",
        "NOP",
        "NOP",
        "NOP",
        "NOP",
        "OUT",
        "HLT",
    ];
    // Only use the lowest four bits to decode the opcode.
    document.getElementById('current-ins-opcode').innerText = opcode[(cpu.reg_ins >> 4)];
    document.getElementById('current-ins-data').innerText = (cpu.reg_ins & 0b00001111);
}

function drawBus(bus) {
	ctx.fillStyle = "rgba(0,255,31,0.4)";
    ctx.fillRect(340, 5, 75, 760);
    document.getElementById('value-bus').innerText = printBinary(bus, 8);
}

function drawArrow(x, y, status, direction) {
    ctx.fillStyle = status ? "rgba(6,255,0,0.79)" : "rgba(205,247,228,0.53)";
    if (direction === "left") {
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x+15, y);
        ctx.lineTo(x+25, y+10);
        ctx.lineTo(x+15, y+20);
        ctx.lineTo(x, y+20);
        ctx.fill();
    } else {
        ctx.beginPath();
        ctx.moveTo(x+25, y);
        ctx.lineTo(x+10, y);
        ctx.lineTo(x, y+10);
        ctx.lineTo(x+10, y+20);
        ctx.lineTo(x+25, y+20);
        ctx.fill();
    }

    ctx.fillStyle = "#838fa1";
    ctx.fillRect(540, 200, 80, 250);
}

function drawMar() {
    ctx.fillStyle = "#838fa1";
    ctx.fillRect(140, 200, 80, 50);
    // Clear previous highlighted rows
    Array.from(document.getElementsByClassName('memory-row'),
        i => i.classList.remove("highlight-mem-row"));
    // Highlight Rows
    if (cpu.mar < 16) {
        document.getElementById('mem-row-' + cpu.mar).classList.add('highlight-mem-row');
    }
}

function drawLights(element, lightArray, color="red", spacing = 15) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
    lightArray.forEach((light, index) => {
        let newLight = document.createElement('div');
        newLight.className = parseInt(light) ? 'light light-' + color : 'light light-off-' + color;
        newLight.setAttribute('style', 'left:' + index * spacing + 'px');
        element.appendChild(newLight);
    });
}

function erase() {
    ctx.fillStyle = "#FFFFFF";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function drawPins() {
    togglePins((cpu.controlPins & HLT), 'pin-hlt');
    togglePins((cpu.controlPins & MI),  'pin-mi');
    togglePins((cpu.controlPins & RI),  'pin-ri');
    togglePins((cpu.controlPins & RO),  'pin-ro');
    togglePins((cpu.controlPins & IO),  'pin-io');
    togglePins((cpu.controlPins & II),  'pin-ii');
    togglePins((cpu.controlPins & AI),  'pin-ai');
    togglePins((cpu.controlPins & AO),  'pin-ao');
    togglePins((cpu.controlPins & EO),  'pin-eo');
    togglePins((cpu.controlPins & SU),  'pin-su');
    togglePins((cpu.controlPins & BI),  'pin-bi');
    togglePins((cpu.controlPins & OI),  'pin-oi');
    togglePins((cpu.controlPins & CE),  'pin-ce');
    togglePins((cpu.controlPins & CO),  'pin-co');
    togglePins((cpu.controlPins & J),   'pin-j');
    togglePins((cpu.controlPins & RCR), 'pin-rcr');
    togglePins((cpu.controlPins & FI),  'pin-fi');

    drawArrow(415, 20,  (cpu.controlPins & J),  "left");     // PC In
    drawArrow(415, 60,  (cpu.controlPins & CO), "right");    // PC Out
    drawArrow(415, 140, (cpu.controlPins & AI), "left");     // ACC In
    drawArrow(415, 180, (cpu.controlPins & AO), "right");    // ACC Out
    drawArrow(415, 320, (cpu.controlPins & EO), "right");    // ALU Out
    drawArrow(415, 440, (cpu.controlPins & BI), "left");     // B In
    drawArrow(415, 570, (cpu.controlPins & OI), "left");     // Output Register In
    drawArrow(315, 150, (cpu.controlPins & MI), "right");    // MAR
    drawArrow(315, 380, (cpu.controlPins & RI), "right");    // RAM In
    drawArrow(315, 430, (cpu.controlPins & RO), "left");     // RAM Out
    drawArrow(315, 680, (cpu.controlPins & II), "right");    // II In
    drawArrow(315, 720, (cpu.controlPins & IO), "left");     // IR Out
}

function togglePins(status, className) {
    if (status) {
        Array.from(document.getElementsByClassName(className),
            i => i.classList.add("highlight-pin"));
    } else {
        Array.from(document.getElementsByClassName(className),
            i => i.classList.remove("highlight-pin"));
    }
}

/*****************************************************************************
 * Helper Functions
 ****************************************************************************/
function deepCopy(obj) {
    return JSON.parse(JSON.stringify(obj));
}

function printBinary(dec, padding = 4) {
    return (dec >>> 0).toString(2).padStart(padding, "0");
}

/*****************************************************************************
 * Memory Input Box Handling
 ****************************************************************************/
// Binary Inputs only
Array.from(document.getElementsByClassName("memoryInput"),
    i => i.addEventListener('keydown', function (ev) {
        if (ev.keyCode !== 48 && ev.keyCode !== 49 && ev.keyCode !== 8) {
            ev.preventDefault();
        }
    })
);

Array.from(document.getElementsByClassName("memoryInput"),
    i => i.addEventListener('focusout', memoryChanged, false));

function memoryChanged(e) {
    let index = parseInt(e.target.id.split('-')[2]);
    cpu.memory[index] = parseInt(e.target.value, 2);
    drawAll();
}

document.getElementById('clock-auto-tick').addEventListener('change', function() {
    autoTick = this.checked;
    executeTick();
});

document.getElementById('clk-range').oninput = function() {
    cpu.speed = this.value;
};

document.getElementById('clk-button').addEventListener('click', function() {
    executeTick();
});

/**
 *
 *     memory: [
 0b01110001, // 0x0000
 0b01001110, // 0x0001
 0b01110000, // 0x0010
 0b01010000, // 0x0011
 0b00101110, // 0x0100
 0b01001111, // 0x0101
 0b00011110, // 0x0110
 0b01001101, // 0x0111
 0b00011111, // 0x1000
 0b01001110, // 0x1001
 0b00011101, // 0x1010
 0b10000000, // 0x1011
 0b01100011, // 0x1100
 0b00000000, // 0x1101
 0b00000000, // 0x1110
 0b00000000  // 0x1111
 ]
 */

/*

        // LABEL: Top
        0b00011110, // LDA <14>
        0b00111100, // SUB <12>
        0b01110110, // JC <6> - Continue
        0b00011101, // LDA <13>
        0b11100000, // OUT
        0b11110000, // HLT
        // LABEL: Continue
        0b01001110, // STA <14>
        0b00011101, // LDA <13>
        0b00101111, // ADD <15>
        0b01001101, // STA <13>
        0b01100000, // JMP 0 - Top
        0b00000000, //
        // Data
        0b00000001, // 1
        // Variables
        0b00000000, // product
        0b00000011, // x
        0b00011101, // y
 */
// Fibinocci
/*
memory: [
    0b01110001, // 0x0000
    0b01001110, // 0x0001
    0b01110000, // 0x0010
    0b01010000, // 0x0011
    0b00101110, // 0x0100
    0b01001111, // 0x0101
    0b00011110, // 0x0110
    0b01001101, // 0x0111
    0b00011111, // 0x1000
    0b01001110, // 0x1001
    0b00011101, // 0x1010
    0b10000000, // 0x1011
    0b01100011, // 0x1100
    0b00000000, // 0x1101
    0b00000000, // 0x1110
    0b00000000  // 0x1111
]; */


/*

        0b11100000, // OUT  <------------+--+
        0b00101111, // ADD <15>          |  |
        0b01110100, // JC <4>   ====+    |  |
        0b01100000, // JMP <0>  ---||----+  |
        0b00111111, // SUB <15> <==+        |
        0b11100000, // OUT        ||        |
        0b10000000, // JZ <0>  ---||--------+
        0b01110100, // JMP <4> ===+
        0b00000000, //
        0b00000000, //
        0b00000000, //
        0b00000000, //
        0b00000000, //
        0b00000000, //
        0b00000000, //
        0b00000100  // Data: 1
 */
/*
    memory: [
        0b00011110, // LDA <14>
        0b00101111, // ADD <15>
        0b11100000, // OUT  - Should be 42
        0b11110000, // HLT
        0b00000000, // 0x0100
        0b00000000, // 0x0101
        0b00000000, // 0x0110
        0b00000000, // 0x0111
        0b00000000, // 0x1000
        0b00000000, // 0x1001
        0b00000000, // 0x1010
        0b00000000, // 0x1011
        0b00000000, // 0x1100
        0b00000000, // 0x1101
        0b00011100, // 0x1110 - 28
        0b00001110  // 0x1111 - 14
    ]
    // - Test the zero and carry flags
    memory: [
        0b00011110, // LDA <14>
        0b11100000, // OUT
        0b00101111, // ADD <15>
        0b11100000, // OUT  - Should be 0 with carry and zero flag set
        0b11110000, // HLT
        0b00000000, // 0x0101
        0b00000000, // 0x0110
        0b00000000, // 0x0111
        0b00000000, // 0x1000
        0b00000000, // 0x1001
        0b00000000, // 0x1010
        0b00000000, // 0x1011
        0b00000000, // 0x1100
        0b00000000, // 0x1101
        0b11111111, // 0x1110 - 255
        0b00000001  // 0x1111 - 1
    ],

 */

/**
 *
 0b11100000, // OUT  <--------------+--+
 0b00101111, // ADD <15>            |  |
 0b01110100, // JC <4>   =====+     |  |
 0b01100000, // JMP <0>  ----||-----+  |
 0b00111111, // SUB <15> <====+        |
 0b11100000, // OUT          ||        |
 0b10000000, // JZ <0>  -----||--------+
 0b01110100, // JMP <4> =====+
 0b00000000, //
 0b00000000, //
 0b00000000, //
 0b00000000, //
 0b00000000, //
 0b00000000, //
 0b00000000, //
 0b00000001 // Data: 1
 */


/*
        // LABEL: Top
        0b00011110, // LDA <14>
        0b00111100, // SUB <12>
        0b01110110, // JC <6> - Continue
        0b00011101, // LDA <13>
        0b11100000, // OUT
        0b11110000, // HLT
        // LABEL: Continue
        0b01001110, // STA <14>
        0b00011101, // LDA <13>
        0b00101111, // ADD <15>
        0b01001101, // STA <13>
        0b01100000, // JMP 0 - Top
        0b00000000, //
        // Data
        0b00000001, // 1
        // Variables
        0b00000000, // product
        0b00000010, // x
        0b01001000, // y
 */


// BOOT IT!
erase();
// executeTick();
    document.getElementById('container').removeAttribute('hidden');
    drawAll();

