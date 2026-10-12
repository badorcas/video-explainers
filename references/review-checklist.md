# Frame review rubric (Gate 2)

A checklist a reviewer of any strength can follow. Each item is a yes/no question with a fixed way
to check it. "Looks fine" is not an answer: every item gets Y, N or NA, and every N becomes an issue
with the severity listed. The items come from defects that real reviews caught in finished scenes.

## Inputs
- `lint/summary.txt` and `lint/<Scene>_beats.png` (and `_beats2.png`, ...) from
  `python3 lint.py <transcript.json> --host=intercut.py --sheets file:Scene ...`. A beat sheet has the settled frame of
  every animation beat and a frame every ~3 s inside long animations (captioned "moving"), each with the narration
  said during it printed underneath. `WAIVED` lines carry the author's reason: judge the reason. `HOST` lines are
  covered by the host on camera: skip them.
- The storyboard (scene table and its **Encoding** section: what each color and marker means).
- The approved key-visual stills (`keyframes/approved/`), and the source figures if any.
- For any detail you can't see at 480p, grab a full-size frame: `python3 grab.py <Scene> <seconds into scene>`.

## A. Lint lines (do these first)
For each line in `lint/<Scene>.txt`, open the frame at its time and decide.
- **A1** Every `ERROR` is fixed. (blocking if a label vanishes mid-word or the slot is wrong; otherwise should fix)
- **A2** Each `CHECK` is either fixed or justified in one sentence you would accept from someone else. For
  `static-hold`, read the printed narration: if it names things (a list, a place, an object) that do not
  light up as they are said, it is N. (should fix)

## B. Narration against picture: go through the beat sheet frame by frame
- **B1** The main thing the narration names in this beat is visible in this frame or the next one. (blocking if it
  is the scene's key idea; else should fix)
- **B2** When the narration describes motion or change ("travels", "splits", "grows", "fades", "passes",
  "drifts"), two consecutive beat frames differ in exactly that way. A shape that just sits there while the
  narration says it moves is N. (should fix)
  *Seen:* an uplifted sea surface sat as a static plateau for 15 s while the narration said "giant wave".
- **B3** Every number or size claim on screen matches the narration and the drawing. Measure it: a brace
  labeled "1-2 m" must span 1-2 m of the drawn scale. (blocking if it contradicts; nit if only loose)
- **B4** When the narration lists items ("streets, traffic, homes, boats, docks"), each one is shown or
  highlighted in the same order, near the moment it is said. (should fix)
- **B5** A label the narration says stays up until about 1 s after the word ends (lint `label-gone`). (should fix)

## C. Consistency across scenes (once per video)
Make a short table: each recurring object or process, and the scenes it appears in. Put those
frames side by side.
- **C1** The same object is drawn the same way in every scene: same icon, same glyph, same color.
  *Seen:* a buoy drawn two different ways; a tide gauge drawn as a wave icon in one scene and as the map's
  inverted triangle in another. (should fix)
- **C2** The same physical process has the same shape and sign in every scene. Compare the frames directly.
  *Seen:* one scene showed the forced wave as a pure dip under the pressure, while two others showed a crest
  ahead and a trough under it. (blocking: it teaches two different things)
- **C3** Each color keeps the one meaning given in the storyboard's Encoding section. Check every colored
  element in the beat sheets against that list. (should fix)
- **C4** A key-beat scene lands on its approved still (same layout, same representation). (should fix)

## D. Drawing correctness (look at full-size frames)
- **D1** Every fill (water, ground, a band) ends at the frame edge or at a physical boundary (shore, wall, seabed).
  A free-standing vertical edge in mid-frame is N. *Seen:* harbor water ending in a cliff short of the frame edge;
  water ending as a vertical wall at the beach. (should fix)
- **D2** Things behave physically: floating objects ride the surface, water doesn't pass through solid walls,
  objects don't sink into the ground. (blocking if it teaches the wrong physics; else should fix)
- **D3** Each label sits right next to what it names, on the outside, not floating in the middle of nowhere.
  An axis label sits at the end of its axis. *Seen:* a time-axis "t" placed 0.6 units below its axis. (should fix)
- **D4** Leader and connector lines run through empty space. One that cuts across a curve or another label is N.
  *Seen:* a dashed leader from a gauge to its inset cutting through the pressure curve. (should fix)
- **D5** Several sources feeding one target use drops into a bus with one arrow out, and arrows land on a box
  edge. One arrow from the middle of a row, or a row hanging off one end of the chain, is N. (should fix)
- **D6** With the sound off, each icon reads as what it is meant to be. If you would have to guess (a buoy
  that looks like a joystick, an ambiguous "broadcast" glyph), it is N: use the standard glyph or add a
  one-word label. (should fix)
- **D7** Objects drawn "to scale" have true proportions (a car about 1.5 m tall, a door about 2 m, a person
  1.75 m). (should fix)

## E. Layout
- **E1** The composition is centred, or deliberately split into columns. No half of the frame stays empty
  for 5 s or more (lint `lopsided`). (should fix)
- **E2** A row of items that builds one at a time stays centred as it grows; it is not left-justified. (should fix)
- **E3** No text-only stretch of 3 s or more, and most frames have under five words that aren't math
  (lint `text-only`, `wordy`). (nit, or should fix if it lasts)

## F. Transitions and pacing
- **F1** No empty frame inside a scene for 0.8 s or more (lint `blank`). (nit)
- **F2** When the next scene starts from the same picture, it is a straight cut, not a fade-out and fade-in
  (lint `fade-flicker`). (should fix)
- **F3** When the narration changes topic, the picture changes within about 2 s. A frame identical to the
  previous scene's end for 10+ s is N. (should fix)

## G. Facts
- **G1** Every number on screen appears in the source paper or the narration. Write down where (page, table or
  figure) for each. (blocking if one doesn't)
- **G2** Anything illustrative rather than from data is tagged small and dim ("schematic"). (should fix)
- **G3** Terms and notation are the field's standard ones. (blocking if wrong)

## Output
For each scene:
```
<Scene>: PASS | FAIL
A1 Y | A2 N 221.0 (list not highlighted) | B1 Y | B2 Y | B3 N 211.2 | B4 N 221-227 | B5 Y | D1 Y | ... | G2 Y
- [t=..s] [blocking | should fix | nit] <problem> -> <concrete fix>
```
Then section C once for the whole video, with its table. A scene with any blocking N is FAIL.

## Who runs which part
Sections A, B, D, E and F are mechanical with the lint output and beat sheets, so a cheaper model can do
the per-scene pass. Sections C and G need the whole video and the paper in view: give those to the strongest
reviewer available, or do them yourself, at Gate 2 and on any re-review that changes shapes or numbers.
