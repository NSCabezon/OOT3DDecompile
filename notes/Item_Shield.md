# Item_Shield (Opus closing pass, fresh ws)
- ItemShield_Init: MATCHED. Fix: each of the 3 GetModelManager() uses bound to its own `ModelManager& mm` local in its own `{}` scope (stops armcc caching &sInstance in a reg).
- Collider init 0x00531E5C -> EQU `ItemShield_sCylinderInit` in src/game/actors/Item_Shield/data_syms.s.
- Destroy, Update, Draw, FUN_003f4414, FUN_0015c554: matched (previous pass).
- ws_check: baseline only (FUN_00249af8).
