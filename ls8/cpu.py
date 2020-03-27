"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.reg[self.sp] = 0xF4
        self.op_pc = False
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[CMP] = self.handle_CMP
        self.flag = 0b00000000

    # `ram_read()` should accept the address to read and return the value stored there  
    def ram_read(self, read_address):
        return self.ram[read_address]

    # `ram_write()` should accept a value to write, and the address to write it to
    def ram_write(self, write_address, write_value):
        self.ram[write_address] = write_value

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("usage: ls8.py <filename>")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:

                # split before and after any comment symbol '#'
                    comment_split = line.split("#")
                    num = comment_split[0].strip()

                # ignore blank lines / comment only lines
                    if len(num) == 0:
                        continue

                # set the number to an integer of base 2
                    value = int(num, 2)
                    # program.append(value)
                    self.ram_write(address, value)
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000001    
        else:
            raise Exception("Unsupported ALU operation")
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        IR = self.ram_read(self.pc)
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        
        running = True
        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR in self.branchtable:
                self.branchtable[IR](operand_a, operand_b)
            else:
                print(f"Unknown Instruction")
                sys.exit(1)

    
    def handle_LDI(self, op_id1, op_id2):
        self.reg[op_id1] = op_id2
        self.op_pc = False
        if not self.op_pc:
            self.pc += 3

    def handle_PRN(self, op_id1, op_id2):
        print(self.reg[op_id1])
        self.op_pc = False
        if not self.op_pc:
            self.pc += 2

    def handle_MUL(self, op_id1, op_id2):
        self.alu("MUL",op_id1, op_id2)
        self.op_pc = False
        if not self.op_pc:
            self.pc += 3 
    
    def handle_ADD(self, op_id1, op_id2):
        self.alu("ADD",op_id1, op_id2)
        self.op_pc = False
        if not self.op_pc:
            self.pc += 3 
    
    def handle_PUSH(self, op_id1, op_id2):
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.reg[op_id1]
        self.op_pc = False
        if not self.op_pc:
            self.pc += 2

    def handle_POP(self, op_id1, op_id2):
        self.reg[op_id1] = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        self.op_pc = False
        if not self.op_pc:
            self.pc += 2

    def handle_HLT(self, op_id1, op_id2):
        sys.exit()

   
    def handle_CALL(self, op_id1, op_id2):
        self.reg[self.sp] -= 1 
        self.ram[self.reg[self.sp]] = self.pc + 2
        self.pc = self.reg[op_id1]
        self.op_pc = True
        
    def handle_RET(self, op_id1, op_id2):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        self.op_pc = True
        
    def handle_CMP(self, op_id1, op_id2):
        self.alu("CMP",op_id1, op_id2)
        self.op_pc = False
        
        

