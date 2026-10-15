
<!-- merge 2026-10-14 10:15:04 -->
# En_Ms status (cascade stage 3, Opus) — ALL MATCHED

Matched in C (ws_check: baseline only): EnMs_Init, EnMs_Destroy, EnMs_Update, EnMs_Draw, EnMs_Talk, EnMs_TalkAfterPurchase, EnMs_Sell, EnMs_Wait.

- EnMs_Update (stage 2): `gSaveContext.sceneSetupIndex == 8` real symbol instead of raw EQU base (raw base made armcc if-convert).
- EnMs_Init (stage 3): N64 order with plain `0.0f` literals and `self->actor.` for mass/speedXZ/gravity/velocity.y (store order speedXZ, gravity, velocity.y as in ROM); dropping the `f32 zero` local fixed `mov r0,#0xff`.
- EnMs_Talk (stage 3): r2/r3 literal-reg swap was vreg numbering: dead-ish alias `Actor* thisx = &self->actor;` used for GiveItem fixes it (also `EnMs* s2 = self` or a `play2` alias did).

Data: `data_syms.s` EQUs for sPrices, sOfferTextIDs, sInitChain, sCylinderInit, focus height (EnMs_sGameStateBase now unused).
