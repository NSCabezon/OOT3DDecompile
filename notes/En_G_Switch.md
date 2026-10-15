
<!-- merge 2026-10-14 12:56:50 -->
# En_G_Switch status (cascade stage 1, Haiku, batch 1/1)

Matched (moved into src/game/actors/En_G_Switch/z_en_g_switch.cpp, GLOBAL_ASM removed from functions_*.cpp):
- EnGSwitch_Destroy: matched (Collider_DestroyCylinder + FUN_0034fda8 tail call, models at 0x9B4).
- FUN_00238cb4 (Kill): matched.
- FUN_0037e450 (DrawPot): matched.
- FUN_002593d0 (WaitForObject): matched (uses FUN_00352ee0 with modelIds at 0x90C).
- FUN_001745ac (SilverRupeeCollected): matched.
- FUN_002692ac (DrawRupee): matched (mtx declared inside the !broken block so the final call becomes a tail call).
- FUN_003df554 (SilverRupeeTracker): matched (sCollectedCount, sMajorScale, sfx pointers via data_syms.s EQUs).

Not matched:
- FUN_00198288 (SilverRupeeIdle): MATCHED in stage 2 (Sonnet) with `s16 cnt = sCollectedCount; cnt++; sCollectedCount = cnt;`, moved to the actor .cpp, GLOBAL_ASM removed from functions_180000s.cpp.

Not attempted: none (FUN_002073c0 and FUN_001e9c1c call FUN_00238cb4 but are outside the list and not touched).

Other: EnGSwitch_Init and EnGSwitch_Update remain GLOBAL_ASM (not in this batch). Header EnGSwitch now has typed 3DS fields (+0x58 vs N64) and models/modelIds arrays. New file data_syms.s holds EQUs for 0x523C14, 0x523C54, 0x54AC20, 0x54AC24.

Stage 2 (Sonnet), part A:
- EnGSwitch_Update: not matched, 8/150 words (VFP callee-saved numbering of the effect loop temps vs 0.8f/250.0f consts). Draft #if 0 in actor .cpp; header now has typed EnGSwitchEffect effects[40].
- FUN_002073c0 (ArcheryPot): not matched, 34/151 words (GPR i/thisPos swap, s19/s20 consts); loop bound is data word 0x523C18 (EQU EnGSwitch_sStatics.shardCount); `PlayState* play2` for the Kakera call and s16 phi_s0 needed. Draft #if 0. GLOBAL_ASM kept.
- EnGSwitch_Init: not matched, 61/207 words (register numbering only; modelIds[1]/[i+2]=0x41, (Actor*,PlayState*) signature). Draft #if 0.

Stage 2 (Sonnet), part B:
- FUN_001e9c1c (GalleryRupee): MATCHED (0 words). Moved to actor .cpp (local EnGSwitchGallery view of the parent EnSyatekiItm; `__fabsf` via inline wrapper; `f32 vy = velocity.y;` local fixed the home.y-50 compare reg order; collider flag clear before parent load), GLOBAL_ASM removed from functions_1C0000s.cpp.
- FUN_0033ba54 (Break + SpawnEffects inlined): not matched, best 86/198 words (same size). Matrix must be a Break-scope local to share the sp+0 outgoing-arg slot, but then the inlined helper reads it via pointer (r5=sp base); randPos only stays in memory when passed by pointer to the helper. Draft #if 0. Not shared: only called from En_G_Switch (FUN_001e9c1c, FUN_002073c0).
- FUN_001e5048 (DrawEffects): not matched, 240/330 words off; inlined Matrix class (translate/scale/rotXYZ) - same class as Bg_Menkuri_Eye Draw. Draft #if 0. No cfg tail (pool inside listed size).

Stage 3 (Opus):
- EnGSwitch_Init: MATCHED. Dead alias `EnGSwitch* s2 = self;` used only for the first store (`s2->type = ...`), `thisx` as the Collider_SetCylinder actor arg in case 2, `thisx->shape.yOffset` in case 3.
- EnGSwitch_Update: MATCHED. N64 signature `(Actor* thisx, PlayState* play)`, `Collider_UpdateCylinder(thisx, ...)` + dead alias `s2` only in `CollisionCheck_SetAC(..., &s2->collider.base)`.
- FUN_002073c0: 2 words (loop-end `cmp n,i; bgt` vs ROM `cmp i,n; blt`). Draft updated (scale inline in the Kakera call; thisPos, i, angle, play2 declared inside the AC_HIT block).
- FUN_0033ba54: unchanged (86). Helper-local mtx gives +8 frame; fully inlined loop puts randPos in regs.
