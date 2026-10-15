# Shared "model manager" static (guard 0x0055A21C, object 0x005BE5B8): recipe

Proven on Item_Inbox `FUN_003a0e88`: it matches byte for byte, and `ws_check.sh Item_Inbox` shows only the baseline `FUN_00249af8`.

## Root cause
- The object is a **function-local static inside a header `inline` function**: `inline ModelManager& GetModelManager() { static ModelManager sInstance; return sInstance; }`.
- armcc inlines the guard test, `__cxa_guard_acquire`, the ctor, `__aeabi_atexit` and `__cxa_guard_release` into every caller. About 384 ROM functions reference 0x5BE5B8; some use offset literals such as 0x5C05B8 (= +0x2000).
- armcc emits the static as COMDAT sections that the linker deduplicates:
  - `.bss__ZZ15GetModelManagervE9sInstance` (ZI): the object, at 0x005BE5B8.
  - `.data__ZZ15GetModelManagervE9sInstance` (RW, 4 bytes): the guard. It is the **last word of .data** (0x0055A21C; .data ends at 0x0055A220).
- ctor = `FUN_0036788c` (returns `this`, as AEABI ctors do). dtor = `V00` (0x0048B1F0). `__dso_handle` = 0x00100000 (shown as `__ctr_start`).
- `__aeabi_atexit` and `__cxa_guard_release` are **empty C functions**. `armlink --inline` turns each call into `mov r0, r0`.
  - An asm `bx lr` stub is NOT inlined, because an asm symbol has no size. So `__aeabi_atexit` has to be C.
- armcc emits the `nop` (e320f000) after `cmp r0,#0` and after `ldr r0,=guard` itself when scheduling requires it (FUN_003a0e88 has them, EnGanonMant_Destroy does not). Never add them by hand.

## Infra (every file outside the actor dir)
1. **NEW `include/model_manager.hpp`**: inside `extern "C++" {}`, so actor .cpp files can include it from inside their `extern "C" {}` block and keep the C++ mangling.
   - `ModelAllocator` has virtuals vf00/vf04/`Create(cmb, arg)` and `void* owner` at +8.
   - `ModelManager` has `allocator` at +0x17C, plus a declared (not defined) `ModelManager()` and `~ModelManager()`.
   - `inline ModelManager& GetModelManager()` holds the static.
2. **NEW `src/game/model_manager/model_manager.cpp`**:
   - Empty C definitions of `__aeabi_atexit(void*, void(*)(void*), void*)` and `__cxa_guard_release(unsigned int*)`.
   - `GLOBAL_ASM("../src/game/model_manager/model_manager_syms.s")`.
3. **NEW `src/game/model_manager/model_manager_syms.s`**:
   ```
   _ZN12ModelManagerC1Ev EQU 0x0036788C, CODE32   ; ", CODE32" is required, else L6805E on the bl
   _ZN12ModelManagerD1Ev EQU 0x0048B1F0, CODE32
   __dso_handle          EQU 0x00100000
   ```
   Each symbol is EXPORTed.
4. **`src/functions/functions_300000s.cpp`**: delete `GLOBAL_ASM("asm/__aeabi_atexit.s")`. The C version takes its place at 0x00303B10; the scatter pins the section `i.__aeabi_atexit`.
5. **`data/oot3d.ld`**:
   - Right after the `data_54AC28` region:
     ```
     model_manager.guard +0 /* 0x0055A21C */
     {
         *(.data__ZZ15GetModelManagervE9sInstance)
     }
     ```
   - After `err.bss`:
     ```
     model_manager.bss 0x005BE5B8
     {
         *(.bss__ZZ15GetModelManagervE9sInstance)
     }
     ```
6. **The data dump loses its last word (0x55A21C).**
   - Workspace stopgap: `src/data/data_54AC28.s` is a copy of `disassembly/data/data_54AC28.s` without the final `DCD 0x00000000`, and `src/data/data.cpp` now uses `GLOBAL_ASM("../src/data/data_54AC28.s")`.
   - **Proper fix in main:** split the chunk in `disassembly/data_chunks.txt` (`data_54AC28,0054AC28,0055A21C`), regenerate `data/data_54AC28.s` and keep data.cpp unchanged. Do not keep a 15k-line copy of the dump in src/.

What is safe:
- The 380+ asm functions still use raw literals, so they are unaffected.
- Several C TUs can each emit the COMDAT; the linker keeps one copy.
- The object is ZI, so it is not in code.bin; the guard word is 0 in both ROM and build.

