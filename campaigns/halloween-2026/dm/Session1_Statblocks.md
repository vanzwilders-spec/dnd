# Session 1 Stat Blocks: custom, built for six level-3 characters

*DM only. [DECIDED, Oct 12] Monsters are **custom** and tracked here and in DM's Ark, not pulled from 5e.tools. AboveVTT needs only an icon, a health pool and (nice to have) AC. **Anything the players can carry or keep (loot, scrolls, items) must come from verified source material.** Nothing below hands out a player item; the Collector only *holds* what the party already owns.*

**Party at a glance** (for tuning): HP 25 / 21 / 24 / 24 / 30 / 42. AC 14 / 15 / 14 / 16 / 18 / 12 (Kurield with chain shirt and shield, Oct 16). Proficiency +2. Save DCs of 12 to 13 are fair; 15 is harsh for most of them. Rough party damage on a good round: 35 to 50.

**Conventions.** To-hit and damage are written as ready-to-paste dice. Macro lines are plain dice expressions (`1d20+5`). Whether AboveVTT turns text in a token's notes into clickable rolls is **untested**; try one on the Collector token before Friday, and if it does not, paste the lines into the chat as `/roll` commands instead.

---

## 1. Harwick, the Grieving Butler (Climax, 4:30)

*Medium undead (incorporeal), lawful neutral. Token: a translucent butler holding a silver tray; weeping.*

| | |
|---|---|
| **HP** | 65 |
| **AC** | 14 |
| **Speed** | 0 ft walking, fly 40 ft (hover) |
| **Abilities** | STR 6, DEX 16, CON 12, INT 11, WIS 13, CHA 14 |
| **Saves** | WIS +3, CHA +4 |
| **Resist / immune** | Resist acid, cold, fire, lightning, thunder; **immune** necrotic, poison, charmed, grappled, restrained, exhaustion. **Not immune to frightened** (Oct 16), so Turn Undead works fully |
| **Senses** | Darkvision 60 ft, passive Perception 11 |
| **Challenge** | About CR 2 (working target) |

**Traits**

- **Incorporeal Movement.** Moves through creatures and objects as difficult terrain. Takes 5 force damage if it ends its turn inside an object.
- **Bound to Service.** Harwick **cannot enter a room with a lit hearth**, and cannot cross its threshold. If a hearth is lit while he is inside, he must leave that room on his next move. Hearth fire is the only thing that does this (magic light, Continual Flame and Dancing Lights do not).
- **Sunless Weeping.** At the start of each of his turns he weeps; creatures within 10 ft that can hear him have disadvantage on concentration checks.
- **Undead Nature.** Does not need air, food or sleep. Turn Undead works on him.

**Actions**

- **Multiattack.** One Life Drain and one I Must Serve.
- **Life Drain.** Melee, `1d20+5`, reach 5 ft. Hit: `2d6+3` necrotic. The target makes a **DC 12 CON save**; on a failure its HP maximum is reduced by half the damage dealt (minimum 1) until a long rest.
- **I Must Serve.** One creature within 5 ft makes a **DC 13 STR save** or is grappled and **dragged up to 15 ft toward the cellar stairs** (the grapple ends if it enters a room with a lit hearth). A grappled creature can use its action to escape (Athletics or Acrobatics, DC 13). *DC lowered from the DC 15 in the Guide; Hetfield's STR is 8 and a DC 15 would nearly always catch him.*

**Bonus action**

- **Servant's Step.** Moves up to 20 ft without provoking opportunity attacks.

**Reactions**

- **"May I be of service?"** When a creature offers him a task, forgiveness or a kind word, he may spend his reaction to stop and listen (no attack until his next turn). This is the opening for Release.

**Three ways it ends**

