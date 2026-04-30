import argparse
from pathlib import Path

import pytest

import run_lga_scoring_pipeline as rp


def test_run_step_raises_on_nonzero(monkeypatch):
    class Result:
        returncode = 1

    monkeypatch.setattr(rp.subprocess, "run", lambda *args, **kwargs: Result())

    with pytest.raises(SystemExit, match="Step failed"):
        rp.run_step(["python", "x.py"], Path("."), "Bad Step")


def test_main_invokes_prepare_then_build(monkeypatch):
    captured = []

    monkeypatch.setattr(
        rp,
        "parse_args",
        lambda: argparse.Namespace(
            input="input.csv",
            normalized_output="prepared.csv",
            sources_manifest="sources.json",
            config="scoring.v1.json",
        ),
    )

    def fake_run_step(cmd, cwd, label):
        captured.append((cmd, cwd, label))

    monkeypatch.setattr(rp, "run_step", fake_run_step)

    rp.main()

    assert len(captured) == 2
    assert captured[0][2] == "Normalize public LGA indicator CSV"
    assert captured[1][2] == "Score LGA input"

    prepare_cmd = captured[0][0]
    build_cmd = captured[1][0]

    assert "src/normalize_public_lga_indicator_csv.py" in prepare_cmd
    assert "--sources-manifest" in prepare_cmd
    assert "src/score_lga_input.py" in build_cmd
    assert "--config" in build_cmd
