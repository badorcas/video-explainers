---
name: manim-explainer-video
description: Turn narration audio (podcast, journal-club episode, lecture recording, voiceover) or a script into a fully synced explainer video built with manim, in a 3Blue1Brown / Marshall Bruner style with Edward Tufte's data-ink principles. Use this skill whenever the user uploads an mp3/wav/m4a and asks for a "video track", "visuals", "animation", "explainer", or "manim" for it, or asks for a manim animation of a technical concept (radar, signals, physics, controls, math, engineering papers), even if they don't say "manim" or "Tufte" explicitly.
---

# Manim explainer video from narration

The output is an MP4 whose picture is timed to the narration second by second. Quality bar: a viewer should understand the idea with the sound off and without reading much.

## Visual principles (the part that matters most)

These come from direct user feedback on a finished video. The equations, the clean dark style and the step-by-step builds were praised. Text-heavy frames, obvious labels and an invented diagram style were the complaints.

1. **Show, don't caption.** Never put on screen a sentence the narrator is already saying. If a frame needs words to make sense, redesign the frame. Allowed text: equations, axis names, a few key numbers (0.24 m, 70°), and a short label only where the picture is truly ambiguous. Target: most frames have under five words that aren't math.
2. **Trust the viewer, but label what the lesson names.** Don't label everyday things recognizable by shape. Draw a van as a van and a car as a car (`sedan()`, `van()` in style.py) instead of boxes saying "you" and "van". Show the viewer's car by position and camera framing, not a tag. The exception is technical structures whose names are the point: anatomy (retina, optic nerve, LGN, occipital cortex), circuit components, named parts of an instrument. Label those directly with a thin leader line, introduce each label as the narration names it, and use the field's standard term. An unlabeled structure the viewer is supposed to learn is a missed lesson, not restraint.
3. **Make the physical event visible.** Braking = brake lights plus the car visibly slowing and the gap shrinking. A turn signal = a rhythmic amber pulse at the front corner at about 1.5 Hz while the car drifts, not a dot blinking in place. "Harder braking" = a shorter stopping distance drawn on the road, not a bar labeled "hard".
4. **Use the field's standard notation.** Control or processing loops use a controls-style block diagram: forward path left to right, feedback path returning underneath (`block`, `chain`, `feedback` in style.py), animated by a signal pulse moving through the blocks. Pure schedules (do X, then Y, every 100 ms) use a timing diagram with lanes on a shared time axis. Use circuit symbols for circuits and ray diagrams for optics. Never invent a bespoke cyclical flowchart.
5. **Tufte data-ink.** Range-frame axes with no tips and no tick clutter. Label lines and peaks directly instead of using legends. Label only the values the narration uses. Never fabricate data: if the source only gives a worst-case error, draw a band, not invented points. If a plot is illustrative, tag it small and dim ("schematic").
6. **Equations are a strength.** Build them with Write, color terms to match the diagram (outgoing signal blue, echo orange), use underbraces for meaning ("out", "back"), and keep each equation on screen while it is being discussed.
7. **One idea per beat.** Each new element appears when the narration reaches it. Fade out what is no longer relevant instead of piling up.
8. **Draw recognizable things accurately or not at all.** A wobbly freehand outline of an eye or brain distracts more than it helps. Anatomy, organs and instruments must come from a real reference: trace or import an accurate outline (see "Anatomy and biology" in `references/creative-devices.md`), keep correct proportions and relative positions, and prefer a clean schematic view (a standard sagittal or axial section) over an inaccurate realistic one. If an accurate outline isn't available, use a recognized schematic convention for the field instead of improvising.
9. **Consistent encoding.** One color means one thing for the whole video (TX blue = outgoing or ours, RX orange = echo, BRAKE red = braking, AMBER = signals, gray = context). Text set in a color only to match the thing it names.

## Hard rules from review (each one came from a user complaint)

These are not style preferences. A video that breaks one is not done.