- **Fire.** All eight hearths lit: he cannot enter or cross any threshold, and at dawn his service ends.
- **Release.** A Persuasion or Performance check (DC 14) after the party names his grief ("you can set the tray down") and gives him leave to stop. Advantage if they have freed Luna, and advantage if the calico spirit Milo is allowed to flop at his feet (not cumulative). He sets down the tray and fades.
- **Break.** Reduced to 0 HP, he does not die: he retreats weeping into the cellar. Turn Undead (Kurield's Channel Divinity, DC 13 WIS save): Frightened and Incapacitated for 1 minute, and he flees; it ends early if he takes damage.

**Macros**

- Life Drain attack: `1d20+5`
- Life Drain damage: `2d6+3` necrotic
- Life Drain CON save DC 12: players roll `1d20+CON`
- I Must Serve DC 13: players roll `1d20+STR`

---

## 2. The Collector (Animated Armor; Entry Hall, Trophy Room)

*Medium construct, unaligned. Token: a polished suit of armor holding a tidy brass placard. Proud and polite.*

| | |
|---|---|
| **HP** | 45 |
| **AC** | 17 |
| **Speed** | 25 ft |
| **Abilities** | STR 14, DEX 11, CON 13, INT 3, WIS 3, CHA 1 |
| **Immune** | Poison, psychic, charmed, exhaustion, frightened |
| **Senses** | Blindsight 60 ft |
| **Challenge** | About CR 1 |

**Traits**

- **False Appearance.** While motionless it looks like an empty suit of armor.
- **Collect.** If **both** Slams in one Multiattack hit the **same creature**, that creature drops one **non-armor, non-spellcasting-focus item of its choice** (held, worn or carried), and the Collector takes it. It then uses its bonus action to **Retreat**.
- **A Proud Collection.** The Collector never goes into the Dining Room. It will **trade** an item back for a small one-line compliment or a "better piece" for the display (a roleplay beat, not a roll).

**Actions**

- **Multiattack.** Two Slams.
- **Slam.** Melee, `1d20+4`, reach 5 ft. Hit: `1d6+2` bludgeoning. (Average per round about 11, so it is not a damage fight.)

**Bonus action**

- **Retreat.** Moves up to its speed toward the Trophy Room without provoking. Items it holds are **displayed on the Trophy Room shelf**.

**Getting items back.** Three ways, all on the party: defeat it (items spill), trade (above), or a challenge in the Trophy Room (Sleight of Hand or Athletics DC 13, or Rivet's tools). No item is ever lost for good, and **the Collector never takes armor, weapons used as a primary attack, or spellcasting focuses**, which keeps the fight fun instead of crippling.

**Macros**

- Slam to hit: `1d20+4`
- Slam damage: `1d6+2` bludgeoning

---

## 3. Revenant Hounds x3 (Servant's Passage, Wine Cellar approach)

*Medium undead, unaligned. Token: translucent hound, hunched, ears forward.*

| | |
|---|---|
| **HP** | 16 each |
| **AC** | 13 |
| **Speed** | 40 ft |
| **Abilities** | STR 12, DEX 16, CON 11, INT 3, WIS 14, CHA 6 |
| **Skills** | Perception +6, Stealth +5 |
| **Immune** | Necrotic, poison, exhaustion |
| **Resist** | Cold, nonmagical bludgeoning/piercing/slashing |
| **Senses** | Darkvision 60 ft, passive Perception 16 |
| **Challenge** | About CR 1/2 each |

**Traits**

- **Hunts by Sound.** Each hound has advantage on Perception checks that rely on hearing. A noise made within 60 ft draws all three hounds to its source. A **Silence** sphere hides sounds made inside it.
- **Refuge.** The hounds never enter the Dining Room while its hearth burns.
- **Reforming.** A hound reduced to 0 HP dissolves and **reforms in the cellar after one hour**. They cannot be destroyed.

**The silence puzzle.** To cross the Servant's Passage unheard, each character makes a Stealth check (**DC 13**, advantage with a Silence sphere covering them, disadvantage in metal armor or when carrying a lit torch of oil). One loud failure alerts the hounds. A clever lure works instead: Butch's bell thrown far away, a coin tossed, Hetfield's bandore in another room.

**Actions**

- **Chill Bite.** Melee, `1d20+5`, reach 5 ft. Hit: `1d6+3` cold, and the target makes a **DC 11 CON save** or is **Chilled**: its STR score is reduced by 1, stacking (cannot go below 1). **Ends on a short or long rest.** Not lethal.

**Macros**

- Chill Bite to hit: `1d20+5`
- Chill Bite damage: `1d6+3` cold
- Chilled save DC 11: players roll `1d20+CON`
- Stealth DC 13: players roll `1d20+Stealth`

---

## 4. The Twins: Elspeth and Dorian (Drawing Room)

*Tiny/small ghost children. Token: two pale children in nightclothes. Playful, not hostile.*

| | |
|---|---|
| **HP** | 14 each (they only matter if attacked; they never fight back harder than a game) |
| **AC** | 12 |
| **Speed** | fly 30 ft (hover) |
| **Senses** | Darkvision 60 ft |
| **Immune** | Poison, necrotic, charmed, frightened |

**Traits**

- **Passage Step.** Once per round, a Twin can move through any of the three secret passages (Drawing Room to Servant's Passage, Study to Master Bedroom, Kitchen to Wine Cellar) and drag a "caught" player with it.
- **Statues (game).** Anyone seen moving when a Twin looks is **out** and is taken through a passage to a different room.

**Actions**

- **Cold Hands.** Melee, `1d20+4`, reach 5 ft. Hit: `1d6` cold the first time a character is caught. A second touch deals no damage and just moves them.

**Games.** Statues and Hide-and-Seek (see the DM Script, Act 2). Winning both earns the **rhyme**, one line per lit hearth.

**Macros**

- Cold Hands: `1d20+4`, `1d6` cold

---

## 5. Ashford, the Solicitor (Dining Room, Study)

*Medium humanoid, neutral. Token: a thin man in a suit with a ring of keys. Nervous smile.*

| | |
|---|---|
| **HP** | 18 |
| **AC** | 11 |
| **Speed** | 30 ft |
| **Abilities** | STR 9, DEX 11, CON 10, INT 12, WIS 12, CHA 14 |
| **Skills** | Deception +4, Insight +3, Persuasion +4 |

**Traits**

- **Coward.** Will not fight and bolts at the first threat. If cornered he surrenders and begs.
- **Bardic Inspiration (1/day).** As a bonus action, gives a creature within 30 ft a `1d6` to add to one check or save in the next minute. Hidden: he does not offer it until he is trusted.
- **Carries the Master Bedroom key.** Will not volunteer it.
- **Mordax's deal.** If shown forgiveness he breaks and confesses: his survival for delivering guests. **Redeemed: Stage Fill -1.**

**Actions**

- **Letter Opener.** Melee, `1d20+3`, reach 5 ft. Hit: `1d4+1` piercing. (A last resort.)

---

## 6. Luna / Edith Marrow (Kitchen)

*Medium humanoid (maid), neutral. Token: a middle-aged woman with a ladle. She does not look up.*

| | |
|---|---|
| **HP** | 10 (only for the AboveVTT token; she cannot be hurt in any way that matters) |
| **AC** | 10 |
| **Speed** | 30 ft |
| **Immune** | Psychic, frightened, charmed |

**Traits**

- **Only While Working.** She answers questions only while doing a task (peeling, stirring, polishing). Stop her work and she goes quiet.
- **Cannot Ask.** She cannot ask to be freed.
- **Freed by two things.** Her name ("Edith Marrow", found under the chair in the Hidden Chamber) and **a dinner for six served in the Dining Room**. Both together free her. **Stage Fill -1.** She is an Echo in Session 4.
- **No attacks.** If attacked she drops what she holds and stops.

---

## 7. Mordax (mirror, Pantry)

No stat block and no token health. He is an image in a mirror and a figure among the preserved guests. If attacked, the glass shatters and re-forms or he fades. **A voice, not a fight.**

---

## Quick table for the table

| Creature | Token HP | AC | Attacks | Save DC |
|---|---|---|---|---|
| Harwick | 65 | 14 | Life Drain +5 (`2d6+3`) and I Must Serve | CON 12 / STR 13 |
| The Collector | 45 | 17 | Slam +4 x2 (`1d6+2`) | n/a |
| Revenant Hound (x3) | 16 | 13 | Chill Bite +5 (`1d6+3`) | CON 11 |
| Elspeth / Dorian | 14 | 12 | Cold Hands +4 (`1d6`) | n/a |
| Ashford | 18 | 11 | Letter Opener +3 (`1d4+1`) | n/a |
| Luna | 10 | 10 | none | n/a |

## Open for you

1. **Test:** do AboveVTT token notes make dice clickable? (One quick check; fall back to chat `/roll` if not.)
2. **Harwick's save DCs** are 12 and 13 (the Guide had 15). Confirm.
3. **Token icons:** I can draw simple PNG icons, or you can pick from AboveVTT's library.
4. **Roll macros:** if you want proper D&D Beyond / AboveVTT macros later, tell me which one you prefer and I'll format them.
