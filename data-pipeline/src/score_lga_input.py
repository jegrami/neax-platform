"""Compute the first scoring artifact from a normalized LGA input CSV."""

import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import json

import pandas as pd


def minmax_0_100(series: pd.Series) -> pd.Series:
    min_v = series.min()
    max_v = series.max()
    if min_v == max_v:
        return pd.Series([50.0] * len(series), index=series.index)
    return ((series - min_v) / (max_v - min_v)) * 100.0


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def load_scoring_config(config_path: Path) -> dict:
    with config_path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)

    demand_weights = cfg["demand_weights"]
    weights_sum = sum(demand_weights.values())
    if abs(weights_sum - 1.0) > 1e-9:
        raise ValueError(f"demand_weights must sum to 1.0, got {weights_sum}")

    return cfg


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="scoring.v1.json",
        help="Scoring config filename inside data-pipeline/config",
    )
    parser.add_argument(
        "--input",
        default="lga_input_prepared.csv",
        help="Input CSV filename inside data-pipeline/data",
    )
    parser.add_argument(
        "--sources-manifest",
        required=True,
        help="Sources manifest filename inside data-pipeline/data",
    )
    return parser.parse_args()


def load_input_data(src: Path) -> pd.DataFrame:
    return pd.read_csv(src)


def compute_demand_score(df: pd.DataFrame, demand_weights: dict) -> pd.DataFrame:
    pop_norm = minmax_0_100(df["population_density"])
    health_norm = minmax_0_100(df["health_facilities"])

    out = df.copy()
    out["demand_score"] = (
        demand_weights["population_density"] * pop_norm
        + demand_weights["health_facilities"] * health_norm
    )
    return out


def build_run_stamp(now: datetime | None = None) -> str:
    moment = now or datetime.now(timezone.utc)
    return moment.strftime("%Y%m%dT%H%M%SZ")


def write_artifact(df: pd.DataFrame, out_dir: Path, version: str, run_stamp: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"lga_priority_input__{version}__{run_stamp}.parquet"
    df.to_parquet(out_file, index=False)
    return out_file


def write_data_manifest(
    out_dir: Path,
    version: str,
    run_stamp: str,
    out_file: Path,
    row_count: int,
    config_path: Path,
    input_path: Path,
    sources_manifest_path: Path,
) -> Path:
    manifest_file = out_dir / f"data_manifest__{version}__{run_stamp}.json"
    manifest = {
        "artifact_version": version,
        "artifact_run_stamp": run_stamp,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "artifact_file": str(out_file),
        "artifact_sha256": sha256_file(out_file),
        "row_count": row_count,
        "scoring_config_file": str(config_path),
        "scoring_config_sha256": sha256_file(config_path),
        "normalized_input_file": str(input_path),
        "normalized_input_sha256": sha256_file(input_path),
        "sources_manifest_file": str(sources_manifest_path),
        "sources_manifest_sha256": sha256_file(sources_manifest_path),
    }
    manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_file


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    repo_root = project_root.parent

    args = parse_args()
    src = project_root / "data" / args.input
    config_path = project_root / "config" / args.config
    sources_manifest_path = project_root / "data" / args.sources_manifest
    out_dir = repo_root / "data-artifacts" / "latest"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    if not src.exists():
        raise FileNotFoundError(f"Input file not found: {src}")
    if not sources_manifest_path.exists():
        raise FileNotFoundError(f"Sources manifest file not found: {sources_manifest_path}")

    config = load_scoring_config(config_path)
    version = config["version"]
    demand_weights = config["demand_weights"]

    df = load_input_data(src)
    if df.empty:
        raise ValueError(f"Input file has 0 rows {src}")

    run_stamp = build_run_stamp()
    scored = compute_demand_score(df, demand_weights)
    scored["artifact_version"] = version
    scored["artifact_run_stamp"] = run_stamp

    out_file = write_artifact(scored, out_dir, version, run_stamp)
    manifest_file = write_data_manifest(
        out_dir=out_dir,
        version=version,
        run_stamp=run_stamp,
        out_file=out_file,
        row_count=len(scored),
        config_path=config_path,
        input_path=src,
        sources_manifest_path=sources_manifest_path,
    )

    print(f"Wrote {out_file} with {len(scored)} rows")
    print(f"Wrote data manifest: {manifest_file}")


if __name__ == "__main__":
    main()
