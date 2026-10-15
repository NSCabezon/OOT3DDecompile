
<!-- merge 2026-10-15 16:32:06 -->
# En_Syateki_Niw (G35 batch, Haiku first pass) — STATUS

ws_check: baseline only (FUN_00249af8; 0 non-function bytes).

| Function | Where | Status |
|---|---|---|
| EnSyatekiNiw_Destroy | actor .cpp | MATCHED (0/20 words). Collider stub inlined by armlink; loop uses `&self->actor` (thisx form differs) |
| EnSyatekiNiw_Init | actor .cpp | MATCHED (0/107). Uses `self->actor.` everywhere except Collider_SetCylinder(thisx) |
| FUN_00181800 (SetupDefault) | moved to actor .cpp, GLOBAL_ASM removed from functions_180000s.cpp | MATCHED (0/30) |
| FUN_00206320 (SetupArchery) | moved, GLOBAL_ASM removed from functions_200000s.cpp | MATCHED (0/41). Chained stores `a.z = a.zTarget = K` give ROM store order |
| FUN_00158508 (SetupRemove) | moved, GLOBAL_ASM removed from functions_140000s.cpp | MATCHED (0/80). Condition as `if (z>200 && z<800) { if (screenX>0 && ...) }`; FRAMES(30)/FRAMES(100) timers |
| FUN_003ca7b0 (Remove) | moved, GLOBAL_ASM removed from functions_3C0000s.cpp | MATCHED (0/117). Dead `s2` alias on the movementTimer check; `focus` local before SetFocus |
| FUN_00394300 (OverrideLimbDraw, head 0x394300..0x3944F8, 504 B) | stays GLOBAL_ASM (split/asm/FUN_00394300.s) | UNMATCHED (far: 95/126 words, 424 B vs 504 B). Draft under `#if 0`. Limb 7 = inlined 3DS Matrix_RotateAxis (FUN_003625f8 body: angle*40.7437*(pi/128)*40.7437) about axis (0,0,-1); limbs 4/6 shapes OK (right wing z,y negated). ROM does not constant-fold the axis (runtime vsqrt/vdiv, vmov copies), armcc folds it in every local/static/ctor/plain-static-helper shape tried (~10). |
| EnSyatekiNiw_Update | actor .cpp | MATCHED (0/376, Sonnet pass). N64 helpers (UpdateEffects/SpawnFeather/CheckHit) as plain `static` (gives the `push {r0,r1,..}` param spill), `(Actor* thisx, GameState* state)` + `PlayState* play = (PlayState*)state`, `thisx` for Actor_MoveForward/Collider_UpdateCylinder and raw `(PlayState*)state` for CollisionCheck_SetAC/OC, case ARCHERY before ALLEY, `timer > lifespan`, FRAMES(300) for the Default cluck, shootingGalleryStatus as raw `*(s8*)((u8*)play + 0x5C74)`, and the two UNUSED `Vector3f sp90/sp84(0,0,0)` locals from the N64 source (they fix the literal-pool order: 0.0 first). |
| EnSyatekiNiw_Draw | stays GLOBAL_ASM | UNMATCHED (far: 111/146 words, mnemonic diff 25, 604 B vs 584 B). Draft under `#if 0` (needs EQU `EnSyatekiNiw_sColors` = 0x004D9D2C in data_syms.s: 3 black colors of the TU rodata, sootShade = [2]). Blocker = zero/1.0 remat class: ROM keeps only `1` (SetUnkAC) hoisted in r7 and re-materialises 0 / 0x3F800000 per iteration (strd r0,r1 pairs), armcc hoists 0 (r7) and 1.0 (r8). ~25 variants (see comment in .cpp). |
| FUN_003944F8 (tail of the split, NOT FUN_003944FC) | moved to actor .cpp | MATCHED (0/22). Unknown owner actor (OverrideLimbDraw of some actor with a pointer at +0x16B4: limb 0 -> Matrix_RotateZ(mtx,1,obj->f14); Matrix_RotateY(mtx,1,(s16)obj->s18*9.587e-5)). |

## cfg split applied (ws only) -- CORRECTED by Sonnet
- The Haiku split `FUN_00394300 0x003944FC FUN_003944FC` was 4 bytes too late: the tail function starts with `ldr r0,[pc,#0x48]` at 0x3944F8 (before the `push`), so the head asm swallowed it. Re-split by hand in the ws: `FUN_00394300 0x003944F8 FUN_003944F8` (head 504 B, tail 88 B). Edited: split/asm/FUN_00394300.s (dropped trailing `ldr`), split/asm/FUN_003944F8.s (new, replaces ...FUN_003944FC.s), data/oot3d.ld region, data/keep_symbols.txt, split/splits.tsv, functions_380000s.cpp GLOBAL_ASM. On main use `apply_split_merge.sh ... FUN_00394300 0x003944F8 FUN_003944F8` (NOT 0x3944FC).

## Layout notes (3DS vs N64, derived from ROM)
- SkelAnime is 0x84 on 3DS: skelAnime 0x1A4, jointTable 0x228, morphTable 0x3FC, actionFunc 0x5D0.
- N64 offsets >= 0x250 map to 3DS +0x380 (e.g. focusYOffset 0x654, collider 0x67C, minigameType 0x61E).
- Model slots `models[5]` (stride 0x3C) at 0x70C, last slot runs past the 0x800 allocation size; InitVars uses 0x800 literal.
- ColliderCylinder is 0x58 on this tree.
- Data: EnSyatekiNiw_sCylinderInit = 0x52F528, EnSyatekiNiw_sInitChain = 0x52F560 (data_syms.s).

## Header change
- z_en_syateki_niw.hpp: `unk_6D4[0x38]` + `models[5]` replaced by `EnSyatekiNiwEffect effects[5]` (stride 0x3C at 0x6D4; model ptr at +0x38 = old models[i].model); sizeof(EnSyatekiNiw) == 0x800 now, InitVars uses sizeof.

## New files (need `git add -f` on merge, .s under src/)
- src/game/actors/En_Syateki_Niw/data_syms.s
