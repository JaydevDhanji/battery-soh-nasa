from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW = PROJECT_ROOT / "data" / "raw" / "Battery_Data_Cleaned.csv"
OUT = PROJECT_ROOT / "data" / "processed" / "soh_table.parquet"

N_BASELINE = 5  # use first 5 discharge cycles for baseline

def baseline_capacity(group: pd.DataFrame) -> float:
    g = group.sort_values(["test_id", "uid"]).copy()
    first_n = g["Capacity"].head(N_BASELINE)
    # robust baseline (median avoids one weird small value)
    return float(first_n.median())

def main():
    df = pd.read_csv(RAW)
    df.columns = [c.strip() for c in df.columns]
    print("Loaded rows:", len(df))

    # discharge only
    df = df[df["type"] == -1].copy()
    print("After discharge filter:", len(df))

    # valid capacity only
    df = df[df["Capacity"] > 0].copy()
    print("After Capacity>0 filter:", len(df))

    df = df.sort_values(["battery_id", "test_id", "uid"])

    # compute robust baseline capacity per battery
    base = df.groupby("battery_id", group_keys=False).apply(baseline_capacity)
    base.name = "baseline_capacity"
    df = df.merge(base, on="battery_id", how="left")

    # drop batteries where baseline is still too small (safety)
    df = df[df["baseline_capacity"] > 0.5].copy()  # adjust if needed
    df["soh"] = df["Capacity"] / df["baseline_capacity"]
    df["soh"] = df["soh"].clip(0.6, 1.15)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False)

    print("Saved:", OUT)
    print("Rows saved:", len(df))
    print("Batteries:", df["battery_id"].nunique())
    print("SoH min/max:", df["soh"].min(), df["soh"].max())

if __name__ == "__main__":
    main()