#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
# Built on top of Unicorn emulator (www.unicorn-engine.org) 
from unicorn import *
from unicorn.arm_const import *
from struct import pack
from .arch import Arch

def ql_arm_check_thumb(uc, reg_cpsr):
    mode = UC_MODE_ARM
    if reg_cpsr & 0b100000 != 0:
        mode = UC_MODE_THUMB
        return mode

class ARM(Arch):
    def __init__(self, ql):
        super(ARM, self).__init__(ql)


    def stack_push(self, value):
        SP = self.ql.uc.reg_read(UC_ARM_REG_SP)
        SP -= 4
        self.ql.uc.mem_write(SP, self.ql.pack32(value))
        self.ql.uc.reg_write(UC_ARM_REG_SP, SP)
        return SP


    def stack_pop(self):
        SP = self.ql.uc.reg_read(UC_ARM_REG_SP)
        data = self.ql.unpack32(self.ql.uc.mem_read(SP, 4))
        self.ql.uc.reg_write(UC_ARM_REG_SP, SP + 4)
        return data


    def stack_read(self, offset):
        SP = self.ql.uc.reg_read(UC_ARM_REG_SP)
        return self.ql.unpack32(self.ql.uc.mem_read(SP + offset, 4))


    def stack_write(self, offset, data):
        SP = self.ql.uc.reg_read(UC_ARM_REG_SP)
        return self.ql.uc.mem_write(SP + offset, self.ql.pack32(data))


    # set PC
    def set_pc(self, value):
        self.ql.uc.reg_write(UC_ARM_REG_PC, value)


    # get PC
    def get_pc(self):
        reg_cpsr = self.ql.uc.reg_read(UC_ARM_REG_CPSR)
        mode = ql_arm_check_thumb(self.ql.uc, reg_cpsr)
        if mode == UC_MODE_THUMB:
            append = 1
        else:
            append = 0
        return self.ql.uc.reg_read(UC_ARM_REG_PC) + append


    # set stack pointer
    def set_sp(self, value):
        self.ql.uc.reg_write(UC_ARM_REG_SP, value)


    # get stack pointer
    def get_sp(self):
        return self.ql.uc.reg_read(UC_ARM_REG_SP)


    # get stack pointer register
    def get_reg_sp(self):
        return UC_ARM_REG_SP


    # get pc register pointer
    def get_reg_pc(self):
        return UC_ARM_REG_PC

    def get_reg_table(self):
        registers_table = [
            UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
            UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5,
            UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
            UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
            UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR,
            UC_ARM_REG_PC, UC_ARM_REG_CPSR
            ]
        return registers_table

    # set register name
    def set_reg_name(self):
        pass  

    def get_reg_name(self, uc_reg):
        adapter = {
            UC_ARM_REG_R0: "R0",
            UC_ARM_REG_R1: "R1", 
            UC_ARM_REG_R2: "R2",
            UC_ARM_REG_R3: "R3", 
            UC_ARM_REG_R4: "R4", 
            UC_ARM_REG_R5: "R5",
            UC_ARM_REG_R6: "R6", 
            UC_ARM_REG_R7: "R7", 
            UC_ARM_REG_R8: "R8",
            UC_ARM_REG_R9: "R9", 
            UC_ARM_REG_R10: "R11", 
            UC_ARM_REG_R11: "R12",
            UC_ARM_REG_R12: "R13", 
            UC_ARM_REG_SP: "SP", 
            UC_ARM_REG_LR: "LR",
            UC_ARM_REG_PC: "PC", 
            UC_ARM_REG_CPSR: "CPSR",
        }
        if uc_reg in adapter:
            return adapter[uc_reg]
        # invalid
        return None