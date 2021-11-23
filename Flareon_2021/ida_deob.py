# coding: utf-8
import ida_bytes
import idc
import idaapi
import ida_search
import ida_idp
import ida_name
import ida_segment
from known_hash import known_hash

rev_known_hash = {known_hash[k]:k for k in known_hash}
pos_table = {}
seg_base = 0x5000000
not_found = []
ida_segment.add_segm(0, seg_base, seg_base+0x40000, 'flare_ptr', "BSS")

def patch(cur_ea):
    head = cur_ea
    for i in range(100):
        head = idc.prev_head(head)
        if idc.print_insn_mnem(head) == "mov" and "ecx" == idc.print_operand(head, 0):
            target = idc.print_operand(head, 1)
            for ii in range(100):
                head = idc.prev_head(head)
                if idc.print_insn_mnem(head) == "mov" and target in  idc.print_operand(head, 0):
                    func_hash = int(idc.print_operand(head, 1)[:-1], 16)
                    if func_hash not in pos_table:
                        pos_table[func_hash] = seg_base+ 4*len(pos_table)
                    if not ida_idp.assemble(cur_ea, 0, cur_ea, True, f"call {rev_known_hash[func_hash].decode()}"):
                        idc.set_name(pos_table[func_hash], rev_known_hash[func_hash].decode(), ida_name.SN_CHECK)
                        ida_idp.assemble(cur_ea, 0, cur_ea, True, f"call {rev_known_hash[func_hash].decode()}")
                    ida_bytes.patch_bytes(cur_ea+5, b'\x90\x90')
                    break
            break

def again():
    code_head = 0x401000
    while code_head != idaapi.BADADDR:
        if idc.print_insn_mnem(code_head) == "xor" and  idc.print_operand(code_head, 0) ==  idc.print_operand(code_head, 1):
            next_head = idc.next_head(code_head)
            if idc.print_insn_mnem(next_head) == "div" and  idc.print_operand(code_head, 0) ==  idc.print_operand(next_head, 1):
                patch(code_head)
            elif idc.print_insn_mnem(next_head) == "mov":
                reg = idc.print_operand(code_head, 0)
                op2 = idc.print_operand(next_head, 1)
                op1 = idc.print_operand(next_head, 0)
                if ('[' in op1 or '[' in op2 ) and (op2 in op1 or op1 in op2) and (reg in op1 and reg in op2):
                        patch(code_head)
        code_head  = idc.next_head(code_head)
