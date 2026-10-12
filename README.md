# manim-explainer-video

A Claude skill and reproducible toolchain for turning narration audio into a synced manim explainer video (3Blue1Brown / Marshall Bruner style, Tufte data-ink).

- `SKILL.md`: workflow and visual principles
- `references/creative-devices.md`: when and how to use 3D, morphs, icons, Blender renders
- `scripts/`: style kit, layout QA, transcription, rendering, review contact sheets, assembly
- `assets/icons/`: Phosphor fill icons (MIT) for recognizable objects, loaded with `icon()`
- `flake.nix`: pinned environment (manim, TeX, ffmpeg, faster-whisper, model weights, fonts)

```bash
nix develop                                   # interactive shell
nix run .#transcribe -- narration.mp3 out/    # timestamped transcript
nix develop .#blender                         # optional, for 3D renders
```
