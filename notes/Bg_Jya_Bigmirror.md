
<!-- merge 2026-10-14 22:08:21 -->
# Bg_Jya_Bigmirror (G13, haiku stage) - status

- BgJyaBigmirror_Destroy (30 insns): NOT MATCHED (near). Draft under `#if 0`, 11 words off. Everything matches except one `mov r0,r0` (linker-inlined empty call with the object pointer as arg) before the manager vcall. Virtual call recipe applied (manager at 0x0055A1A8, slot 4 = `Remove(obj)`, `_ZTI21BgJyaBigmirrorManager` EQU 0x7FFF0040 placeholder in a syms.s that is NOT wired yet). Three call-site variants tried (v1/v2/v3) without change.
- BgJyaBigmirror_Init (71 insns): NOT ATTEMPTED beyond analysis. Blocker: the 3DS body allocates the object through manager slot 3 with a `__FILE__` string literal placed in .text (path string from the original build; open issue per CLAUDE.md), plus AutoClass1 and FUN_00340e14 / ZAR GetCMABByIndex. Body differs wholly from the N64 Init.
- Stage2: BgJyaBigmirror_Destroy MATCHED (syms.s wired, stub returning arg via __asm GraphicsContext_UnknownStub, obj local before vcall).
