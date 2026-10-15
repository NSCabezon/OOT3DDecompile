
<!-- merge 2026-10-13 19:55:48 -->
# En_Niw_Lady (solo barrido, Opus 2026-10-13)
Matched 12/16: Init, Destroy, OverrideLimbDraw FUN_0022de08, 9 action FUN_s moved in (struct mapped: N64 0x250 block = 3DS +0x5F0).
Near: EnNiwLady_Draw 2w (FaceAnimations::FUN_0035e3a4 arg setup order; play2 param fixed the rest).
Big: FUN_00154904 (WaitForObject 155), FUN_001792f4 (cucco count 196), EnNiwLady_Update (226).
Idioms: GiveItem(..., self->getItemId = K, ...) inline assignment; if/else instead of ternary for actionFunc gives shared store tail.
