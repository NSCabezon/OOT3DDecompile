#!/usr/bin/env python3
"""Differential semantic test: original code.bin function vs. our C reimplementation
(compiled by clang for armv6k hard-float and linked at 0x07000000), both executed in unicorn
from identical randomized memory. Callees are stubbed (args recorded, deterministic r0 returned).
Compares: callee trace (name, r0-r3, s0-s2, 2 stack words) and all RW memory at exit.

usage: difftest.py <code.bin> <oot3d.cfg> <pilot.elf> [trials]
"""
import sys, random, struct, subprocess, collections, zlib
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UcError, UC_PROT_ALL
from unicorn.arm_const import *

BASE = 0x100000
IMG_END = 0x600000          # code.bin + bss
HEAP = 0x08000000
HEAP_SZ = 0x00200000
MY = 0x07000000
MY_SZ = 0x00100000
STACK = 0x0E000000
STACK_SZ = 0x00100000
MAGIC_RET = 0x0F000000

ACTOR = HEAP
PLAY = HEAP + 0x100000
NPCS = HEAP + 0x10000
GAMEINFO = HEAP + 0x40000

GSAVE = 0x587958
GGAMEINFO_PTR = 0x51B2F4

code = open(sys.argv[1], 'rb').read()
cfg = sys.argv[2]
elf = sys.argv[3]
TRIALS = int(sys.argv[4]) if len(sys.argv) > 4 else 500

orig = {}
for ln in open(cfg):
    p = ln.split()
    if len(p) >= 3 and p[0].endswith('func'):
        orig[p[2]] = int(p[1], 16)
orig_by_addr = {v: k for k, v in orig.items()}

nm = subprocess.run(['/opt/homebrew/opt/llvm/bin/llvm-nm', elf], capture_output=True, text=True).stdout
mine = {}
for ln in nm.splitlines():
    p = ln.split()
    if len(p) == 3 and p[1] == 'T':
        mine[p[2]] = int(p[0], 16)
mine_by_addr = {v: k for k, v in mine.items()}
subprocess.run(['/opt/homebrew/opt/llvm/bin/llvm-objcopy', '-O', 'binary', elf, elf + '.bin'], check=True)
my_img = open(elf + '.bin', 'rb').read()
assert my_img, 'empty pilot image'

TESTS = ['ObjRoomtimer_Init', 'ObjRoomtimer_Destroy', 'ObjRoomtimer_Update', 'FUN_003e7c50', 'FUN_0010862c',
         'EnEg_Init', 'EnEg_Destroy', 'EnEg_Update', 'EnEg_Draw', 'FUN_00249af8',
         'ObjMakekinsuta_Init', 'ObjMakekinsuta_Update', 'ObjMakekinsuta_DoNothing', 'FUN_003bf620',
         'EnWallTubo_Init', 'EnWallTubo_Destroy', 'EnWallTubo_Update', 'FUN_001810b4']


# (int-reg args, float-reg args, stack words) actually consumed by each callee
ARITY = {
    'FUN_0035239c': (1, 0, 0), 'Actor_ChangeType': (4, 0, 0), 'Flags_GetTempClear': (2, 0, 0),
    'Flags_SetClear': (2, 0, 0), 'Flags_SetSwitch': (2, 0, 0), 'Flags_GetSwitch': (2, 0, 0),
    'FUN_00372244': (3, 0, 0), 'Actor_Kill': (1, 0, 0), 'Audio_PlaySoundGeneral': (4, 0, 2),
    'Gameplay_TriggerVoidOut': (1, 0, 0), 'FUN_0036f4f0': (1, 0, 0), 'Audio_SetBGM': (2, 0, 0),
    'FUN_0033caf8': (1, 0, 0), 'Actor_Spawn': (4, 3, 4),
}
DEFAULT_ARITY = (2, 0, 0)  # action funcs / actor funcs: (self, play)


def name_of(addr):
    return orig_by_addr.get(addr) or mine_by_addr.get(addr)