- **Kerning: always make text with `T()`, never `Text()` directly.** At the small sizes manim lays text out at, Pango snaps each glyph advance to a whole pixel, which produces "Ar ray", "et  al", "Workfl ow". `T()` lays out at 8x and scales down. The same goes for any helper that builds text.
- **Real objects come from the icon set, never hand-plotted polygons.** A plane drawn from a list of coordinates came out angular and wrong. Use `icon("airplane", h)` (and `car`, `truck`, `user`, `hard-drives`, `cpu`, `lightning`, `clock`, `file-text`, `thermometer`, `currency-dollar`, ... see `assets/icons/`, Phosphor fill set, MIT). Each is drawn as an off-white outline with an opaque dark fill. If an object isn't in the set, fetch the Phosphor fill SVG from `cdn.jsdelivr.net/npm/@phosphor-icons/core@2.1.1/assets/fill/<name>-fill.svg` into `assets/icons/`. If you truly must draw one, build it from smooth curves (arcs, rounded rectangles, `set_points_smoothly`), then look at a full-size still before using it. Some icon sets (Tabler) include an invisible bounding-box path that renders as a square: delete it. Abstract diagram parts (nodes, bars, boxes, servers-as-rack-units) stay as primitives.
- **No text on top of graphics.** A label never sits on a line, an arrow, another label, or the edge of a filled shape. Move it into clear space. If it must sit over something, back it with `plate(label)` (opaque background).
- **Layers must hide what is under them.** When one graphic sits on another, the top one gets an opaque fill (`fill_opacity=1`) so the lines underneath don't show through; or fade/clear the bottom layer first. Translucent fills over lines, outline-only shapes with edges running through them, and arrows drawn across boxes all read as a tangle. Draw order matters: edges first, then nodes on top.
- **These are checked automatically.** `scripts/qa.py` runs at every `self.till()` when `QA=1` (`scripts/lq.sh` sets it) and writes `qa/<Scene>.txt`. Every line in it must be fixed before the final render, or deliberately waived with `mob.qa_ok = True` for a reason you can state (for example, a shaded range band laid over its own scale line).

Style defaults are in `scripts/style.py`: near-black background, off-white ink, Caladea serif, thin strokes. If the user prefers a light Tufte "paper" look, swap BG/INK/MUTE/FAINT there; everything else follows.

## Creativity, used sparingly

The restrained 2D house style is the default for most of the runtime. On top of it, plan **1 to 3 signature moments per 10 minutes** where a more inventive device explains something 2D line art can't. Put them at the opening hook, the single hardest concept, and optionally the payoff.

Before using a device, ask: would the explanation be weaker without it? Use it only if the answer is clearly yes. Examples of good uses:
- a morph from a chirp graph into its spectrum (two forms of one idea),
- an orbiting 3D view of a corner reflector bouncing a ray off three faces (the third bounce is invisible in 2D),
- a driver's-eye 3D shot where the van fills the windshield (the occlusion explains itself),
- small multiples comparing test conditions instead of a sequence of slides.

Keep geometry with readable angles and lengths in orthographic 2D, and keep every creative shot in the same palette and stroke weight so the video looks like one artist made it. Read `references/creative-devices.md` for the device catalog (morphs, camera moves, manim 3D, Blender line-art renders, icon sets, raster-to-vector, small multiples), asset sources and licenses, and how to keep 3D shots stylistically coherent.

There is no image generator in the claude.ai container. For richer objects, prefer CC0 3D models rendered as line art, an icon family imported via `SVGMobject`, or parametric primitives. Moving parts (lights, signals, beams) stay as manim overlays.

## Workflow

### 1. Environment (once per container)
Preferred: the bundled Nix flake (`flake.nix` + `flake.lock`). It pins nixpkgs, manim, faster-whisper, ffmpeg, a minimal TeX with dvisvgm, the Caladea font (through a private fontconfig), and the Whisper weights (pinned to a Hugging Face commit and hash-checked). Everything comes from the binary cache, about 4 min on a cold container.

Installing Nix in the claude.ai container (running as root, no daemon):
```bash
mkdir -p /etc/nix && printf 'build-users-group =\nexperimental-features = nix-command flakes\nsandbox = false\n' > /etc/nix/nix.conf
curl -sSfL https://nixos.org/nix/install -o /tmp/nix-install.sh && USER=root sh /tmp/nix-install.sh --no-daemon --yes
export PATH=/root/.nix-profile/bin:$PATH      # the profile script needs bash; setting PATH is enough
```
Copy the skill folder somewhere writable and run it as a git repo (flakes only see tracked files: `git init && git add -A`). Then either:
- `nix develop -c bash -c "cd <work> && manim ..."` for interactive steps, or
- `nix run <skill>#transcribe -- <audio> <outdir>`, `#render`, `#assemble`, `#grab` (same arguments as the scripts below).

