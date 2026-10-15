# En_Sth (Gold Skulltula House people) - stage 3 (Opus) status: ALL MATCHED

ws_check.sh: baseline only (FUN_00249af8).

| Function | Status | Notes |
|---|---|---|
| EnSth_Destroy / EnSth_Update | matched (stage 1) | |
| FUN_0010f9b4 (WaitForObject) | matched (stage 1) | |
| EnSth_Init | MATCHED (stage 2) | N64 store order (requiredObjectSlot, drawFunc), `params` local, (EnSth*, PlayState*) signature, drawFunc address held in local `ActorFunc draw` before the stores |
| FUN_001df8c0 (Draw) | MATCHED, moved into actor .cpp | uses the C color tables (raw 0x52F1D4 literals would get CSE'd/folded by armcc) |
| FUN_00111e7c / FUN_00111ee8 (Parent/Child RewardObtainedWait) | MATCHED, moved | |
| FUN_00111f68 (RewardObtainedTalk) | MATCHED, moved | |
| FUN_0012cb98 (RewardUnobtainedWait) | MATCHED, moved | |
| FUN_0012cc10 (RewardUnobtainedTalk) | MATCHED, moved | GivePlayerItem inlined, wallet via upgrade mask/shift tables |
| FUN_0012ccdc (GiveReward) | MATCHED, moved | |
| FUN_001dfa30 (Update2) | MATCHED (stage 3) | signature `(Actor* thisx, GameState* state)`, locals `play` then `self`, `thisx` passed to Collider_UpdateCylinder/Actor_MoveForward/Actor_UpdateBgCheckInfo |
| FUN_003cd920 (SetupAfterObjectLoaded) | MATCHED (stage 3) | N64 helper `EnSth_SetupShapeColliderUpdate2AndDraw(Actor*, PlayState*)` kept as a static fn (auto-inlined); `Actor* thisx = &self->actor` local, params read via `thisx->params`, tail `params = &thisx->params` |

Data (stage 3): actor data is now real C after InitVars (sCylinderInit, sObjectIds, sAnimIdx, sRewardObtainedWaitActions, sEventFlags, sGetItemIds, float RGBA colors) — `data/z_En_Sth.data.s` no longer included; a non-static `u32 EnSth_sUnused = 0;` reproduces the zero word at 0x52F124. Save/upgrade accesses use `gSaveContext.inventory.{gsTokens,upgrades}`, `gSaveContext.eventChkInf[13]`, `CUR_UPG_VALUE(4)`. Only `EnSth_sModelIdx` (0x59B644, in .bss, no ROM data) remains as an EQU in syms.s.
3DS: Update2 sets skelAnime byte +0x81 (=1 when animationType==8); Setup uses FUN_00372f38 / FUN_00353c9c (model + skel by cmb/csab index); shirt colors passed via FUN_00357a50; limb draw funcs FUN_0016dc1c/FUN_0015074c are generic.
