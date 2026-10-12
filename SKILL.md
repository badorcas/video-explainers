---
name: manim-explainer-video
description: Turn narration audio (podcast, journal-club episode, lecture recording, voiceover) or a script into a fully synced explainer video built with manim, in a 3Blue1Brown / Marshall Bruner style with Edward Tufte's data-ink principles. Use this skill whenever the user uploads an mp3/wav/m4a and asks for a "video track", "visuals", "animation", "explainer", or "manim" for it, or asks for a manim animation of a technical concept (radar, signals, physics, controls, math, engineering papers), even if they don't say "manim" or "Tufte" explicitly.
---

# Manim explainer video from narration

The output is an MP4 whose picture is timed to the narration second by second. Quality bar: a viewer should understand the idea with the sound off and without reading much.

## Visual principles (the part that matters most)

These come from direct user feedback on a finished video. The equations, the clean dark style and the step-by-step builds were praised. Text-heavy frames, obvious labels and an invented diagram style were the complaints.

1. **Show, don't caption.** Never put on screen a sentence the narrator is already saying. If a frame needs words to make sense, redesign the frame. Allowed text: equations, axis names, a few key numbers (0.24 m, 70°), and a short label only where the picture is truly ambiguous. Target: most frames have under five words that aren't math.
2. **Trust the viewer.** Don't label things recognizable by shape. Draw a van as a van and a car as a car (`sedan()`, `van()` in style.py) instead of boxes saying "you" and "van". Show the viewer's car by position and camera framing, not a tag.
3. **Make the physical event visible.** Braking = brake lights plus the car visibly slowing and the gap shrinking. A turn signal = a rhythmic amber pulse at the front corner at about 1.5 Hz while the car drifts, not a dot blinking in place. "Harder braking" = a shorter stopping distance drawn on the road, not a bar labeled "hard".
4. **Use the field's standard notation.** Control or processing loops use a controls-style block diagram: forward path left to right, feedback path returning underneath (`block`, `chain`, `feedback` in style.py), animated by a signal pulse moving through the blocks. Pure schedules (do X, then Y, every 100 ms) use a timing diagram with lanes on a shared time axis. Use circuit symbols for circuits and ray diagrams for optics. Never invent a bespoke cyclical flowchart.
5. **Tufte data-ink.** Range-frame axes with no tips and no tick clutter. Label lines and peaks directly instead of using legends. Label only the values the narration uses. Never fabricate data: if the source only gives a worst-case error, draw a band, not invented points. If a plot is illustrative, tag it small and dim ("schematic").
6. **Equations are a strength.** Build them with Write, color terms to match the diagram (outgoing signal blue, echo orange), use underbraces for meaning ("out", "back"), and keep each equation on screen while it is being discussed.
7. **One idea per beat.** Each new element appears when the narration reaches it. Fade out what is no longer relevant instead of piling up.
8. **Consistent encoding.** One color means one thing for the whole video (TX blue = outgoing or ours, RX orange = echo, BRAKE red = braking, AMBER = signals, gray = context). Text set in a color only to match the thing it names.

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
Copy `scripts/style.py` next to the scene files. Every scene subclasses `TL`, sets `T0, T1` in absolute audio seconds, and uses `self.till(t)` (absolute time) before each beat, then `self.end()`. Spread scenes across 3 or 4 files so they can be fixed and re-rendered independently. End each scene with a fade-out about 1 s before T1.

### 5. Review loop at low quality (do not skip)
Render each scene with `manim -ql --disable_caching -o <Scene> file.py <Scene>` (about 10 s per minute of video). Make contact sheets with `python3 scripts/grab.py <Scene> t1 t2 t3 t4` and view them. Check for:
- clipped text at the frame edges, labels overlapping lines or each other
- rays and paths that do something geometrically wrong (retro-reflectors that don't retro-reflect)
- frames that are mostly words (apply principle 1)
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
