# """CPU functionality."""

# import sys

# HLT  = 0b00000001
# LDI  = 0b10000010
# PRN  = 0b01000111
# MUL  = 0b10100010
# PUSH = 0b01000101
# POP  = 0b01000110
# CALL = 0b01010000
# RET  = 0b00010001
# ADD  = 0b10100000
# CMP = 0b10100111
# JMP = 0b01010100
# JEQ = 0b01010101
# JNE = 0b01010110  

# '''
# Passing Examples -- Mult, Print8, sctest, stack
# '''

# class CPU:
#     """Main CPU class."""

#     def __init__(self):
#         """Construct a new CPU."""
#         '''Add list properties to the `CPU` class to hold 256 bytes of memory and 8 general-purpose registers.'''
#         self.ram = [0] * 256
#         self.reg = [0] * 8
#         '''Also add properties for any internal registers you need, e.g. `PC`.'''
#         self.pc = 0
#         '''* R7 is reserved as the stack pointer (SP)'''
#         self.sp = 7
#         '''Set up the branch table'''
#         self.branchtable = {}
#         self.branchtable[HLT] = self.hlt
#         self.branchtable[LDI] = self.ldi
#         self.branchtable[PRN] = self.prn
#         self.branchtable[MUL] = self.mul
#         self.branchtable[PUSH] = self.push
#         self.branchtable[POP] = self.pop
#         self.branchtable[CALL] = self.call
#         self.branchtable[RET] = self.ret
#         self.branchtable[ADD] = self.add
#         self.branchtable[CMP] = self.CMP
#         self.branchtable[JMP] = self.JMP
#         self.branchtable[JEQ] = self.JEQ
#         self.branchtable[JNE] = self.JNE
#         self.fl = 0
#         # E Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise.
#         self.E = 0 # 0 == false, 1 == true
#         # L Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise.
#         self.L = 0 # 1 == regA.value < regB.value
#         # G Greater-than: during a CMP, set to 1 if registerA is greater than registerB, zero otherwise.
#         self.G = 0 # 1 == regA.value > regB.value    

#     def load(self):
#         """Load a program into memory."""

#         address = 0

#         # For now, we've just hardcoded a program:
#         try:
#             with open(sys.argv[1]) as f:
#                 for line in f:
#                     try:
#                         line = line.strip()
#                         line = line.split('#', 1)[0]
#                         line = int(line, 2)
#                         self.ram[address] = line
#                         address += 1
#                     except ValueError:
#                         pass
#         except FileNotFoundError:
#             print(f"Couldn't find file {sys.argv[1]}")
#             sys.exit(1)
#         except IndexError:
#             print("Usage: ls8.py filename")
#             sys.exit(1)
        

#         # for instruction in program:
#         #     self.ram[address] = instruction
#         #     address += 1

#     '''`ram_read()` should accept the address to read and return the value stored there.'''
#     def ram_read(self, MAR):
#         try:
#             return (self.ram[MAR])
#         except IndexError:
#             print("index out of range for ram_read") 

#     '''`ram_write()` should accept a value to write, and the address to write it to.'''
#     def ram_write(self, MDR, MAR):
#         try:
#             self.ram[MAR] = MDR
#         except IndexError:
#             print("index out of range for ram_write")

#     def alu(self, op, reg_a, reg_b):
#         """ALU operations."""

#         if op == "ADD":
#             self.reg[reg_a] += self.reg[reg_b]
#         elif op == "MUL":
#             self.reg[reg_a] *= self.reg[reg_b]
#         #elif op == "SUB": etc
#         else:
#             raise Exception("Unsupported ALU operation")

#     def trace(self):
#         """
#         Handy function to print out the CPU state. You might want to call this
#         from run() if you need help debugging.
#         """

#         print(f"TRACE: %02X | %02X %02X %02X |" % (
#             self.pc,
#             #self.fl,
#             #self.ie,
#             self.ram_read(self.pc),
#             self.ram_read(self.pc + 1),
#             self.ram_read(self.pc + 2)
#         ), end='')

#         for i in range(8):
#             print(" %02X" % self.reg[i], end='')

#         print()

#     def increment_pc(self, op_code):
#         add_to_pc = (op_code >> 6) + 1
#         self.pc += add_to_pc

#     '''Halt the CPU (and exit the emulator).'''
#     def hlt(self):
#         self.running = False
#         sys.exit(1)

#     '''Set the value of a register to an integer.'''
#     def ldi(self):
#         operand_a = self.ram[self.pc + 1]
#         operand_b = self.ram[self.pc + 2]
#         self.reg[operand_a] = operand_b
#         self.increment_pc(LDI)

