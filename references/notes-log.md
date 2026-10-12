# Notes log

Every note the user (or a reviewer) gave on a finished video, and what catches that kind of problem now.
Add a row per note; see "When the user sends notes after watching" in SKILL.md.
Catcher: `lint:<code>` (scripts/lint.py), `qa:<code>` (scripts/qa.py), or a rubric id from review-checklist.md.
Verified: the check fires on the render the note was about.

| video | scene, time | note | catcher | verified |
|---|---|---|---|---|
| meteotsunami | S05 93-99 s | uplifted sea sat as a static plateau while narration said "giant wave" | lint:static-hold, B2 | yes |
| meteotsunami | S05 107.6 s | empty frame between the uplift and the sensor network | lint:blank, F1 | yes |
| meteotsunami | S05 118-126 s | chain built from the left, right half of the frame empty | lint:lopsided, E1, E2 | yes |
| meteotsunami | S06 | forced wave a pure dip here, crest-ahead + trough in S07/S12 | C2 | yes (Haiku caught it from the rubric) |
| meteotsunami | S06 | harbor water drawn over the top of the breakwater | D2 | no |
| meteotsunami | S07 | time axis "t" placed well below its axis | D3 | no (Haiku missed it) |
| meteotsunami | S07 | leader from gauge to inset cut through the pressure curve | D4 | yes |
| meteotsunami | S08 220.9 s | "Cancún" label gone while still being said | lint:label-gone, lint:label-flash, B5 | yes |
| meteotsunami | S08 221-228 s | damage list (streets, homes, boats...) said over a static street | lint:static-hold, B4 | yes |
| meteotsunami | S08 | brace labeled "1-2 m" against 1.2 m of drawn water | B3 | no (Haiku missed it) |
| meteotsunami | S13 429.8 s | render 0.6 s longer than its slot, end cut | lint:slot | yes |
| meteotsunami | S13 | harbor water ended in a cliff short of the frame edge | D1 | yes |
| meteotsunami | S13 | basin and response curve not linked | D8 | no |
| meteotsunami | S03 end | ended on a people icon instead of the sign | D9, C1 | no |
| meteotsunami | S14 457-470 s | right half of the frame empty | lint:lopsided, E1 | yes |
| meteotsunami | S05, S07 | tide gauge drawn two ways; buoy glyph read as a joystick | C1, D6 | yes |
| meteotsunami | S02, S15, S18 | 1-3 s of empty frame at scene start | lint:blank | yes |
