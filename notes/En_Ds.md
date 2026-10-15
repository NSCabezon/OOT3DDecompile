
<!-- merge 2026-10-15 17:23:07 -->
# En_Ds (G38, Haiku pass)

- MATCHED (C, 0 words off): EnDs_Destroy, EnDs_Draw (uses GraphicsContext_UnknownStub for the empty N64 Gfx_SetupDL_37Opa), EnDs_OverrideLimbDraw, EnDs_Talk, EnDs_TalkNoEmptyBottle, EnDs_TalkAfterGiveOddPotion, EnDs_DisplayOddPotionText, EnDs_GiveOddPotion, EnDs_TalkAfterBrewOddPotion, EnDs_BrewOddPotion1, EnDs_BrewOddPotion2, EnDs_BrewOddPotion3, EnDs_OfferOddPotion (switch form), EnDs_OfferBluePotion (switch + nested rupee switch), EnDs_GiveBluePotion
- UNMATCHED (drafts under #if 0, GLOBAL_ASM kept):
  - EnDs_Init: 4 words off, all in the tail (actionFunc store and unk_1E8/unk_1E4 stores: ROM computes base &self->unk_400 before the fn-ptr store). Tried store orders I3-I5.
  - EnDs_Update: 7 words off (ROM keeps play in r6 and hoists the 0x1838 constant into r5; tried play2 alias, hoisted step local, cached unk_1DE pointer, signature change).
  - EnDs_Wait: 4 words off in the else branch (ROM loads yaw fields, then 0x116 literal, then stores textId; C variants tried: order swaps, actor alias, s16 locals).
  - EnDs_PostLimbDraw: NOT C. Blocked by a guarded function-local static `sMultVec` (guard 0x522B4C, object 0x5990A4): needs pin_static / LOADER_RECIPE (orchestrator-only).
- Offset facts (3DS): unk_1D8 = 0x430 (Vec3s), unk_1DE = 0x436, unk_1E4 f32 = 0x43C, unk_1E8 u16 = 0x440, brewTimer u16 = 0x442, actionFunc = 0x444, model = 0x448, jointTable 0x228, morphTable 0x32C. Timers are 3DS-scaled (BrewOddPotion1 30, BrewOddPotion2/OfferOddPotion 90).
- Splits: none. No include/ edits. Header z_en_ds.hpp rewritten with typed fields (actor-dir only).

## Sonnet pass (G38)
- MATCHED (0 words): EnDs_Init (`thisx->targetMode = 1`), EnDs_Wait (`Actor* thisx` alias; `yawDiff = thisx->yaw.. - thisx->shape.rot.y; thisx->textId = 0x5048;`).
- UNMATCHED: EnDs_Update 7w (~250 mutation variants: play2/s2 aliases on every site, signature variants, step local types/positions, inline helper; ROM has play=r6, ptr(&unk_1DE)=r7, 0x1838 const=r5; ours play=r5, ptr=r6, const reuses r5).
- EnDs_PostLimbDraw: draft under #if 0 (static Vector3f sMultVec(1100,500,0); limb 3; VEC3TransformAsm(&focus.pos, mtx, &sMultVec)): fastchk 2 words (pool words only). Orchestrator pins with pin_static.py (guard 0x522B4C, obj 0x5990A4).
