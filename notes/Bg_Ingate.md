# Bg_Ingate status (Opus closing pass)
All 6 functions MATCHED in C (BgIngate_Init, Destroy, Update, Draw, DoNothing, FUN_00108890 moved).
BgIngate_Init: the "6th stack arg" was actually colHeader = NULL (sp+4) scheduled before the FUN_00372f38 call;
the real call is the 5-arg header prototype. Extern ReadCollisionHeaderFromZsi (armlink-inlined) escapes &colHeader,
which suppresses the Actor_Kill tail call. ws_check: baseline only.
