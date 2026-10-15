
<!-- merge 2026-10-13 19:45:15 -->
# En_Js (solo barrido, Opus 2026-10-13)
Matched 10/12: Init, Destroy, Draw, OverrideLimbDraw (3DS: inline X-rotation of limb 8 mtx), 6 action FUN_s moved in.
Left: EnJs_PostLimbDraw = guarded function-local static Vec3f (guard 0x528988, obj 0x59B068) -> `static` (LOADER_RECIPE).
Left: EnJs_Update (147 insns) -> big.
Idioms: N64 En_Js_SetupAction inline fixes hoisted action literal; `Actor* thisx = &self->actor` routed through talk/offer code fixed reg order (FUN_003f0a08).
