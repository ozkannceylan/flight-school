"""Phase 5 tools: studypack concatenates; screencast emits beats."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str):
    path = ROOT / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"flightlab_tools_{name}", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


studypack = _load("studypack")
screencast = _load("screencast")


def test_studypack_writes_five_phases(tmp_path, monkeypatch):
    monkeypatch.setattr(studypack, "BUILD", tmp_path)
    for n in range(1, 6):
        dest = studypack.pack_phase(n)
        text = dest.read_text(encoding="utf-8")
        assert dest.name == f"studypack_phase{n}.md"
        assert f"Phase {n}" in text
        assert "Lecture L" in text
        assert "Lab README" in text


def test_studypack_phase5_includes_lab23_and_l24(tmp_path, monkeypatch):
    monkeypatch.setattr(studypack, "BUILD", tmp_path)
    text = studypack.pack_phase(5).read_text(encoding="utf-8")
    assert "lab23_red_team" in text
    assert "L24" in text


def test_screencast_beats_have_timing(tmp_path, monkeypatch):
    monkeypatch.setattr(screencast, "BUILD", tmp_path)
    dest = screencast.write_script("17")
    text = dest.read_text(encoding="utf-8")
    assert dest.name == "lab17_script.md"
    assert "| t | s | beat | cue |" in text
    assert "Why now?" in text
    assert "Total" in text