The nixpkgs input is a commit tarball rather than `github:` because unauthenticated GitHub API calls from the container hit rate limits.

Fallback without Nix: `bash scripts/setup.sh` (apt pango headers and dvisvgm, then pip install manim and faster-whisper; versions float).

Known pitfalls either way:
- Type1 fonts (such as Bitstream Charter) silently fall back to sans in pango; use Caladea or another TTF/OTF and confirm with a test frame.
- `-qh` means 1080p **60**; always pass `--frame_rate 30`. That halves render time.
- Every tool call is capped at 300 s. Run transcription, rendering and assembly detached (`setsid nohup ... >/dev/null 2>&1 </dev/null &`) and poll a progress file in later calls.
- Never `pkill -f manim` from a shell command that itself contains "manim"; it kills the calling shell. Kill by PID.

### 2. Transcript with timestamps
`python3 scripts/transcribe.py <audio> <outdir>` (about 4 min per 13 min of audio). Read the whole transcript. Whisper mishears proper nouns (it heard "Dremel Club" for "Journal Club"), so cross-check names against later mentions, and leave uncertain names off screen.

### 3. Storyboard
Split the transcript into scenes of roughly 30 to 90 s at topic boundaries. For each scene write down its absolute start/end (T0/T1) and a beat list: timestamp → what appears or moves. For each beat, ask "what would this look like with no words?" before reaching for text. Then mark the 1 to 3 beats that get a signature device, and plan everything else in the house style.

### 4. Write scenes
Copy `scripts/style.py`, `scripts/qa.py` and `scripts/lq.sh` next to the scene files (set `ICON_DIR` to `assets/icons`, or copy that folder as `icons/`). Every scene subclasses `TL`, sets `T0, T1` in absolute audio seconds, and uses `self.till(t)` (absolute time) before each beat, then `self.end()`. Spread scenes across 3 or 4 files so they can be fixed and re-rendered independently. End each scene with a fade-out about 1 s before T1.

### 5. Review loop at low quality (do not skip)
Render with `bash lq.sh <file> "S01 S02 ..."` (about 10 s per minute of video). It runs the layout QA and writes the issue count per scene to `lq_<file>.txt`; read `qa/<Scene>.txt` and clear every line. Then make contact sheets with `python3 scripts/grab.py <Scene> t1 t2 t3 t4` and view them: the QA catches geometry, not meaning. Check for:
- clipped text at the frame edges, labels overlapping lines or each other, lines showing through a layer on top (the QA flags these; confirm by eye)
- letter spacing that looks uneven (means something bypassed `T()`)
- hand-drawn objects that look angular or off-model (replace with `icon()`)
- rays and paths that do something geometrically wrong (retro-reflectors that don't retro-reflect)
- frames that are mostly words (apply principle 1)
- technical structures the narration names but the frame leaves unlabeled (principle 2)
- anatomy or objects that look hand-wavy, out of proportion, or anatomically wrong (principle 8): compare against the reference image side by side
- empty halves of the frame, lopsided layouts
- color meaning drift across scenes

Fix, re-render, re-check. Do this before the slow full render.

### 6. Final render and assembly
- `setsid nohup bash scripts/render_all.sh "part1:S01 part1:S02 ..." ...&` takes about 1 min of render time per minute of video at 1080p30. Poll `progress.txt` and `fails.txt`.
- `python3 scripts/assemble.py <audio> /mnt/user-data/outputs/<name>.mp4 part1:S01 ...` pads or trims each segment to its exact slot (so small timing drift never desyncs the audio), concatenates, and muxes the narration. It's resumable after a timeout.
- Spot-check about 10 frames across the final file against the transcript times, then call `present_files`.

## Reporting back
Keep the summary short:
- what the video covers
- any transcript corrections made
- anything shown as schematic rather than sourced data
- the one or two choices the user may want to flip (dark vs. light, pacing)
