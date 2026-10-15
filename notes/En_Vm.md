
<!-- merge 2026-10-14 22:31:08 -->
# En_Vm (G16, haiku stage)

| Function | Status | Notes |
|---|---|---|
| FUN_0039bb60 | MATCHED | SetupWait (timer 15, 3DS layout). Moved to z_en_vm.cpp; GLOBAL_ASM removed from functions_380000s.cpp |
| FUN_00285a7c | MATCHED | Stun. Moved to z_en_vm.cpp. cfg split: tail FUN_00285be0 (12 B) kept as asm. Setup-wait branch written inline (ROM does not call FUN_0039bb60 there, different store order) |
| FUN_0016f36c | MATCHED | OverrideLimbDraw (play, limb, MTX34*, thisx). Moved; GLOBAL_ASM removed from functions_140000s.cpp |
| FUN_001acb6c | MATCHED | EffectSs_Spawn wrapper (zero vector via data_syms.s EQU 0x598E4C). Moved |
| FUN_001acac4 | MATCHED | EffectSs_Spawn wrapper, 11 stack args. Stack args a6..a12 must be s32 (u8 gives 36/42 words off). Moved; GLOBAL_ASM removed from functions_180000s.cpp |
| FUN_002503e4 | MATCHED | Die (timer, bomb spawn, drop, Actor_Kill). Moved; GLOBAL_ASM removed from functions_240000s.cpp |
| EnVm_Destroy | MATCHED (sonnet) | tail call `FUN_003685a0(&self->animModel)` (= dtor-like loop of the 0x64C SkeletonAnimationModel_unk_0C member; the `pop; mov r0,r0` is armlink --tailreorder to the NEXT function) |
| EnVm_Draw | draft #if 0 (matches the code modulo static layout) | Draw reads its guard as `*(0x52FF5C+0x24)`: guard shares ONE TU .data section with the guards of FUN_002a8568 (Wait, 0x52FF5C) and FUN_0016f3d0 (PostLimbDraw, 8 guards 0x52FF60..0x52FF7C); objects 0x59B778..0x59B7F0 (Wait 0x59B778, PostLimbDraw 0x59B784..0x59B7D8, Draw 0x59B7E4). Can only be enabled together with PostLimbDraw in C; then use `pin_static.py ws/En_Vm split 0x52FF5C --size 0x28` + guard/bss regions for the whole range |
| FUN_002a8568 (Wait) | MATCHED (sonnet, not in the task list) | 0 words. FUN_001acac4 must be `__attribute__((noinline))` at the call site; `{ f32 one = 1.0f; playSpeed = one; }` block fixes the late 1.0f load. Guard 0x52FF5C / obj 0x59B778 pinned via pin_static `pin` |
| FUN_0016f3d0 (PostLimbDraw) | draft #if 0, ~107 instrs off | limb 2 part ~matches (8 guarded static Vector3f + locals); ROM hoists `mov sb,#0` (poly=NULL) above the limb test (unsolved class) and limb 5 is inlined Matrix_Translate(NEW) integer stores (MakeTrans) + RotateZ inline + Scale |
| EnVm_Init | draft #if 0, ~10 instrs off | animModel.unk_00 store after GetCMAB via pointer copy; scene check if-converted |
| EnVm_Update | draft #if 0, ~28 instrs off | see comment above the draft |

Debt: EnVm struct in z_en_vm.hpp is partial (offsets from 3DS ROM; 0x228..0x498, 0x4A8.., 0x548.. are padding).
Data: src/game/actors/En_Vm/data_syms.s (EnVm_sZero = 0x598E4C).
