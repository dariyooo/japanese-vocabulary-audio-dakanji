from pathlib import Path

from dalang_dict import fetch

from japanese_vocabulary_audio.build import AUDIO, INDEX_FIELDS, audio_files, encode_opus


def test_index_has_required_fields():
    for field in ("sourceLanguage", "author", "url", "description", "attribution"):
        assert field in INDEX_FIELDS


def test_audio_files_go_to_audios():
    paths = [Path("mp3/人【にん】.mp3"), Path("mp3/一【いち】.mp3")]
    assert audio_files(paths) == {"audios/一【いち】.mp3": paths[1], "audios/人【にん】.mp3": paths[0]}


def test_opus_encoding_is_reproducible(tmp_path):
    source = sorted(fetch(AUDIO).glob("mp3/*.mp3"))[0]
    encode_opus(source, tmp_path / "1.opus")
    encode_opus(source, tmp_path / "2.opus")
    assert (tmp_path / "1.opus").read_bytes() == (tmp_path / "2.opus").read_bytes()
