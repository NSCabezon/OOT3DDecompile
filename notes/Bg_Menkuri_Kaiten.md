# Bg_Menkuri_Kaiten: status (cascade stage 1, Haiku)

Workspace: ws/Bg_Menkuri_Kaiten. ws_check.sh: only baseline FUN_00249af8 differs.

| Function | Status | Notes |
|---|---|---|
| BgMenkuriKaiten_Init | MATCHED (C) | DynaPoly init, FUN_00372f38(…, 4, 0) model load, colHeader via ReadCollisionHeaderFromZsi (armlink inlines it, no bl). |
| BgMenkuriKaiten_Destroy | MATCHED (C) | DynaPoly_DeleteBgActor, then FUN_00350f34 (tail call). |
| BgMenkuriKaiten_Update | MATCHED (C) | Flags_GetSwitch + FUN_0032d8d8 (DynaPolyActor_IsPlayerAbove) + FUN_00373264 sfx; rot.y += 0x55 (0x80 scaled 2/3). |
| BgMenkuriKaiten_Draw | MATCHED (C) | Mori_Idomizu-style draw; animSpeed must be assigned AFTER MTX34CopyAsm (else literal load order differs). |

Data: init chain (ICHAIN scale 100/1000) stays in data/z_Bg_Menkuri_Kaiten.data.s at 0x00512DC0; referenced via EQU symbol in sBgMenkuriKaitenInitChain.s (no raw-address hack).
Action FUN_s: none (actor has no actionFunc).
