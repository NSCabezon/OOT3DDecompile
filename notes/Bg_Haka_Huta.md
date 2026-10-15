# Bg_Haka_Huta (cascade stage 1, Haiku)

Baseline after this stage: ws_check shows only FUN_00249af8 (known).

| Function | Status |
|---|---|
| BgHakaHuta_Init (0x240254) | matched (sInitChain via raw ptr 0x511108, data GLOBAL_ASM kept) |
| BgHakaHuta_Destroy (0x240328) | matched |
| BgHakaHuta_Update (0x276eb4) | matched |
| BgHakaHuta_Draw (0x276e68) | matched |
| FUN_003e69b8 (SpawnEnemies) | matched, moved into actor .cpp (GLOBAL_ASM removed from functions_3E0000s.cpp) |
| FUN_003ebcdc (Open) | matched, moved into actor .cpp (GLOBAL_ASM removed from functions_3E0000s.cpp); PlaySfx inlined as static helper |
| FUN_003df814 (SlideOpen, includes inlined SpawnDust) | NOT matched, still asm: uses function-local statics (guard vars at 0x51110c, primColor/envColor at 0x511110/0x511114, sEffectAccel at 0x56995c). Reproducing needs the data block 0x511108.. laid out exactly, which conflicts with the GLOBAL_ASM data file. Stage 2: try raw-address statics + manual guard, or split the data. |
| FUN_0012795c (func_8087D720, Quake/Haka move) | NOT matched, still asm: function-local statics D_8087D958/D_8087D964 (guards at 0x51111c/0x511118, data at 0x569968/0x569974), 680 B, quake calls. Same data problem as above. |
| BgHakaHuta_DoNothing | not located yet (not checked in stage 1). |

Notes:
- 0x511108 block is shared: data/z_Bg_Haka_Huta.data.s must stay as GLOBAL_ASM. Removing it (test) shifted the layout and broke ws_check.
- Struct: DynaPolyActor (0x1BC) + actionFunc 0x1BC, counter 0x1C0, unk_1C2 (s16, N64 unk_16A), skelAnimModel 0x1C4, unk_1C8 (always NULL).

## Stage 2 (Sonnet)
Both remaining functions reached near-match in C (kept under `#if 0` in z_bg_haka_huta.cpp), NOT exact:
- FUN_003df814: 4 words off (only the order of two vmov/vstr in the sEffectAccel ctor init, s0/s1 swap).
- FUN_0012795c: 6 words off (m[1][1]/m[1][0] store order + const/counter register swap before FUN_003625f8).
Key findings: function-local statics must be real C++ statics with dynamic init (`static Vector3f x(a,b,c)`; guards `_ZGV*` land in .data in exactly the original order 0x511108.. so the whole data block can be C: sInitChain first, statics declared inside functions placed AFTER InitVars). The 3 bss Vec3f (0x56995c, 0x24 B) need an ld rule: `z_bg_haka_huta.bss +0x00F73C { *z_bg_haka_huta.o(+BSS) }` and `z_bg_treemouth.bss +0x168` (data/oot3d.ld, outside actor dir) - reverted because functions do not match exactly. Statics must be declared after MTX34CopyAsm in FUN_0012795c; rotMtx in inner block (shares [sp] arg slot); SlideOpen statics inside the `!Math_StepToF` block; sfx duration 50 and shares effectPos.
Reverted to asm + raw address 0x00511108 (ws_check baseline only).

## Stage 3 (Opus) - final
Result: both still asm (cascade ends). ws_check = baseline only. Workspace left exactly in the stage-2 state (data GLOBAL_ASM, ld unchanged, GLOBAL_ASM lines in functions_120000s/3C0000s kept); only the `#if 0` block comment updated.
- Reproduced stage-2 state (data block as C, ld rule `z_bg_haka_huta.bss +0x00F73C` + treemouth `+0x168`, both FUN_s moved): 6 / 4 words off. Data bytes matched (0 non-function diffs), so the data/ld side works.
- Built a compile-only checker (tmp/fast.py, ~0.8 s/variant, compares .o words vs ROM ignoring relocs) and ran ~10k automated variants.
- FUN_003df814: `static Vector3f` ctor allocation always comes out x->s0,y->s1 (ROM x->s1,y->s0). Tried: ctor-body/StaticVec3f, `= Vector3f(...)`, 1-elem array (N64 shape), separate SpawnDust/PlaySfx helpers (17 off), static placement, local decl perms, effectVel/effectPos store orders, xPosOffset forms (2304-variant search). Only exact match: a contrived ctor `ZV(a,b,c) : x(b), y(a), z(c)` with all-zero args -> rejected as register-steering fake (documented in the `#if 0` block).
- FUN_0012795c: two independent bits. (a) m[1][0]/m[1][1] store order: fixed by writing `m[1][1] = 1` before `m[1][0] = 0`, but that flips the D_8087D958/D_8087D964 ctor register allocation. (b) `vmul` of counter * 0.10667452f (= 191*pi/5625, N64 191*pi/3750 scaled 2/3; = 6.112 deg) always gets K in s1 / counter in s0 (ROM: K s0, counter s1). Tried operand order, double M_PI form (fpmode=fast demotes, same code), deg*DEG_TO_RAD (not folded, +2 insns), local/reused angle var, inline RotY / RotAxis helpers, arg order (MTX34RotAxisRad_(out, axis, rad) signature), Vector3f axis, s16 local. 5760 + 3840-variant searches (decl perms x row order x angle form x ctor type x sincos form): best 6 words.
- Finding: FUN_003625f8 = nn::math MTX34RotAxisRad_ (rad->fidx internally); the RotY block (sin/cos with `angle != 0` shortcut, 9.58738E-5 = 2pi/65536) is an inlined helper not present in repo headers.
