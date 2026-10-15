# Bg_Ice_Objects: status (stage 2, Sonnet)

Baseline: `scripts/ws_check.sh Bg_Ice_Objects` shows only FUN_00249af8 (known). Current state clean.

| Function | Status | Notes |
|---|---|---|
| BgIceObjects_Destroy | MATCHED (C) | 48 B |
| BgIceObjects_Update | MATCHED (C) | 8 B |
| BgIceObjects_Draw | MATCHED (C) | 120 B; animSpeed loaded after MTX34CopyAsm, kept in s16 |
| BgIceObjects_Init | MATCHED (C) | colHeader=NULL local at top + Math_Vec3f_Copy after ReadCollisionHeaderFromZsi, as in N64 order |
| FUN_001979d0 (Idle) | MATCHED (C, in actor file; GLOBAL_ASM removed from functions_180000s.cpp) | use self->dyna.actor (no thisx alias); float literals -340.0f etc. in SetNextTarget; single s16 x16 var, no z16 |
| FUN_00196f54 (Slide) | asm (GLOBAL_ASM) | C in `#if TRY_SLIDE` matches except sWhite/sGray: orig does `ldr r1,=0x511f88; sub r0,r1,#4` twice (same-TU statics); with EQU externs armcc emits 2 literals (+4 B) or CSEs into r7 (+push, +4 B slot). Step speed 0.75f lives at 0x511F90 (sBlock[3]). |
| FUN_0015441c (Reset) | MATCHED (C, GLOBAL_ASM removed from functions_140000s.cpp) | no thisx alias; speedXZ=0 before actionFunc store |
| BgIceObjects_Stuck (0x001976E4) | raw address | Lives as DCB bytes inside BgPoEvent_BlockWait.s (not disassembled). Referenced via `((BgIceObjectsActionFunc)0x001976e4)`. Debt. |

Data: tables live in Bg_Hidan_Syoku's raw dump (0x511F80..0x511FE8). Exposed as absolute EQU symbols in `BgIceObjects_data.s` (no duplicate data). sZeroVec (zero Vec3f) is .bss at 0x5699E0 (no linker rule for this actor), referenced only by Slide's asm.

Files outside the actor dir: none changed (src/functions/functions_*.cpp identical to oot3d except the pre-existing `GLOBAL_ASM("asm/FUN_00144618.s")` line that is in the ws copy only). include/: none.

## Opus closing pass (2026-10-13)
- Draft fixed: `if (velocity.y <= 0) flags &= ~0x10;` (ROM uses ldrls/bicls/strls, not ternary) and `spread * Math_CosS/SinS` (vmls operand order). With those the ONLY remaining diff is the colors.
- Proven: with `static Color_RGBA8 sWhite = {250,250,250,255}; static Color_RGBA8 sGray = {180,180,180,255};` in the TU, FUN_00196f54 is 0/252 words different (fastchk). Two *separate* same-TU statics -> armcc merges literals late (`ldr =sGray; sub #4`, reloaded each call).
- Every extern form fails: two EQU symbols (2 literals, +4 B); array `[-1]/[0]`, `[0]/[1]`, struct {white,gray,...} members, `__asm("name")` aliases, weak/const, `__schedule_barrier`, inline spawn helper -> base CSE'd into r7 (push r7, frame 0x2c, +4 B); raw int addresses (worse, +8 B). Even a same-TU static *array* sC[2] CSEs - must be two distinct objects.
- To match: split Bg_Hidan_Syoku's dump at 0x511F84..0x511F8C and define sWhite/sGray (and likely sInitChain/0.75f step, sXStarts...) in this TU. Needs data-dump/linker change -> out of scope. Left as GLOBAL_ASM.