def norm(v):
    """Map our-image function addresses to original ones so stored pointers compare equal."""
    n = mine_by_addr.get(v)
    if n is not None and n in orig:
        return orig[n]
    return v


def build_state(rng):
    st = {}
    actor = bytearray(rng.getrandbits(8) for _ in range(0x200))
    # params: bias towards interesting values
    params = rng.choice([0x3FF, 0x3FF | (rng.randrange(64) << 10), rng.randrange(0x10000), rng.randrange(0x400),
                         601, 600, 599, 0])
    struct.pack_into('<H', actor, 0x1C, params)
    actor[3] = rng.choice([0, 1, 2, rng.randrange(256)])  # room
    struct.pack_into('<I', actor, 0x1A4, rng.choice([orig['FUN_0010862c'], orig['FUN_003e7098'],
                                                    orig['ObjMakekinsuta_DoNothing']]))
    # EnEg action: mostly 0
    st['enEgAction'] = rng.choice([0, 0, 0, 1, -1, rng.getrandbits(31)])
    struct.pack_into('<h', actor, 0x1A8, rng.choice([0, 1, 58, 59, 60, 61, 177, -1, rng.randrange(-32768, 32767)]))
    struct.pack_into('<H', actor, 0x1AA, rng.choice([0, 1, rng.randrange(65536)]))
    st['actor'] = actor
    play = bytearray(rng.getrandbits(8) for _ in range(0x8000))
    struct.pack_into('<h', play, 0x104, rng.choice([0xB, 0xB, 0, rng.randrange(100)]))
    struct.pack_into('<i', play, 0x7FA0, rng.choice([0, 0, 1]))
    # NPC list (category 4) at actorCtx(0x208C)+0xC+4*8 -> head ptr at 0x20BC
    n = rng.choice([0, 1, 2, 3, 5])
    ptrs = [NPCS + 0x400 * i for i in range(n)]
    npcs = bytearray(rng.getrandbits(8) for _ in range(0x400 * 8))
    for i, p in enumerate(ptrs):
        struct.pack_into('<h', npcs, 0x400 * i, rng.choice([0x14B, 0x14A, rng.randrange(0x200)]))
        struct.pack_into('<I', npcs, 0x400 * i + 0x130, ptrs[i + 1] if i + 1 < n else 0)
    struct.pack_into('<I', play, 0x20BC, ptrs[0] if ptrs else 0)
    st['npcs'] = npcs
    st['play'] = play
    save = bytearray(rng.getrandbits(8) for _ in range(0x1600))
    save[0xE] = rng.choice([0, 1])
    struct.pack_into('<h', save, 0x1560, rng.choice([0, 1, -1, rng.randrange(-32768, 32767)]))
    struct.pack_into('<h', save, 0x1564, rng.choice([0, 1, -1, rng.randrange(-32768, 32767)]))
    st['save'] = save
    gi = bytearray(0x15D4)
    struct.pack_into('<h', gi, 0x14 + 2 * 126, rng.choice([1, 2, 3, 3, 3, 4]))  # SREG(30) = R_UPDATE_RATE
    st['gameinfo'] = gi
    return st


