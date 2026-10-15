
<!-- merge 2026-10-14 18:16:59 -->
# Bg_Haka_Trap (sonnet stage, G4) — STATUS

ws_check.sh: baseline only (FUN_00249af8).

## Matched (C, byte-identical under fastchk + ws_check)
- BgHakaTrap_Destroy, FUN_0019ba38, FUN_001ca810, FUN_00345fe0 (haiku)
- FUN_001777d8 (SpikedCrusher_Lift; single `goto done` so 20.0f is not hoisted to entry)
- BgHakaTrap_Init (data via actor-dir data_syms.s EQUs: sInitChain/sColChkInfoInit/sCylinderInit/TrisInit; FanBlade_Idle EQU 0x1758EC; sSpikedCrusherFlip lives at PlayState+0x7F74; 13-arg FUN_00372f38 via fn-ptr cast; actionFunc store last in fan/crusher arms)
- BgHakaTrap_Draw (inline N64-order MultVec3f wrapper; `s32 idx = actor->params` local; Vec3f vtx declared BEFORE MTX34 mtx; f32 x_,z_,y_ init order / z,y,x store order)

## Not matched (drafts under #if 0, GLOBAL_ASM kept)
- BgHakaTrap_Update (52): ~15 words off. Two issues: (1) ROM keeps play in r1 for the actionFunc call so the decrement temp is r2 (ours r1 + `mov r1,r5`); (2) ROM `mov r6,r7` copy of colChkCtx before SetAC/SetOC in the guillotine arm. ~25 variants (play2 param, alias locals, signatures A/C/D) did not move it.
- FUN_001cb334 (SpikedCrusher_Fall) and FUN_001e8684 (Guillotine_Fall): drafts match everything EXCEPT the Quake block: ROM hoists the small int consts (countdown, 8/5, three zeros; 4 also folded into 0xa60+4 for the cam index) into callee-saved regs (push r4-fp) and spills Quake_Add result to stack; ours rematerialises them. Fall differs only there. Locals/params/s16 typing/inline helper did not reproduce it. Fall draft is the first thing to retry if someone finds the hoisting trigger (same trigger likely used in other Quake callers).
- FUN_001ca65c (SpikedWall_Burn): guarded function-local static (static, LOADER_RECIPE).
