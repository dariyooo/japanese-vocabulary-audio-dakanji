"""Builds the WaniKani vocabulary audio dictionaries, one per audio format: mp3, ogg and our own opus."""

import shutil
import subprocess
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import imageio_ffmpeg
from dalang_dict import Vendored, build_index, fetch, package_dictionary

GITHUB_REPO = "dariyooo/japanese-vocabulary-audio-dakanji"
ASSET = "japanese-vocabulary-audio-dakanji"
TITLE = "WaniKani Vocabulary Audio"

# `used_for` and the version are listed in the release notes
AUDIO = Vendored(
    "japanese-vocabulary-pronunciation-audio",
    path="vendored_sources/japanese-vocabulary-pronunciation-audio",
    version="9725e0e",
    used_for="mp3 and ogg audio, the opus audio is encoded from the mp3 audio",
)

# Our own Opus build, encoded from the mp3 build: upstream's ogg build lacks 894 of the mp3 build's 6,355 words.
OPUS_BITRATE = "32k"
OPUS_DIR = Path("tmp") / "opus"

INDEX_FIELDS = {
    "sourceLanguage": "ja",
    "author": "WaniKani (Tofugu)",
    "url": "https://github.com/tofugu/japanese-vocabulary-pronunciation-audio",
    "description": "Mainly old vocabulary pronunciation audio from WaniKani, which has since replaced it with newer "
    "recordings. A mix of two voices: a male native speaker (Tokyo accent, professional voice actor, professionally "
    "recorded) and a female native speaker (Kansai accent, amateur voice actor, amateur recorded).",
    "attribution": "Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) Tofugu Inc. and WaniKani "
    "[https://github.com/tofugu/japanese-vocabulary-pronunciation-audio/blob/master/LICENSE]",
}


def encode_opus(source: Path, target: Path, bitrate: str = OPUS_BITRATE) -> None:
    # -vn drops the cover art some mp3s embed, -map_metadata -1 their tags,
    # bitexact keeps ffmpeg from writing a random stream serial so rebuilds are identical.
    subprocess.run(
        [
            imageio_ffmpeg.get_ffmpeg_exe(), "-nostdin", "-loglevel", "error", "-y",
            "-i", str(source),
            "-vn", "-map_metadata", "-1", "-fflags", "+bitexact", "-flags:a", "+bitexact",
            "-ac", "1", "-c:a", "libopus", "-b:a", bitrate,
            str(target),
        ],
        check=True,
    )  # fmt: skip


def encode_opus_files(sources: list[Path], target_dir: Path) -> list[Path]:
    shutil.rmtree(target_dir, ignore_errors=True)
    target_dir.mkdir(parents=True)
    targets = [target_dir / f"{source.stem}.opus" for source in sources]
    with ThreadPoolExecutor() as pool:
        list(pool.map(encode_opus, sources, targets))
    return targets


def audio_files(paths: Iterable[Path]) -> dict[str, Path]:
    """Maps the audio files to their place in the dictionary, `audios/{word}【{reading}】.{ext}`."""
    return {f"audios/{path.name}": path for path in sorted(paths)}


def main() -> None:
    audio_dir = fetch(AUDIO)
    mp3_files = sorted(audio_dir.glob("mp3/*.mp3"))
    formats = {
        "mp3": mp3_files,
        "ogg": sorted(audio_dir.glob("ogg/*.ogg")),
        "opus": encode_opus_files(mp3_files, OPUS_DIR),
    }
    for audio_format, paths in formats.items():
        package_name = f"{ASSET}-{audio_format}"
        index = build_index(f"{TITLE} ({audio_format})", GITHUB_REPO, package_name, **INDEX_FIELDS)
        package_dictionary(package_name, index, {}, extra_files=audio_files(paths), format="dakanji-audio")
