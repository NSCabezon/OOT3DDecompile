# Actor_1D9 — Opus closing pass
- Actor1D9_Init: MATCHED (C). `&play->GetObjectStatus(objBankIndex)->zarInfo` as a `zar` local, `ReadCollisionHeaderFromZsi(zar->FUN_003532c0(0), &colHeader)` with `colHeader = NULL`, `gSaveContext.masterQuestFlag` -> Actor_Kill.
- Actor1D9_Update: MATCHED (C). Constants as locals assigned up front (wrap/scale/zero, then step, dist); timer re-read via `((Actor1D9*)actor)->timer`.
- Actor1D9_Destroy, Actor1D9_Draw: matched (earlier stage).
- FUN_003d0ed4: not attempted (function-local static guard / shared model loader, needs data symbols outside actor dir).
- ws_check: baseline only (FUN_00249af8).
