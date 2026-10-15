
<!-- merge 2026-10-15 19:17:15 -->
# En_Syateki_Man (G42 Haiku pass) status

Baseline: ws_check.sh = only FUN_00249af8, 0 non-function bytes (2026-10-15, after the changes below).

| Function | Status | Notes |
|---|---|---|
| EnSyatekiMan_Destroy | MATCHED 0/8 | |
| EnSyatekiMan_BlinkWait | MATCHED 0/12 | `s16 t = blinkTimer - 1; if (t != 0) store; else blinkFunc = FUN_001310a0` |
| EnSyatekiMan_Start | MATCHED 0/52 | cfg tail split: FUN_00196A80 (124 B, ws split/asm) — the ROM span of Start (208 B) contains another function after the literal pool |
| EnSyatekiMan_Idle | MATCHED 0/20 | |
| EnSyatekiMan_SetupIdle | MATCHED 0/23 | needs TU-defined text tables (see data below) |
| EnSyatekiMan_Talk | MATCHED 0/84 | same data requirement |
| EnSyatekiMan_EndGame | MATCHED 0/129 | same data requirement; item-get logic uses itemGetInf[0] and CUR_UPG_VALUE |
| EnSyatekiMan_StopTalk | MATCHED 0/38 | |
| EnSyatekiMan_WaitForGame | MATCHED 0/65 | |
| EnSyatekiMan_GivePrize | MATCHED 0/23 | |
| EnSyatekiMan_FinishPrize | MATCHED 0/41 | itemGetInf[0] (0xF08) bits 0x2000/0x4000 |
| EnSyatekiMan_RestartGame | MATCHED 0/21 | |
| FUN_001310a0 | MATCHED 0/32 | = EnSyatekiMan_Blink (N64 shape) |
| FUN_0019efd8 | MATCHED 0/14 | countdown (counter @0x59C) -> WaitForGame |
| FUN_00284070 | MATCHED 0/27 | OverrideLimbDraw: limb 7 = head (gameResult==REFUSE negates headRot.y), limb 0 = body |
| EnSyatekiMan_Init | MATCHED 0/47 | raw byte store for attentionRangeType (0x1F) — debt, Actor has no field in repo |
| EnSyatekiMan_StartGame | MATCHED 0/53 (Sonnet) | gallery (`actor.parent`) loaded right after the Message_ShouldAdvance check, before the cameraHold block; `if (FUN_00374be8(play, 0x17)) { counter = 3; actionFunc = FUN_0019efd8; } else actionFunc = WaitForGame` |
| EnSyatekiMan_Update | MATCHED 0/33 (Sonnet) | signature `(Actor* thisx, GameState* state)` + `PlayState* play = (PlayState*)state` fixed the timer register |
| EnSyatekiMan_Draw | MATCHED 0/26 (Sonnet) | dead read kept with `s32 flag = (self->gameResult == SYATEKI_RESULT_REFUSE);` before the 3rd model call |

Data (debt/infra, needs orchestrator step on merge):
- sTextIds (0x52F4F8) and sTextBoxCount (0x52F500) are now C arrays in the actor TU with
  `__attribute__((section("EnSyatekiManTextData")))` (non-const: const folds the values away). Pinned by
  data/oot3d.ld region `EnSyatekiManTextData +0 { *(EnSyatekiManTextData) }` which replaces the old
  `z_En_Syateki_Man_ASM.data +0 { *(i.z_En_Syateki_Man.data) }` (same 16 bytes, same position).
  The actor cpp no longer has GLOBAL_ASM("data/z_En_Syateki_Man.data.s"). On merge: drop data_chunks.txt row
  `z_En_Syateki_Man.data,0052F4F8,0052F508` and apply the ld region change to oot3d.ld by hand.
- Init uses `ACTOR_ATTENTION_RANGE_TYPE` and PlayState uses `SHOOTING_GALLERY_STATUS` (raw offset 0x5C74):
  local macros in the actor cpp (debt, a field in include/ would be better).

Other ws changes: split/asm/EnSyatekiMan_Start.s + FUN_00196A80.s, data/keep_symbols.txt (cfg_split).
Typed header z_en_syateki_man.hpp: N64 offsets +0x36C from actionFunc (0x568) on; skelAnime at 0x1A4; model 0x598; counter 0x59C.