## C pattern at a call site
```c
#include "model_manager.hpp"          // inside the actor's extern "C" { } is fine
...
ModelAllocator* alloc = GetModelManager().allocator;   // guard+ctor+atexit expand here
alloc->owner = owner;                                    // ROM: str rOwner,[r5,#8]
model = alloc->Create(cmb, 1);                           // ldr r3,[r0,#8]; blx r3
alloc->owner = NULL;
```
- Write the owner set, call and reset out at the call site. Wrapping them in an inline member gave different `mov rX,#0` placement.
- Each `GetModelManager()` use repeats the guard block. ArrowFire_Init has two of them, so it calls it twice.
- Fields at other offsets (EnGanonMant_Destroy reads `[0x5C05B8 + 0x47C]` = sInstance+0x247C) are added as members of `ModelManager`. armcc forms `&sInstance+0x2000` by itself, giving the same literal.

## Item_Inbox FUN_003a0e88: register tricks that were also needed (beyond the static)
- Signature `(void* owner, GameState* state, s32 entry, s32 arg3)`, with `PlayState* play = (PlayState*)state;` first and the raw `state` passed to `FUN_0033da8c`.
- `Object_GetIndex` goes through `static inline s32 X(PlayState* play, s16 id)`, called with an `s32 objectId = row->objectId` local and a **u16** field. This gives ROM's `ldrh`+`sxth` and `index` in r4.
- `ModelTableEntry* table = (ModelTableEntry*)0x004D88C8; row = &table[entry];` fixes the r0/r1 temp order. The raw address is debt: it should become an EQU symbol.
- `play->GetObjectStatus(index)->zarInfo` (existing PlayState inline) for the zar base.

## How to apply to the other actors (En_Si, En_Nutsball, Item_Shield Init; En_Ganon_Mant Destroy/Update)
1. Merge the infra above into main once: files 1-5, plus the data_chunks split.
2. In the actor .cpp, `#include "model_manager.hpp"` and replace any hand-written `__cxa_guard_acquire((unsigned int*)0x0055A21C)` / `(void*)0x005BE5B8` code with `GetModelManager().allocator` (or another member).
3. Remaining diffs are ordinary register work. Try the usual levers: `GameState* state` + cast local, raw `state` to callees, inline wrappers with narrow param types, a local for the table base.
4. Check with `fastchk.py`, which masks relocs, then ws_check. The bytes of the guard block (nops, `mov r0,r0`) only show up correctly after linking.

## Per-actor local statics (e.g. En_Hs2 PostLimbDraw: guard 0x5273DC, object 0x59AFFC)
The same placement method applies, with one catch about section names:
- In a **plain function**, armcc puts the static in the TU's anonymous `.bss` and the guard (local `_ZGV...`) in an anonymous `.data` section of its own. These sections cannot be told apart by name in the scatter file, which is why En_Hs2 hit L6224E.
- If the static instead sits in an **`inline` accessor** (for example `inline T& X_GetS() { static T s; return s; }` (plain `inline`, NOT `static inline`) in the actor .cpp or a header, called from PostLimbDraw), armcc emits it as COMDAT with unique names: `.bss__ZZ<mangled>E1s` and `.data__ZZ<mangled>E1s`. After inlining, the code is the same.
  - Pin the two sections with scatter regions, as in step 5: `<name>.guard +0` right after the data chunk that ends at the guard, and `<name>.bss <addr>`.
  - Remove the guard word from the data dump: split the chunk in data_chunks.txt. Note that a guard sitting in the middle of a chunk needs a 3-way split.
- Fallback: put the function with the static alone in its own .cpp, and pin `*thatfile.o(+BSS)` / `*thatfile.o(+DATA)`.
- Ctor/dtor: if the ROM ctor is inlined (Vec3f init), define it inline. Use an EQU alias with `, CODE32` only when the ROM calls an out-of-line asm ctor/dtor.

## Multiple uses in one function (Opus, ItemShield_Init)
ROM reloads the 0x005BE5B8 literal at each use → give each use its own scoped reference:
`{ ModelManager& mm = GetModelManager(); mm.allocator->owner = owner; }` / `{ ModelManager& mm = GetModelManager(); model = mm.allocator->Create(cmb, 1); }` / `{ ModelManager& mm = GetModelManager(); mm.allocator->owner = NULL; }`.
Writing `GetModelManager().allocator->...` inline caches &sInstance in a callee-saved reg (wrong).