#     '''Print to the console the decimal integer value that is stored in the given register.'''
#     def prn(self):
#         to_prn = self.ram[self.pc + 1]
#         print(self.reg[to_prn])
#         self.increment_pc(PRN)

#     '''Multiply the values in two registers together and store the result in registerA.'''
#     def mul(self):
#         operand_a = self.ram[self.pc + 1]
#         operand_b = self.ram[self.pc + 2]
#         self.alu("MUL", operand_a, operand_b)
#         self.increment_pc(MUL)

#     def add(self):
#         operand_a = self.ram[self.pc + 1]
#         operand_b = self.ram[self.pc + 2]
#         self.alu("ADD", operand_a, operand_b)
#         self.increment_pc(ADD)
    
#     '''Push the value in the given register on the stack.'''
#     def push(self):
#         tar_reg = self.ram[self.pc + 1]
#         '''Decrement the `SP`.'''
#         self.reg[self.sp] -= 1
#         self.ram[self.reg[self.sp]] = self.reg[tar_reg]
#         self.increment_pc(PUSH)

#     '''Pop the value at the top of the stack into the given register.'''
#     def pop(self):
#         tar_reg = self.ram[self.pc + 1]
#         self.reg[tar_reg] = self.ram[self.reg[self.sp]]
#         self.reg[self.sp] += 1
#         self.increment_pc(POP)

#     '''Calls a subroutine (function) at the address stored in the register.'''
#     def call(self):
#         # try:
#             # ret_add = self.pc + 2
#             # # print(ret_add)
#             # self.reg[self.pc] -= 1
#             # addy = self.reg[self.pc]
#             # # print(addy)
#             # self.ram[addy] = ret_add
#             # reg_num = self.ram[self.pc + 1]
#             # # print(reg_num)
#             # subadd = self.reg[reg_num]
#             # # print(subadd)
#             # self.pc = subadd
#         self.reg[self.sp] -= 1
#         self.ram[self.reg[self.sp]] = self.pc + 2
#         addofsub = self.ram[self.pc + 1]
#         self.pc = self.reg[addofsub]
#         # except KeyError:
#         #     print(f'KeyError at {self.pc}')
#         #     sys.exit(1)
#         # except IndexError:
#         #     print(f'IndexError at {bin(self.sp)}')
#         #     sys.exit(1)

#     '''Return from subroutine.'''
#     def ret(self):
#         self.pc = self.ram[self.reg[self.sp]]
#         self.reg[self.sp] += 1

#     def JMP(self):
#         jump_address = self.reg[self.ram[self.pc + 1]]
#         self.pc = jump_address

#     def JEQ(self):
#         if self.E == 1:
#             self.pc = self.reg[self.ram[self.pc + 1]]
#         else:
#             self.pc += 2

#     def JNE(self):
#         if self.E == 0:
#             self.pc = self.reg[self.ram[self.pc + 1]]
#         else:
#             self.pc += 2
    
#     def CMP(self):
#         # self.alu('CMP', a, b)
#         # self.pc += 3

#         # compare two values in regA + regB , set flag accordingly
        
#         # RESET Flags for subsequent compares ?
#         self.E = 0
#         self.L = 0
#         self.G = 0
#         reg_a = self.reg[self.ram[self.pc + 1]]
#         reg_b = self.reg[self.ram[self.pc + 2]]

#         if reg_a == reg_b:
#             self.E = 1
#         elif reg_a < reg_b:
#             self.L = 1
#         elif reg_a > reg_b:
#             self.G = 1


#     def run(self):
#         """Run the CPU."""
#         self.running = True
#         self.reg[self.sp] = 244 # R7 in dec is 244

#         while self.running:
#             ir = self.pc
#             inst = self.ram[ir]
#             inst_len = ((inst & 11000000) >> 6) + 1
#             pc_mask = (inst & 0b00010000)
#             # operA = self.reg[self.ram[self.pc + 1]]
#             # operB = self.reg[self.ram[self.pc + 2]]
#             if pc_mask != 0b00010000:
#                 self.pc += inst_len
#             try:
#                 self.branchtable[inst]()
#             except KeyError:
#                 print(f'KeyError at {self.reg[self.ram[inst]]}')
#                 sys.exit(1)

#             # if inst == HLT:
#             #     self.hlt()
#             # elif inst == PRN:
#             #     self.prn()
#             # elif inst == LDI:
#             #     self.ldi()
#             # elif inst == MUL:
#             #     self.mul()

