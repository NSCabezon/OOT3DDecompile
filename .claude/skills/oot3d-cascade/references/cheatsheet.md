# Matching cheatsheet (OoT3D, armcc b839) — read BEFORE writing C

Most diffs come from a handful of shapes. Check this list against the ROM asm before trying random variants.

## Before writing
1. Copy the N64 function (`tools/repos/oot/src/overlays/actors/ovl_<A>/`) as the starting point: same control flow, same helpers, same branch order. Then apply 3DS offsets (actor fields +0x58; `Actor` = 0x1A4).
2. Use symbols, never raw addresses: `gSaveContext.x`, `gGameInfo`, EQUs in the actor's `data_syms.s`. A raw `*(u16*)0x...` alone changes register choice.
3. Signature: try `(Self* self, PlayState* play)` + `(ActorFunc)` cast in InitVars first. If ROM keeps the Actor* around: `(Actor* thisx, PlayState* play)` + `Self* self = (Self*)thisx;`.

## Reading the diff → what to try
| ROM shows | Try |
|---|---|
| r4/r5 (self/play) swapped | other signature (above); locals order (`play` before `self`); route args via `Actor* thisx` |
| extra `mov r5,r4` copy | second local `Self* s2 = self;` used in one call |
| `b target` tail call missing | close the scope of any address-taken local with `{}` before the last call |
| tail call present but you inline | move callee into a separate .cpp in the actor dir |
| Destroy: arg setup then `mov r0,#1` with no `bl` | `Collider_Destroy*` 2-insn stub inlined by armlink: write the plain N64 call; if your build emits `bl`, see CLAUDE.md "armlink --inline" (callee must be a C function in ANOTHER file) |
| `mov r0,r0` at end / after call | linker-inlined empty call or tail-reorder to NEXT function — not your C |
| `e320f000` nop extra/missing | swap if/else ↔ ternary |
| predicated `ldreq/streq` vs your `bne` | N64-style `static inline` setup helper; or store via `((PlayState*)state)` |
| duplicate stores merged/not merged | `thisx->f` vs `self->actor.f` for that one store |
| loop unrolled | `DECR(x)` macro inside the loop |
| Spawn args: ROM sets `mov r2,(play)` before `mov r1,..` | `{ PlayState* play2 = play; Actor_SpawnAsChild(&play2->actorCtx, parent, play2, ...); }` — play2 for BOTH args |
| float regs swapped | put the float in its own `f32` local before the call; write multiply/compare operands in ROM order; clamp as ternary `d = (d > K) ? K : d` |
| compare-chain vs `ldrlo pc` table | write the FULL N64 case list incl. cases equal to default |
| colHeader / DynaPoly | ALWAYS call real `ReadCollisionHeaderFromZsi(DynaPolyInfo_Alloc(&dyna, play, n), &colHeader)`; never inline it |
| 2/3 speed | `v * 2.0f / 3.0f`; timers `n * 3.0f / R_UPDATE_RATE + 0.5f`; if no gGameInfo load: `n>0 ? (s32)(0.5f+(n*3.0f)*0.5f) : (s32)((n*3.0f)*0.5f-0.5f)` |
| action-func literal hoisted early into ip, ROM loads it late into r0 | N64 `static inline void Self_SetupAction(Self* self, ActionFunc f)` helper |
| action-func pool load scheduled wrong in Setup tail | `s16 yaw = shape.rot.y; world.rot.y = yaw;` |
| local `s16 arr[6] = {...}` copied with `ldm/stm` (you get memcpy) | wrap array in struct `__attribute__((aligned(4)))` inside an EQU rodata struct; copy struct (En_fHG) |
| Spawn float args (pos+K) loaded before the int stack args in ROM | N64-style `f32 x = ..; f32 y = .. + K; f32 z = ..;` locals before the Spawn call (En_Dnt_Nomal GivePrize) |
| `mov r4,r5` copy of actor mid-function (one reg for bgId store, other for rest) | N64 inline helper taking `Actor* thisx` (cast inside) + pass `(DynaPolyActor*)actor` (Bg_Spot11_Bakudankabe Init) |
| ROM `mov r2,#K; str r2,[getItemId]` / branches share final `str actionFunc` via `b` | `GiveItem(.., self->getItemId = K, ..)` inline assign; `if/else` instead of `?:` for the actionFunc store (En_Niw_Lady) |
| bitfield `lsl16; lsr26` | plain s16 `(params >> 10) & 0x3F`, not PARAMS_GET_U |
| Draw reloads `ldr r0,[r4,#off]` before each model call + tail `b FUN_00372170` | re-read `self->model` at every use, no model local (Item_Etcetera Draw/DrawThroughLens) |
| min/clamp store with wrong reg order / `strgt` | two `s32` locals + ternary `x = (best > cur) ? cur : best;` (En_Ma3 UpdateTalkState) |
| ROM `bic r1,r0,#K; strb r1` but ours `bic r0` (flag clear) | test via `self->`, clear via 2nd alias `Self* s2 = self; s2->f &= ~K;` (En_Fd_Fire) |
| raw-address cast `(ActorFunc)0x...` + action ptr in wrong reg | EQU symbol in actor data_syms.s + declared fn (En_A_Obj) |
| float consts in wrong s-regs AND wrong literal-pool order | `f32 a,b,c;` declare in one order (→ reg numbers), assign in ROM load order (→ pool order); brute-force decl perms (En_Poh) |

## Hard rules
- Data arrays: define AFTER `<A>_InitVars`; arrays used only by still-asm code need `__attribute__((used)) static`. All-zero static arrays break (go to .bss).
- Moved FUN_s keep their exact `FUN_xxxxxxxx` name (linker-pinned).
- Drafts: `#if 0 ... #endif` + plain `GLOBAL_ASM` (never `#ifdef NON_MATCHING/#else`).
- No per-function `#pragma`. No `volatile` hacks unless stated in STATUS.md.
- Cheap loop: `scripts/fastchk.py` (~1 s) per variant; `ws_check.sh` after every match (fastchk masks relocated words: `bl` vs `mov` differences only show in ws_check).
- Unknown pattern? `grep -n "<keyword>" CLAUDE.md` (decomp-spike) — it has ~100 solved cases with actor names.
