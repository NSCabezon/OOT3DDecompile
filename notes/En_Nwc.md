# En_Nwc status (stage 1 Haiku, 2 Sonnet, 3 Opus)

Workspace: ws/En_Nwc (ws_check.sh: baseline only, FUN_00249af8)

| Function | Status | Notes |
|---|---|---|
| EnNwc_Destroy | MATCHED (C) | tail call to FUN_00161654 (Collider_FreeJntSph, not moved) |
| EnNwc_Update | MATCHED (C) | updateFunc call via blx r2, tail call CollisionCheck_SetAC |
| EnNwc_Draw | MATCHED (C) | empty (bx lr) on 3DS |
| EnNwc_ChickNoop | MATCHED (C) | empty (bx lr) |
| EnNwc_Init | MATCHED (C) stage 2 | data stays asm; EQU symbols in data_syms.s (EnNwc_sJntSphInit @0x52D1F8, element init = that pointer - 1, EnNwc_sChickActionFuncs @0x52D1C0). Single base pointer gives ROM's `sub r4, r1, #0x30`. |
| EnNwc_ChickFall | asm (draft under #if 0, 3/69 words) | `f32 v = velY - 0.1f; velY = v; if (v < -10.0f) velY = -10.0f;` + `bgFlags |= FLOOR` before `pos.y = floorY` gets everything but the r1/r2 swap of the const/bits regs in the int compare. ~25 variants.  Opus: +~35 more variants (compare forms, ternary/CLAMP_MIN, inline helpers, signature tricks GameState*/Actor*, helper param order/colCtx param, Vec3f temp, inline-all) -- r1/r2 swap is invariant. Accept as asm. |
| EnNwc_Idle | MATCHED (C) stage 3 (Opus) | dx/dz computed into a Vec3f temp `d`, then copied to dx/dz locals (+ local `s = sqrtf(test)`): prevChickPos.x/.z now share s0 like ROM. |

Layout: EnNwc struct: actor 0x1A4, collider 0x1A4 (elements at +0x1C), count 0x1C4, chicks 0x1C8 (stride 0x5C), updateFunc 0x788, size 0x78C.
Data: GLOBAL_ASM("data/z_En_Nwc.data.s") kept (chickActionFuncs @0x52D1C0, element init @0x52D1C8, sJntSphInit @0x52D1F8).
Files touched (stage 2 adds data_syms.s): ws/En_Nwc/src/game/actors/En_Nwc/z_en_nwc.cpp, z_en_nwc.hpp only. Nothing outside the actor dir.
