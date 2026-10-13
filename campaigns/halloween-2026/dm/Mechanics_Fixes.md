# The Reveler's Stage — Mechanics Fixes (Master Draft v1)

Drop-in replacements for the DM Guide sections on Mordax, the Stage Fill, bonds, the Session 3 shuttle, and the Session 4 Echoes. Items marked **[NEW]** are decisions I made to close a gap; change any you disagree with.

---

## 1. The Stage Fill (Despair Tracker)

A single d10 counter, persistent across all four sessions. **Range 0–10, clamped. Starts at 3.**

**+1 when:**
- A named NPC dies
- The party fails a check and the failure has a real consequence
- A player drops to 0 HP
- The party makes a meaningful sacrifice

**−1 when:**
- The party does something genuinely heroic or funny
- The party saves an NPC
- A player expresses genuine in-character care for another player

Session-specific adjustments (from each Resolution) apply on top and are clamped to 0–10.

### What the Stage Fill does in Session 4 [NEW: replaces the overlapping thresholds]

Legendary actions are bought with **points per round**, so the counter maps directly onto what Mordax can do.

| Stage Fill | Legendary points / round | Other effect |
|---|---|---|
| 0 | 1 | "Cowed": The Hollow (3 points) is unavailable even if points are gained later |
| 1–3 | 1 | — |
| 4–6 | 2 | — |
| 7–10 | 3 | +2 to all of Mordax's attack rolls and save DCs |

Legendary action costs: **Script Change = 1, Hush = 2, The Hollow = 3.**

> Dropped as redundant: "5 = one free legendary action" and "0 = loses one permanently." Both are covered by the table above.

---

## 2. Bonds

A **bond** is a pair of players who share a genuine, in-character moment of care, loyalty, or sacrifice for each other. The DM marks it on the Bond Tracker the moment it happens. A pair can only be marked once. **Maximum 5 bonds.**

**Guidance:** aim for about one bond per session in Sessions 1–3, with the rest earned in Session 4. A stat-block trade-off or a purely tactical heal doesn't count; the table should feel the moment.

**Effect on Mordax in Session 4:** each bond reduces his **maximum HP by 15** and his **AC by 1** (in Phases 2 and 3; Phase 1 AC stays 15).

| Bonds | Max HP | Phase 2 starts at | Phase 3 starts at | AC in Phases 2–3 |
|---|---|---|---|---|
| 0 | 230 | 153 | 76 | 17 |
| 1 | 215 | 143 | 71 | 16 |
| 2 | 200 | 133 | 66 | 15 |
| 3 | 185 | 123 | 61 | 14 |
| 4 | 170 | 113 | 56 | 13 |
| 5 | 155 | 103 | 51 | 12 |

> **Fix:** the old text used fixed thresholds (150 / 75). With 5 bonds his max HP was 155, so Phase 1 lasted 5 HP. Thresholds now scale: **Phase 2 at ⅔ of current max HP, Phase 3 at ⅓ (round down).**

---

## 3. Mordax, the Laughing Dark

*Huge ancient entity, chaotic evil.* Tuned for five to six level-7 characters (roughly CR 9–10). **Re-check the numbers against six players when Session 4 is built.** Spell save DC **15** for everything below (16 effects at Stage Fill 7+ via the +2 rule).

**Common to all phases**
- **Speed:** 40 ft, fly 40 ft (hover)
- **Damage resistances:** psychic, necrotic; bludgeoning/piercing/slashing from nonmagical attacks
- **Condition immunities:** charmed, frightened
- **Legendary Resistance (3/day).** If the True Name is complete, he cannot use it during Phase 1.
- **Lair actions** continue in every phase: at initiative 20 choose **one** per round, not the same one twice in a row. (Spotlight, Applause, Curtain; Curtain only once per phase.) [NEW: clarifies that lair actions persist.]

### Phase 1: "The Director"
Mordax stays in the Front Row and does not attack. **AC 15.** He takes damage normally while he is in his seat (he is 60 ft from the stage, so the party must cross the House or use ranged attacks). Phase 1 ends when he drops to the Phase 2 threshold above.

**Lair actions (initiative 20):**
- **Spotlight.** One creature, DC 15 Wis save or it sees only darkness outside a 10-ft radius and cannot perceive allies until the start of its next turn.
- **Applause.** 30-ft cone, 4d8 psychic, DC 15 Con save for half.
- **Curtain.** A 60-ft Wall of Force drops like a heavy curtain. Lasts 1 minute or until the DM drops it.

### Phase 2: "The Performer"
He rises from his seat and enters the fight. **AC 17 (minus bonds).**