# """CPU functionality."""

# import sys

# PRN = 0b01000111 
# LDI = 0b10000010 
# HLT = 0b00000001 
# MUL = 0b10100010 
# PUSH = 0b01000101 
# POP = 0b01000110 
# CALL = 0b01010000 
# RET = 0b00010001
# CMP = 0b10100111
# JMP = 0b01010100
# JEQ = 0b01010101
# JNE = 0b01010110    
# SP = 7


# class CPU:
#     """Main CPU class."""

#     def __init__(self):
#         """Construct a new CPU."""
#         # Add list properties to the `CPU` class to hold 256 bytes of memory
#         self.ram = [0] * 256
#         # Add 8 general-purpose registers.
#         self.reg = [0] * 8
#         # Also add properties for any internal registers you need, e.g. `PC`.
#         # Program counter starts at 0, points to currently-executing instruction
#         self.pc = 0
#         # Set up a branch table
#         self.branchtable = {}
#         self.branchtable[PRN] = self.prn
#         self.branchtable[LDI] = self.ldi
#         self.branchtable[HLT] = self.hlt
#         self.branchtable[MUL] = self.mul
#         self.branchtable[PUSH] = self.push
#         self.branchtable[POP] = self.pop
#         self.branchtable[CALL] = self.call
#         self.branchtable[RET] = self.ret
#         self.branchtable[CMP] = self.CMP
#         self.branchtable[JMP] = self.JMP
#         self.branchtable[JEQ] = self.JEQ
#         self.branchtable[JNE] = self.JNE
#         # Flag setup
#         # set flag to 0
#         self.fl = 0
#         # E Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise.
#         self.E = 0 # 0 == false, 1 == true
#         # L Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise.
#         self.L = 0 # 1 == regA.value < regB.value
#         # G Greater-than: during a CMP, set to 1 if registerA is greater than registerB, zero otherwise.
#         self.G = 0 # 1 == regA.value > regB.value    

#     # PRN - PRN register pseudo-instruction
#     def prn(self):
#         # Print numeric value stored in the given register.
#         # Print to the console the decimal integer value that is stored in the given register.
#         operand_a = self.ram[self.pc + 1]
#         print(self.reg[operand_a])

#     # LDI - register immediate
#     def ldi(self):
#         operand_a = self.ram[self.pc + 1] # targeted register
#         operand_b = self.ram[self.pc + 2] # value to load
#         self.reg[operand_a] = operand_b
#         # self.pc += 3
    
#     # HLT - Halt the CPU (and exit the emulator).
#     def hlt(self):
#         self.running = False
#         # self.pc += 1

#     # MUL registerA registerB
#     def mul(self):
#         # Multiply the values in two registers together and store the result in registerA.
#         operand_a = self.ram[self.pc + 1]
#         operand_b = self.ram[self.pc + 2]
#         self.alu("MUL", operand_a, operand_b)
#         # self.pc += 3

#     def push(self):
#         reg_address = self.ram[self.pc + 1] # targeted register
#         self.reg[SP] -= 1  # grows down as things are pushed on, decrement stack, update stack pointer
#         value = self.reg[reg_address] 
#         # Copy the value in the given register to the address pointed to by SP
#         self.ram[self.reg[SP]] = value # Save value in portion of ram _that is allocated for the stack_
#         # self.pc += 2

#     def pop(self):
#         reg_address = self.ram[self.pc + 1] # targeted register
#         value = self.ram[self.reg[SP]] # get value from ram
#         self.reg[reg_address] = value # set value from ram to register address
#         self.reg[SP] += 1 # increment stack, update stack pointer
#         # self.pc += 2
    
#     # CALL - CALL register
#     # Calls a subroutine (function) at the address stored in the register.
#     def call(self):
#         # PUSH the next address onto the stack
#         # The address of the instruction directly after CALL is pushed onto the stack. 
#         # This allows us to return to where we left off when the subroutine finishes executing.
#         next_address = self.pc + 2
#         self.reg[SP] -= 1
#         self.ram[self.reg[SP]] = next_address
#         # The PC is set to the address stored in the given register. 
#         # Set pc to first argument(operand)
#         address = self.reg[self.ram[self.pc + 1]]
#         self.pc = address
#         # reg_address = self.ram[self.pc + 1]
#         # self.pc = self.reg[reg_address]

#         # We jump to that location in RAM and execute the first instruction in the subroutine.
#         # The PC can move forward or backwards from its current location.

