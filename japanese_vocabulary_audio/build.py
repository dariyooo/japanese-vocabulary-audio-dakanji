from dalang_dict import Vendored, build_index, fetch, package_dictionary

GITHUB_REPO = "dariyooo/japanese-vocabulary-audio-dakanji"
ASSET = "japanese-vocabulary-audio-dakanji"
TITLE = "japanese-vocabulary-audio-dakanji"

# `used_for` and the version are listed in the release notes
SOURCE = Vendored("<name>", path="vendored_sources/<name>/<file>", version="<date retrieved>", used_for="")

INDEX_FIELDS = {
    "author": "",
    "url": f"https://github.com/{GITHUB_REPO}",
    "description": "Japanese vocabulary pronunciation audio from WaniKani for DaKanji",
    "attribution": "",
}


def build_banks(source: object) -> dict[str, list]:
    """Converts the source data to bank entries, e.g. {"kanji_bank": [...]}."""
    raise NotImplementedError


def main() -> None:
    banks = build_banks(fetch(SOURCE))
    index = build_index(TITLE, GITHUB_REPO, ASSET, **INDEX_FIELDS)
    package_dictionary(ASSET, index, banks)