- **Multiattack.** Three attacks per turn, any mix:
  - *Grasping Claw.* +8 to hit, reach 10 ft, 2d8 + 5 psychic.
  - *Laughter Barb.* +8 to hit, range 60 ft, 3d6 psychic, and DC 15 Wis save or frightened until the end of the target's next turn.
- **Feeding (bonus action).** One creature at 0 HP within 60 ft: Mordax regains 2d10 HP.

### Phase 3: "The Hollow"
The mask drops. **Necrotic Mantle:** his melee attacks deal an extra 2d6 necrotic. **Unrelenting:** his speed can't be reduced below base. **Vulnerability: radiant.**

### Legendary Actions (3 points max per round; set by Stage Fill)
- **Script Change (1).** Move up to 30 ft without provoking opportunity attacks.
- **Hush (2).** One creature within 60 ft loses the ability to speak until the end of its next turn (no verbal spells, **and it can't make a Declaration**).
- **The Hollow (3).** DC 15 Wis save or stunned until the end of its next turn.

---

## 4. The Narrative Kill Condition

Mordax can't be destroyed by damage alone. [NEW: concrete procedure.]

**Declarations.** A *Declaration* is when a player says, in character, something genuine they value about another player's character at the table. A player can make one at any time (it's a free action, no roll). **Every player at the table** must make one Declaration (six when everyone is there; a character who is offstage under the Intermission rule is not required to, and **can still be the subject** of someone else's). Two players can name the same person, but nobody may declare about themselves. Hush, being unconscious, or being out of earshot blocks a Declaration.

**At 0 HP:**
- If every Declaration has been made, he is destroyed.
- If not, he collapses into rags and starts a **3-round Reform Clock**. Players may make their Declarations during it. If every Declaration is done before the end of round 3, he is destroyed.
- If the clock runs out, he rises with **40 HP in Phase 3 form** and Stage Fill +1 (no bonds are lost).

---

## 5. Session 3: Crew Roster and Shuttle Seats [NEW]

The original text said "12 crew," "7 remaining crew," and "more of you than seats," but never gave a seat count. People who may claim a seat (13 in all; the full roster is in `S3_Crew_Roster.md`):

| Group | Who | Count |
|---|---|---|
| Players | The six sleepers in the Cryo Bay (not station crew) | 6 |
| Real survivors | Dr. Elara Voss (infected), "Cutter" Marcus Webb, **Ines Okafor, geologist (new, unnamed in the original)** | 3 |
| Mimics | Four doppelgangers wearing the four dead crew | 4 |

**Shuttle: 8 seats** [CHANGED from 7 for six players]. The six players take six if they choose; the remaining two seats are the real decision. Voss, Cutter, and Okafor all have claims, the mimics will lobby for a seat, and the party doesn't yet know which of the people they've met are real.

> If you want one more notch of tension, drop to **7 seats** (one open seat for three humans).

---

## 6. Session 4: The Echoes [CHANGED: supersedes the earlier "Echo-trio" draft]

The players keep their own bodies all campaign, so the Echoes are no longer host souls. They are **Mordax's past victims**, the former cast members the party met in Sessions 1 to 3. There are exactly **five Echoes** (this also resolves the old 15-hosts-versus-5-Echoes mismatch).

| Echo | From | Proposed one-time boon (once per fight) [PROPOSED] |
|---|---|---|
| **Luna Crooke** | Session 1 | She answers one question about Mordax's current phase or next legendary action |
| **Elspeth and Dorian** (the Twins, counted as one) | Session 1 | One ally moves up to 30 ft through a wall, curtain, or trap door |
| **Sera Whitmore** | Session 2 | One creature at 0 HP rises with 15 HP and ends the frightened condition |
| **Marcus "Cutter" Webb** | Session 3 | One ally automatically ends a grapple, restraint, or stun |
| **ARGO** | Session 3 | Her voice breaks Hush: one silenced player may speak for one turn |

**Engaging an Echo warmly in roleplay = Stage Fill -1** (max -5, one per Echo). The party reaches level 7 by a normal level-up at the start of Session 4. The Echoes' boons are separate from leveling.

---

## Open items for you

1. **Stage Fill start of 3.** I picked it so Session 1 has room to go both ways. Higher means a darker campaign.
2. **Legendary points / The Hollow at 0.** I added "Cowed" so a very low Stage Fill feels earned.
3. **Seats = 8, plus Ines Okafor.** Approved. Okafor is my invention; swap if you'd like a different third survivor.
4. **Lair actions persisting in all phases.** The original didn't say.
5. **Declaration rules.** I wrote a concrete procedure and a 3-round Reform Clock. Say if it should be harder.

Still pending: the Session 1 encounter rebalance (Harwick) and the full Session 4 build-out.
