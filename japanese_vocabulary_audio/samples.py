"""Writes a few words at several opus bitrates to tmp/samples/ to compare them with the mp3 by ear.

uv run python -m japanese_vocabulary_audio.samples
"""

import random
import shutil
from pathlib import Path

from dalang_dict import fetch

from japanese_vocabulary_audio.build import AUDIO, encode_opus

SAMPLES_DIR = Path("tmp") / "samples"
SAMPLE_COUNT = 12
SAMPLE_BITRATES = ["24k", "32k", "48k", "64k"]


def main() -> None:
    sources = random.Random(0).sample(sorted(fetch(AUDIO).glob("mp3/*.mp3")), SAMPLE_COUNT)
    shutil.rmtree(SAMPLES_DIR, ignore_errors=True)
    for source in sources:
        sample_dir = SAMPLES_DIR / source.stem
        sample_dir.mkdir(parents=True)
        shutil.copy(source, sample_dir / f"original{source.suffix}")
        for bitrate in SAMPLE_BITRATES:
            encode_opus(source, sample_dir / f"{bitrate}.opus", bitrate)
    print(f"Samples in {SAMPLES_DIR}")


if __name__ == "__main__":
    main()
