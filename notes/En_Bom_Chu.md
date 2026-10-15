
<!-- merge 2026-10-15 17:54:44 -->
# En_Bom_Chu STATUS (G41 haiku pass, 2026-10-15)

MATCHED (fastchk + ws_check baseline):
- EnBomChu_Destroy (C, src/game/actors/En_Bom_Chu/z_en_bom_chu.cpp). Split applied: EnBomChu_Destroy 0x0020EB70 FUN_0020eb70 (224-byte tail, kept as asm).
- FUN_00333ddc = EnBomChu_Explode: moved into the actor .cpp; GLOBAL_ASM removed from src/functions/functions_320000s.cpp (ws only).

UNMATCHED (draft under #if 0, GLOBAL_ASM kept):
- EnBomChu_Init: best 30/106 words. ROM derives the four colour-table pointers from one base with add-chains (r1=r0+4, r3=r1+4, ip=r3+4); C pointer chains fold to constant offsets. Also ROM zeroes r6 before vldr and loads the timer as 0xB4 (180). Table access via data_syms.s EQU (EnBomChu_sColors 0x521248).
- FUN_003e4ea4 = EnBomChu_WaitForRelease: 75/81 words, built 512 B vs ROM 324 B. ROM tail-calls Explode (beq FUN_00333ddc, pop), C version calls it and returns. Structure differs (player load, timer base r0=self+0x100).
- EnBomChu_Draw: best 41/84 words. Frame 0x3c and MTX at sp+0xc match after operator[] vec; remaining: ROM keeps SetUnkAC(1) in r5 from entry, VFP numbering of 0.0/100.0/255/1/255 constants, FUN_003695cc env colour = (ci, 0, 0, 1-ci) as (x*255)*(1/255).

NOT ATTEMPTED: EnBomChu_Update (not in the prompt list; still GLOBAL_ASM).

Debt:
- WaitForKill (actionFunc 0x0013CAF8) is raw code inside FUN_0013bb74's data tail (no tsv row); referenced by a raw cast. A symbol EQU in data_syms.s did not reach the object file, so the cast is used.
- Header offsets (3DS): axes at 0x1B0/0x1BC/0x1C8, visualJitter 0x1D4, flags 0x1AA-0x1AC. Explode writes bomb timer at +0x26C (raw).
