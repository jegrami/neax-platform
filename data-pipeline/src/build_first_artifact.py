import argparse
from pathlib import Path
import json
import pandas as pd


def minmax_0_100(series: pd.Series) -> pd.Series:
    min_v = series.min()
    max_v = series.max()
    if min_v == max_v:
        return pd.Series([50.0] * len(series), index=series.index)
    return ((series - min_v) / (max_v - min_v)) * 100.0


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


def write_artifact(df: pd.DataFrame, out_dir: Path, version: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"lga_priority_input__{version}.parquet"
    df.to_parquet(out_file, index=False)
    return out_file



def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    repo_root = project_root.parent

    args = parse_args()
    src = project_root / "data" / args.input
    config_path = project_root / "config" / args.config
    out_dir = repo_root / "data-artifacts" / "latest"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config = load_scoring_config(config_path)
    version = config["version"]
    demand_weights = config["demand_weights"]

    df = load_input_data(src)
    if df.empty:
        raise ValueError(f"Input file has 0 rows {src}")
    
    scored = compute_demand_score(df, demand_weights)
    scored["artifact_version"] = version

    out_file = write_artifact(scored, out_dir, version)
    print(f"Wrote {out_file} with {len(scored)} rows")



if __name__ == "__main__":
    main()
