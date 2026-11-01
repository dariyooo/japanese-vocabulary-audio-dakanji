# japanese-vocabulary-audio-dakanji

Japanese vocabulary pronunciation audio from [WaniKani](https://www.wanikani.com) for DaKanji.

The audio of 6,355 words, mainly old WaniKani recordings that WaniKani has since replaced, published by
[Tofugu](https://github.com/tofugu/japanese-vocabulary-pronunciation-audio).
It is a mix of two voices: a male native speaker (Tokyo accent, professional voice actor, professionally recorded)
and a female native speaker (Kansai accent, amateur voice actor, amateur recorded).

It is a DaKanji audio dictionary (`dakanji-audio`), each file is named `{word}【{reading}】.{ext}`,
which DaKanji reads the word and reading from.

## Assets

| Asset | Words | Size |
|---|---|---|
| `japanese-vocabulary-audio-dakanji-mp3.zip` | 6,355 | 147 MB |
| `japanese-vocabulary-audio-dakanji-ogg.zip` | 5,461 | 96 MB |
| `japanese-vocabulary-audio-dakanji-opus.zip` | 6,355 | 21 MB |

The opus dictionary is our own, encoded from the mp3 audio at 32 kbit/s mono, as upstream's ogg audio lacks 894 words.
It is the recommended one.

## Sources

The audio is vendored in `vendored_sources/japanese-vocabulary-pronunciation-audio/` (see `vendored_sources/README.md`
for the exact version).

## Installation

Make sure [uv](https://github.com/astral-sh/uv) is installed on your system and run

``` bash
uv sync
```

## Usage

``` bash
uv run build.py
```

This creates the three dictionaries in `out/` (`.zip`, `.index.json` and `.manifest.json` each).
The uncompressed dictionaries are kept in `tmp/` for inspection.

To compare opus bitrates by ear, `uv run python -m japanese_vocabulary_audio.samples` writes a few words at several
bitrates to `tmp/samples/`.

## Development

``` bash
uv run ruff check .          # lint
uv run ruff format .         # format
uv run pyright               # type check
uv run pytest                # tests
```

The repo follows the [DaLang dictionary repo standard](https://github.com/dariyooo/dalang-dict-utils/blob/main/docs/repo-standard.md),
update the shared setup with `uvx copier update --trust`.

## Release

Push a tag with today's date:

``` bash
git tag 2026-11-01 && git push origin 2026-11-01
```

The *Release* workflow runs the checks, builds the dictionaries with the tag as revision and publishes them as the GitHub release of the tag.
To redo a release, push the tag again with `git tag -f 2026-11-01 && git push -f origin 2026-11-01`.
Installed dictionaries pick up new releases through "Check for updates".

## License

Audio by [Tofugu](https://www.tofugu.com) and [WaniKani](https://www.wanikani.com),
[CC BY-SA 4.0](https://github.com/tofugu/japanese-vocabulary-pronunciation-audio/blob/master/LICENSE).