#     # RET - Return from subroutine
#     def ret(self):
#         # Pop the value from the top of the stack
#         next_address = self.ram[self.pc]
#         self.reg[SP] += 1
#         # store it in the PC.
#         self.pc = next_address
    
#     def JMP(self):
#         jump_address = self.reg[self.ram[self.pc + 1]]
#         self.pc = jump_address

#     def JEQ(self):
#         if self.E == 1:
#             self.pc = self.reg[self.ram[self.pc + 1]]
#         else:
#             self.pc += 2

#     def JNE(self):
#         if self.E == 0:
#             self.pc = self.reg[self.ram[self.pc + 1]]
#         else:
#             self.pc += 2
    
#     def CMP(self):
#         # self.alu('CMP', a, b)
#         # self.pc += 3

#         # compare two values in regA + regB , set flag accordingly
        
#         # RESET Flags for subsequent compares ?
#         self.E = 0
#         self.L = 0
#         self.G = 0
#         reg_a = self.reg[self.ram[self.pc + 1]]
#         reg_b = self.reg[self.ram[self.pc + 2]]

#         if reg_a == reg_b:
#             self.E = 1
#         elif reg_a < reg_b:
#             self.L = 1
#         elif reg_a > reg_b:
#             self.G = 1

#     # In `CPU`, add method `ram_read()` and `ram_write()` that access the RAM inside
#     # the `CPU` object.

#     # `ram_read()` should accept the address to read and return the value stored
#     # there.
#     def ram_read(self, address):  # accept address to read
#         return(self.ram[address])  # get value stored at address

#     # `raw_write()` should accept a value to write, and the address to write it to.
#     def ram_write(self, value, address):  # accept value and address
#         self.ram[address] = value

#     def load(self):
#         """Load a program into memory."""
        
#         try: 
#             with open(sys.argv[1]) as f:
#                 address = 0
#                 # read in its contents line by line
#                 for line in f:
#                     num = line.split('#', 1)[0]
#                     if num.strip() == '':
#                         continue
#                     # convert binary to int and save appropriate data into RAM.
#                     self.ram[address] = int(num, 2)
#                     address += 1

#         except FileNotFoundError:
#             print(f"{sys.argv[0]}: {sys.argv[1]} Not found")
#             sys.exit(2)


#     def alu(self, op, reg_a, reg_b):
#         """ALU operations."""

#         if op == "ADD":
#             self.reg[reg_a] += self.reg[reg_b]
#         #elif op == "SUB": etc
#         elif op == "MUL":
#             self.reg[reg_a] *= self.reg[reg_b]
#         else:
#             raise Exception("Unsupported ALU operation")

#     def trace(self):
#         """
#         Handy function to print out the CPU state. You might want to call this
#         from run() if you need help debugging.
#         """

#         print(f"TRACE: %02X | %02X %02X %02X |" % (
#             self.pc,
#             self.fl,
#             #self.ie,
#             self.ram_read(self.pc),
#             self.ram_read(self.pc + 1),
#             self.ram_read(self.pc + 2)
#         ), end='')

#         for i in range(8):
#             print(" %02X" % self.reg[i], end='')

#         print()

#     def run(self):
#         """Run  the CPU."""
#         # Stack stores information temporarily
#         # Stack Pointer starts at top, R7 (Register 7)
#         # Acts as index 
#         # self.sp = 244 in decimal
#         self.reg[SP] = 244
#         self.running = True

#         while self.running: 
#             # Read the memory address that's stored in register `PC`, 
#             # Store that result in `IR`, the _Instruction Register_. This can just be a local variable in `run()`.
#             ir = self.pc
#             op = self.ram[ir]
#             # dynamic instruction size
#             # instruction_size = ((op & 11000000) >> 6) + 1

#             # In **any** case where the instruction handler sets the `PC` directly, you
#             # _don't_ want to advance the PC to the next instruction. So you'll have to
#             # set up a special case for those types of instructions. This can be a flag
#             # you explicitly set per-instruction... but can also be computed from the
#             # value in `IR`. 
#             # pc_flag = (op & 0b00010000)
#             # print("pc-flag", op)
            
#             operand_a = self.ram[self.pc + 1]
#             operand_b = self.ram[self.pc + 2]
#             instruction_size = ((op & 11000000) >> 6) + 1
#             pc_set_flag = (op & 0b00010000) # applies a mask to get pc_set bit
          
#             self.branchtable[op]
#                 # self.pc += instruction_size
#             if pc_set_flag != 0b00010000:
#                 self.pc += instruction_size
#             # except: 
#             #     print(f"unknown instruction {op}")
#             #     sys.exit(1)

           
