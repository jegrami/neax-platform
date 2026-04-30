"""Run the current normalize -> score pipeline for real LGA indicator inputs."""

from pathlib import Path
import argparse
import subprocess
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="lga_input_real.csv")
    parser.add_argument("--normalized-output", default="lga_input_prepared.csv")
    parser.add_argument("--sources-manifest", required=True)
    parser.add_argument("--config", default="scoring.v1.json")
    return parser.parse_args()


def run_step(cmd: list[str], cwd: Path, label: str) -> None:
    print(f"\n==> {label}")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        raise SystemExit(f"Step failed: {label}")


def main() -> None:
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]  # data-pipeline/

    python = sys.executable

    normalize_cmd = [
        python,
        "src/normalize_public_lga_indicator_csv.py",
        "--input",
        args.input,
        "--output",
        args.normalized_output,
        "--sources-manifest",
        args.sources_manifest,
    ]

    run_step(
        normalize_cmd,
        cwd=project_root,
        label="Normalize public LGA indicator CSV",
    )

    run_step(
        [
            python,
            "src/score_lga_input.py",
            "--config",
            args.config,
            "--input",
            args.normalized_output,
        ],
        cwd=project_root,
        label="Score LGA input",
    )

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
