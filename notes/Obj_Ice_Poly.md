
<!-- merge 2026-10-15 11:00:00 -->
# Obj_Ice_Poly (G28 haiku stage)

Matched (C, fastchk 0 words; ws_check baseline only):
- ObjIcePoly_Update (2 insns, tail call through actionFunc at 0x1A4)
- ObjIcePoly_Destroy (18 insns; armlink-inlined Collider_DestroyCylinder written as plain calls)
- ObjIcePoly_Init (83 insns). Data tables are EQU symbols in src/game/actors/Obj_Ice_Poly/data_syms.s (0x53518C sOffsetY, 0x535194 / 0x5351CC cylinder inits, 0x535204 sScale). Matching shape: `(s16)((u16)params) >> 8` for the params byte, muls before the mass/alpha stores.

Not matched (left as asm, draft under #if 0):
- ObjIcePoly_Draw (107 insns, 102/111 words off, size 492 vs 444). The 3DS Draw does an inline Z/X rotation of the copied model matrix (sinf/cosf of +-0.1227 rad) and a model branch (FUN_003695cc x2, SetUnkAC, FUN_003721e0, FUN_00372170). Structure is close, but register allocation and stack frame (ROM push {r4,r5,lr}, sp+4 matrix) differ and STACK_PAD is not available in the ws. Not attempted further.

Notes: header z_obj_ice_poly.hpp uses the 3DS layout (actionFunc 0x1A4, iceCollider 0x1AC, hardCollider 0x204, model 0x25C). No cfg splits.

## G28 sonnet stage
Drafts under #if 0 in z_obj_ice_poly.cpp: ObjIcePoly_Draw 16w (shared `RotCols(m,c0,c1,angle)` loop helper, `mov r5,#1` hoist + last-row load order remain), ObjIcePoly_Melt 22w (N64 code; tail rounding/VFP numbering; also needs sColorWhite/Gray as real statics at the start of the data dump), ObjIcePoly_Idle 144w (function-local static Vector3f with guard @0x535188 / obj @0x5a2ea4 => pin_static, Player raw offsets). data_syms.s: + sColorWhite 0x535180 / sColorGray 0x535184.
