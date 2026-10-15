<!-- merge 2026-10-13 18:38 -->
# Item_Etcetera (solo-haiku, 2026-10-13) — merged
- Matched: ItemEtcetera_Update (fn ptr tail call @0x1AC), ItemEtcetera_Draw, ItemEtcetera_DrawThroughLens.
- Draw keys: re-read `*(SkeletonAnimationModel**)(self+0x1B0)` at EVERY use (no model local) → ROM `ldr r0,[r4,#0x1b0]` reloads + tail call. Lens flag = `*(u8*)(state+0x208F)`.
- Destroy: draft under #if 0, 9/12 words (ROM loads model into r1 before `mov r4,r0`; vtable slot +4 call).
- Not attempted: Init, UpdateFireArrow, FUN_00129f2c, FUN_003f529c; MoveFireArrowDown big.
- (Opus) MoveFireArrowDown MATCHED: guards/colors stay EQU (syms.s), but velocity/accel are real file-scope `static Vec3f` (TU .bss pinned `z_item_etcetera.bss` at 0x5A2ABC in data/oot3d.ld) → armcc rematerializes `ldr r3,=accel; sub r2,r3,#0xc` at the call. Accel init via placement-new ctor `ItemEtceteraVec3f(x,y,z)` (setter gave s0/s2 swap); velocity init via setter.
