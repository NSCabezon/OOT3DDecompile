#!/usr/bin/env python3
"""Static stats of OoT3D code.bin relevant for an AOT recompiler.

usage: aot_stats.py <code.bin> <oot3d.cfg> <outdir>
Function starts come from zeldaret/oot3d disassembly/oot3d.cfg (arm_func lines).
Per function: recursive-descent ARM decode inside [start, next_start); literal pools are
skipped because we only follow control flow. Classifies every control transfer.
"""
import sys, os, json, collections
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import (ARM_OP_REG, ARM_OP_IMM, ARM_OP_MEM, ARM_REG_PC, ARM_REG_LR,
                          ARM_CC_AL, ARM_INS_B, ARM_INS_BL, ARM_INS_BLX, ARM_INS_BX,
                          ARM_INS_POP, ARM_INS_LDM, ARM_INS_LDR, ARM_INS_MOV, ARM_INS_ADD,
                          ARM_INS_SVC, ARM_INS_LDMIB, ARM_INS_LDMDA, ARM_INS_LDMDB, ARM_INS_SUB)

BASE = 0x100000


def main():
    code = open(sys.argv[1], 'rb').read()
    cfg = sys.argv[2]
    out = sys.argv[3]
    os.makedirs(out, exist_ok=True)
    text_end = BASE + 0x3C99A8
    funcs = []
    names = {}
    for ln in open(cfg):
        p = ln.split()
        if len(p) >= 3 and p[0] in ('arm_func', 'thumb_func'):
            a = int(p[1], 16)
            funcs.append((a, p[0]))
            names[a] = p[2]
    funcs.sort()
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    fstarts = set(a for a, _ in funcs)
    stats = collections.Counter()
    indirect_sites = []
    jt_sites = []
    per_func = []
    callees = collections.Counter()
    for idx, (start, kind) in enumerate(funcs):
        end = funcs[idx + 1][0] if idx + 1 < len(funcs) else text_end
        end = min(end, text_end)
        seen = set()
        work = [start]
        ninsn = 0
        fstat = collections.Counter()
        maxpc = start
        while work:
            pc = work.pop()
            while start <= pc < end and pc not in seen:
                seen.add(pc)
                off = pc - BASE
                ins = next(md.disasm(code[off:off + 4], pc), None)
                if ins is None:
                    fstat['undecodable'] += 1
                    break
                ninsn += 1
                maxpc = max(maxpc, pc + 4)
                iid = ins.id
                ops = ins.operands
                cond = ins.cc
                writes_pc = False
                term = False
                if iid in (ARM_INS_B, ARM_INS_BL) and ops and ops[0].type == ARM_OP_IMM:
                    tgt = ops[0].imm
                    if iid == ARM_INS_BL:
                        fstat['call_direct'] += 1
                        callees[tgt] += 1
                    else:
                        if start <= tgt < end:
                            work.append(tgt)
                            fstat['branch_local'] += 1
                        else:
                            fstat['tailcall_direct'] += 1
                            callees[tgt] += 1
                        if cond == ARM_CC_AL:
                            term = True
                elif iid == ARM_INS_BLX:
                    if ops[0].type == ARM_OP_IMM:
                        fstat['call_direct_to_thumb'] += 1
                    else:
                        fstat['call_indirect'] += 1
                        indirect_sites.append((pc, 'blx_reg', ins.op_str))
                elif iid == ARM_INS_BX:
                    if ops[0].reg == ARM_REG_LR:
                        fstat['return'] += 1
                    else:
                        fstat['jump_indirect_bx'] += 1
                        indirect_sites.append((pc, 'bx_reg', ins.op_str))
                    if cond == ARM_CC_AL:
                        term = True
                elif iid == ARM_INS_SVC:
                    fstat['svc'] += 1
                else:
                    # anything writing PC
                    regs_w = []
                    try:
                        _, regs_w = ins.regs_access()
                    except Exception:
                        pass
                    if ARM_REG_PC in regs_w or (ops and ops[0].type == ARM_OP_REG and ops[0].reg == ARM_REG_PC
                                                and iid not in (ARM_INS_LDR,) or
                                                (iid == ARM_INS_LDR and ops[0].reg == ARM_REG_PC)):
                        writes_pc = True
                    if iid in (ARM_INS_POP, ARM_INS_LDM, ARM_INS_LDMIB, ARM_INS_LDMDA, ARM_INS_LDMDB):
                        if any(o.type == ARM_OP_REG and o.reg == ARM_REG_PC for o in ops):
                            fstat['return'] += 1
                            writes_pc = False
                            if cond == ARM_CC_AL:
                                term = True
                    if writes_pc:
                        # armcc switch: addls pc, pc, rN, lsl #2 ; b default ; b case0 ; b case1 ...
                        if iid == ARM_INS_ADD and len(ops) >= 2 and ops[1].type == ARM_OP_REG and ops[1].reg == ARM_REG_PC:
                            # count following unconditional B's as table
                            n = 0
                            # first insn after add is default branch (executed when cond fails) at pc+4,
                            # table begins at pc+8
                            q = pc + 8
                            tgts = []
                            while q < end:
                                i2 = next(md.disasm(code[q - BASE:q - BASE + 4], q), None)
                                if i2 is None or i2.id != ARM_INS_B or i2.cc != ARM_CC_AL:
                                    break
                                tgts.append(i2.operands[0].imm)
                                n += 1
                                q += 4
                            fstat['jumptable'] += 1
                            fstat['jumptable_entries'] += n
                            jt_sites.append((pc, n, ins.mnemonic + ' ' + ins.op_str))
                            work.append(pc + 4)
                            for k in range(n):
                                work.append(pc + 8 + 4 * k)
                            term = True
                        elif (iid == ARM_INS_LDR and ops[1].type == ARM_OP_MEM and ops[1].mem.base == ARM_REG_PC
                              and ops[1].mem.index != 0):
                            # armcc switch: cmp rN,#K ; ldrls pc,[pc,rN,lsl #2] ; b default ; .word case0..caseK
                            idxreg = ops[1].mem.index
                            n = None
                            for back in range(1, 6):
                                q = pc - 4 * back
                                if q < start:
                                    break
                                i2 = next(md.disasm(code[q - BASE:q - BASE + 4], q), None)
                                if i2 and i2.mnemonic.startswith('cmp') and i2.operands[0].reg == idxreg \
                                        and i2.operands[1].type == ARM_OP_IMM:
                                    # ldrls (<=K) -> K+1 entries; ldrlo/ldrcc (<K) -> K entries
                                    n = i2.operands[1].imm + (1 if ins.mnemonic.endswith('ls') else 0)
                                    break
                            if n is None:
                                fstat['jumptable_unbounded'] += 1
                                indirect_sites.append((pc, 'jumptable_unbounded', ins.op_str))
                                n = 0
                            fstat['jumptable'] += 1
                            fstat['jumptable_entries'] += n
                            tgts = []
                            for k in range(n):
                                w = int.from_bytes(code[pc + 8 + 4 * k - BASE:pc + 12 + 4 * k - BASE], 'little')
                                tgts.append(w)
                                seen.add(pc + 8 + 4 * k)  # data, not code
                                if start <= w < end:
                                    work.append(w)
                                else:
                                    fstat['jumptable_target_outside_func'] += 1
                            jt_sites.append((pc, n, ins.mnemonic + ' ' + ins.op_str))
                            if cond != ARM_CC_AL:
                                work.append(pc + 4)
                            term = True
                        elif iid == ARM_INS_LDR and ops[1].type == ARM_OP_MEM and ops[1].mem.base == ARM_REG_PC:
                            fstat['jump_indirect_ldr_pc_lit'] += 1
                            indirect_sites.append((pc, 'ldr_pc_literal', ins.op_str))
                            term = cond == ARM_CC_AL
                        elif iid == ARM_INS_LDR:
                            fstat['jump_indirect_ldr_pc'] += 1
                            indirect_sites.append((pc, 'ldr_pc', ins.op_str))
                            term = cond == ARM_CC_AL
                        elif iid == ARM_INS_MOV and ops[1].type == ARM_OP_REG and ops[1].reg == ARM_REG_LR:
                            fstat['return'] += 1
                            term = cond == ARM_CC_AL
                        else:
                            fstat['jump_indirect_other'] += 1
                            indirect_sites.append((pc, 'other_pc_write', ins.mnemonic + ' ' + ins.op_str))
                            term = cond == ARM_CC_AL
                    # calls via mov lr, pc ; bx/ldr pc
                if term:
                    break
                pc += 4
        size = end - start
        per_func.append(dict(addr=start, name=names[start], span=size, insns=ninsn, reach_end=maxpc,
                             **{k: v for k, v in fstat.items()}))
        stats.update(fstat)
        stats['insns'] += ninsn
        stats['span_bytes'] += size
    # data in text: span minus decoded insns*4
    stats['functions'] = len(funcs)
    stats['arm_funcs'] = sum(1 for _, k in funcs if k == 'arm_func')
    stats['thumb_funcs'] = sum(1 for _, k in funcs if k == 'thumb_func')
    stats['text_bytes'] = text_end - BASE
    stats['first_func'] = funcs[0][0]
    stats['decoded_code_bytes'] = stats['insns'] * 4
    stats['non_reached_bytes_in_spans'] = stats['span_bytes'] - stats['insns'] * 4
    stats['call_targets_not_func_start'] = sum(1 for t in callees if t not in fstarts)
    stats['distinct_call_targets'] = len(callees)
    sizes = sorted(f['span'] for f in per_func)
    stats['size_median'] = sizes[len(sizes) // 2]
    stats['size_p90'] = sizes[int(len(sizes) * 0.9)]
    stats['size_max'] = sizes[-1]
    buckets = collections.Counter()
    for s in sizes:
        b = '<=32' if s <= 32 else '<=128' if s <= 128 else '<=512' if s <= 512 else '<=2048' if s <= 2048 else '>2048'
        buckets[b] += 1
    stats['size_buckets'] = dict(buckets)
    json.dump(dict(stats), open(os.path.join(out, 'aot_stats.json'), 'w'), indent=1, default=str)
    with open(os.path.join(out, 'functions.tsv'), 'w') as o:
        keys = ['addr', 'name', 'span', 'insns', 'call_direct', 'call_indirect', 'jumptable',
                'jumptable_entries', 'jump_indirect_bx', 'return']
        o.write('\t'.join(keys) + '\n')
        for f in per_func:
            o.write('\t'.join(('0x%08x' % f[k]) if k == 'addr' else str(f.get(k, 0)) for k in keys) + '\n')
    with open(os.path.join(out, 'indirect_sites.tsv'), 'w') as o:
        for a, k, s in indirect_sites:
            o.write('0x%08x\t%s\t%s\n' % (a, k, s))
    with open(os.path.join(out, 'jumptables.tsv'), 'w') as o:
        for a, n, s in jt_sites:
            o.write('0x%08x\t%d\t%s\n' % (a, n, s))
    miss = [(t, c) for t, c in callees.items() if t not in fstarts]
    miss.sort()
    with open(os.path.join(out, 'call_targets_not_in_cfg.tsv'), 'w') as o:
        for t, c in miss:
            o.write('0x%08x\t%d\n' % (t, c))
    print(json.dumps(dict(stats), indent=1, default=str))


if __name__ == '__main__':
    main()
