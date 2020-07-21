"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
'''* R7 is reserved as the stack pointer (SP)'''
SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        '''Add list properties to the `CPU` class to hold 256 bytes of memory and 8 general-purpose registers.'''
        self.ram = [0] * 256
        self.reg = [0] * 8
        '''Also add properties for any internal registers you need, e.g. `PC`.'''
        self.pc = 0
        self.sp = 7
        '''Set up the branch table'''
        self.branchtable = {}
        self.branchtable[HLT] = self.hlt
        self.branchtable[LDI] = self.ldi
        self.branchtable[PRN] = self.prn
        self.branchtable[MUL] = self.mul
        self.branchtable[PUSH] = self.push
        self.branchtable[POP] = self.pop

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        line = line.strip()
                        line = line.split('#', 1)[0]
                        line = int(line, 2)
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")
            sys.exit(1)
        except IndexError:
            print("Usage: ls8.py filename")
            sys.exit(1)
        

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    '''`ram_read()` should accept the address to read and return the value stored there.'''
    def ram_read(self, MAR):
        return (self.ram[MAR])
    '''`ram_write()` should accept a value to write, and the address to write it to.'''
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
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



    def hlt(self):
        self.running = False

    def ldi(self):
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]
        self.reg[operand_a] = operand_b
        self.pc += 3

    def prn(self):
        to_prn = self.ram[self.pc + 1]
        print(self.reg[to_prn])
        self.pc += 2
    
    def mul(self):
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3
    
    def push(self):
        tar_reg = self.ram[self.pc + 1]
        '''Decrement the `SP`.'''
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.reg[tar_reg]
        self.pc += 2

    def pop(self):
        tar_reg = self.ram[self.pc + 1]
        self.reg[tar_reg] = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1
        self.pc += 2
    
    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            ir = self.pc
            inst = self.ram[ir]
            self.branchtable[inst]()
            # if inst == HLT:
            #     self.hlt()
            # elif inst == PRN:
            #     self.prn()
            # elif inst == LDI:
            #     self.ldi()
            # elif inst == MUL:
            #     self.mul()
