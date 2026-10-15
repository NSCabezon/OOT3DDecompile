
<!-- merge 2026-10-15 17:55:53 -->
# En_Door STATUS (G41 haiku pass, 2026-10-15)

MATCHED (fastchk + ws_check baseline):
- EnDoor_Update, EnDoor_AjarWait, EnDoor_Check, EnDoor_AjarClose, EnDoor_WaitForCheck, EnDoor_AjarOpen (C, src/game/actors/En_Door/z_en_door.cpp).
- EnDoor_OverrideLimbDraw: C; reads the limb table 0x004D9466 and DL table 0x004D946B via raw casts (debt, no EQU).

UNMATCHED (draft under #if 0, GLOBAL_ASM kept):
- EnDoor_Destroy: 10/16 words. ROM keeps a dead `add r0,r4,#0x3cc` after the SkelAnime_Free2 call (bl, not tail); C version tail-calls.
- EnDoor_Draw: 40/51 words. Frame 0xC and push {r4-r7,lr} in ROM; C pushes r8 (model/dl locals). ROM loads objBankIndex first, then requiredObjectSlot.
- EnDoor_Open: 40/111 words. ROM keeps index (openAnim + dList*4) in r4 and loads 1.0f early; table reads 0x004D9489 / 0x004D949D (raw). Pointer-to-playSpeed and index-local variants tried (no gain or worse).
- EnDoor_Init: 80/102 words. ROM: `adds r0,#0x3cc; blne FUN_00342968` (flag-driven call), objectInfo in r4 / actor in r5 (C has them swapped). Tried decl order, NULL-check form, thisx chain: no gain. Table 0x00522B08 (EnDoorInfo[6]) and init chain 0x00522B00 are raw casts.

NOT ATTEMPTED: none of the listed. EnDoor_Idle and EnDoor_SetupType are still GLOBAL_ASM (not in the prompt list).

Header (actor dir): skelAnime SkelAnime at 0x1A4 (size 0x84), openAnim 0x3EA, playerIsOpening 0x3EB, unk_3EC (other->unk_192 in N64 = 1 set by Init), requiredObjectSlot 0x3ED, dListIndex 0x3EE, lockTimer 0x3E8, actionFunc 0x3E4. Size 0x3F0.
