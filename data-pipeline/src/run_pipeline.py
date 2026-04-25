from pathlib import Path
import argparse
import subprocess
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-input", default="lga_input_real.csv")
    parser.add_argument("--prepared-output", default="lga_input_prepared.csv")
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

    run_step(
        [
            python,
            "src/prepare_lga_input.py",
            "--input",
            args.raw_input,
            "--output",
            args.prepared_output,
        ],
        cwd=project_root,
        label="Prepare input",
    )

    run_step(
        [
            python,
            "src/build_first_artifact.py",
            "--config",
            args.config,
            "--input",
            args.prepared_output,
        ],
        cwd=project_root,
        label="Build artifact",
    )

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
