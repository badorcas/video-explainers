#!/bin/bash
# One-time environment setup for manim + transcription in the claude.ai container.
set -e
apt-get update -q >/dev/null
apt-get install -y -q libpango1.0-dev pkg-config dvisvgm >/dev/null
pip install manim faster-whisper --break-system-packages -q
python3 -c "import manim, faster_whisper; print('manim', manim.__version__, 'ok')"
