"""Contact sheet of frames from a rendered scene, for visual review.
Usage: python3 grab.py <scene_output_name> t1 t2 ... -> /tmp/<name>.png (2 columns)"""
import sys, subprocess, glob
from PIL import Image
name, times = sys.argv[1], [float(x) for x in sys.argv[2:]]
f = sorted(glob.glob(f"media/videos/**/{name}.mp4", recursive=True))[0]
ims = []
for i, t in enumerate(times):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", f, "-frames:v", "1", f"/tmp/g{i}.png"])
    ims.append(Image.open(f"/tmp/g{i}.png"))
w, h = ims[0].size
o = Image.new("RGB", (w * 2, h * ((len(ims) + 1) // 2)))
for i, im in enumerate(ims):
    o.paste(im, ((i % 2) * w, (i // 2) * h))
o.save(f"/tmp/{name}.png"); print(f"/tmp/{name}.png")
