# Creative devices: when and how

Read this when the storyboard has a beat that 2D line art explains poorly. Everything here costs render time, tooling, or visual consistency, so each device has to earn its place.

## Contents
1. The budget and the test
2. Device catalog (what each is for, how to build it)
3. Asset sourcing and licensing
4. Keeping the style coherent

## 1. The budget and the test

- **Budget:** 1 to 3 signature moments per 10 minutes of video. Everything else is the restrained 2D house style.
- **Test before using a device:** would the explanation be weaker without it? "It looks cool" is not a reason. "The viewer can't see the third bounce in a 2D cross-section" is.
- **Placement:** the opening hook, the single hardest concept, and optionally the payoff. Never in the middle of a geometry derivation, where it would distract from the measurements.

## 2. Device catalog

### Morph between representations
For an idea that has two forms: a chirp graph becoming its spectrum, a time signal folding into its Fourier peaks, a ray diagram collapsing into an equation.
- Build: `ReplacementTransform`, or `TransformMatchingShapes` / `TransformMatchingTex` when the two forms share parts.
- Cheap, stays in the house style. This is the first creative tool to reach for.

### Camera moves in 2D
For a sense of scale, or for following an object.
- Build: `MovingCameraScene`. Zoom from a road overview into the van's rear bumper. Pan with the beam along its zigzag.
- Keep moves slow (2 to 4 s) and motivated by the narration.

### 3D geometry in manim
For an idea that is genuinely three-dimensional: corner reflectors, antenna patterns, wavefronts, rotations.
- Build: `ThreeDScene`. Use `Polygon` plates with `set_fill(opacity=0.25)`, a `VMobject` ray path, and `self.move_camera(phi=..., theta=...)` or `begin_ambient_camera_rotation(rate=0.1)`.
- Cairo handles a few dozen faces fine. Avoid dense surfaces.
- Return to an orthographic 2D view for anything with angles or lengths the viewer must read.

### 3D rendered objects (Blender)
For hero objects that need recognition, or a point-of-view shot. Example: "the van fills your windshield" shown from the driver's seat.
- Model: Kenney Car Kit (CC0, low-poly, consistent across vehicles), or Poly Haven (CC0).
- Render headless: `nix develop .#blender -c blender -b -P render.py`.
- Two looks that match the house style:
  - **Freestyle line art** exported as SVG (enable the Freestyle SVG Exporter add-on). Import with `SVGMobject`, recolor to INK, set strokes to about 2 px.
  - **Flat shading** in the palette (emission shader, 2 to 3 tones), transparent PNG sequence, imported with `ImageMobject`, one frame per manim frame.
- Use orthographic Blender cameras for top-down shots so they line up with the 2D geometry scenes. Perspective only for point-of-view shots.
- Moving parts (brake lights, signals, beams) stay as manim overlays anchored to the render's bounding box.

### Icon sets
For many small recognizable objects (sensors, phones, buildings).
- Sources: Tabler, Phosphor, Lucide (MIT), game-icons.net (CC BY, needs attribution).
- Import with `SVGMobject`. Use one family per video.
- Check at the real on-screen size, often 80 to 120 px at 1080p. Discard icons that turn to mush.

### Raster to vector
For a specific illustrated style that no icon set has.
- Source or generate the image outside the container, then vectorize with `vtracer` or `potrace` into SVG.
- Verify the license of the source image.

### Small multiples
For comparing conditions: with and without the reflector, at 1 to 4 m, in rain or clear.
- A grid of identical miniature plots sharing axes (Tufte). Often more creative and clearer than any animation.

## 3. Asset sourcing and licensing
- Prefer CC0 or MIT assets.
- CC BY requires an on-screen or description credit. Record it in the final summary.
- Never use branded or copyrighted characters, logos, or vehicle designs that identify a real make and model.

## 4. Keeping the style coherent
- Same palette, same stroke weight (2 px), same font across 2D, 3D and imported assets.
- A 3D shot should look like the same artist drew it: line art or flat palette shading, never photoreal next to Tufte plots.
- Cut, don't crossfade, between a 3D shot and a 2D scene, at a narration boundary.
- After rendering, view one contact sheet containing frames from both a 3D shot and a 2D scene together. If they look like two different videos, restyle the 3D.