def run(func_addr, under_test, st, seed, use_mine):
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.mem_map(BASE, IMG_END - BASE, UC_PROT_ALL)
    uc.mem_write(BASE, code)
    uc.mem_map(MY, MY_SZ, UC_PROT_ALL)
    uc.mem_write(MY, my_img)
    uc.mem_map(HEAP, HEAP_SZ, UC_PROT_ALL)
    uc.mem_map(STACK, STACK_SZ, UC_PROT_ALL)
    uc.mem_map(MAGIC_RET, 0x1000, UC_PROT_ALL)
    uc.mem_write(ACTOR, bytes(st['actor']))
    uc.mem_write(PLAY, bytes(st['play']))
    uc.mem_write(NPCS, bytes(st['npcs']))
    uc.mem_write(GSAVE, bytes(st['save']))
    uc.mem_write(GAMEINFO, bytes(st['gameinfo']))
    uc.mem_write(GGAMEINFO_PTR, struct.pack('<I', GAMEINFO))
    uc.mem_write(ACTOR + 0x1A4, struct.pack('<i', st['enEgAction'])) if under_test.startswith('EnEg') else None
    # enable VFP
    uc.reg_write(UC_ARM_REG_C1_C0_2, uc.reg_read(UC_ARM_REG_C1_C0_2) | (0xF << 20))
    uc.reg_write(UC_ARM_REG_FPEXC, 0x40000000)
    uc.reg_write(UC_ARM_REG_SP, STACK + STACK_SZ - 0x100)
    uc.reg_write(UC_ARM_REG_LR, MAGIC_RET)
    uc.reg_write(UC_ARM_REG_R0, ACTOR)
    uc.reg_write(UC_ARM_REG_R1, PLAY)
    trace = []
    rng = random.Random(seed)
    test_addrs = {orig[under_test], mine.get(under_test, -1)}

    def hook(uc, addr, size, _):
        if addr in test_addrs:
            return
        nm_ = name_of(addr)
        if nm_ is None:
            return
        if not (BASE <= addr < IMG_END or MY <= addr < MY + MY_SZ):
            return
        regs = [uc.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        sregs = [uc.reg_read(r) for r in (UC_ARM_REG_S0, UC_ARM_REG_S1, UC_ARM_REG_S2)]
        sp = uc.reg_read(UC_ARM_REG_SP)
        stk = struct.unpack('<4I', uc.mem_read(sp, 16))
        ni, nf, ns = ARITY.get(nm_, DEFAULT_ARITY)
        trace.append((nm_, tuple(norm(x) for x in regs[:ni]), tuple(sregs[:nf]), tuple(norm(x) for x in stk[:ns])))
        uc.reg_write(UC_ARM_REG_R0, rng.choice([0, 1, 0, 1, 0xFFFFFFFF, 2]))
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, hook)
    err = None
    try:
        uc.emu_start(func_addr, MAGIC_RET, count=200000)
    except UcError as e:
        err = '%s @ %08x' % (e, uc.reg_read(UC_ARM_REG_PC))
    mem = {}
    for nm_, a, sz in (('actor', ACTOR, 0x200), ('play', PLAY, 0x8000), ('npcs', NPCS, 0x2000),
                       ('save', GSAVE, 0x1600), ('gameinfo', GAMEINFO, 0x15D4)):
        b = bytes(uc.mem_read(a, sz))
        # normalise stored function pointers (word aligned)
        words = list(struct.unpack('<%dI' % (sz // 4), b))
        mem[nm_] = tuple(norm(w) for w in words)
    return trace, mem, err


def main():
    results = collections.OrderedDict()
    for t in TESTS:
        if t not in mine:
            results[t] = 'MISSING in pilot.elf'
            continue
        ok = 0
        fails = []
        paths = set()
        for i in range(TRIALS):
            rng = random.Random(zlib.crc32(t.encode()) * 100000 + i)
            st = build_state(rng)
            a = run(orig[t], t, st, i, False)
            b = run(mine[t], t, st, i, True)
            paths.add(tuple(x[0] for x in a[0]))
            if a == b:
                ok += 1
            else:
                if len(fails) < 3:
                    diff = []
                    if a[0] != b[0]:
                        diff.append(('trace', a[0], b[0]))
                    for k in a[1]:
                        if a[1][k] != b[1][k]:
                            idx = [j for j in range(len(a[1][k])) if a[1][k][j] != b[1][k][j]][:4]
                            diff.append((k, [(hex(j * 4), hex(a[1][k][j]), hex(b[1][k][j])) for j in idx]))
                    if a[2] != b[2]:
                        diff.append(('err', a[2], b[2]))
                    fails.append((i, diff))
        results[t] = (ok, TRIALS, len(paths), fails)
        print('%-26s %4d/%d equal   distinct callee-paths=%d' % (t, ok, TRIALS, len(paths)))
        for f in fails:
            print('    FAIL trial', f[0], f[1])
    return results


if __name__ == '__main__':
    main()
