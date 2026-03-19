from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA = Path("data/processed/soh_table.parquet")
OUT = Path("reports/soh_curves.png")

def main():
    df = pd.read_parquet(DATA)

    # Create a cycle index per battery (0,1,2,...) for plotting
    df = df.sort_values(["battery_id", "test_id", "uid"]).copy()
    df["cycle_idx"] = df.groupby("battery_id").cumcount()

    Path("reports").mkdir(parents=True, exist_ok=True)

    plt.figure()
    for bid, g in df.groupby("battery_id"):
        plt.plot(g["cycle_idx"], g["soh"], label=str(bid))
    plt.xlabel("Cycle index (discharge cycles)")
    plt.ylabel("State of Health (SoH)")
    plt.title("NASA batteries: SoH degradation curves")
    # Don’t show legend (34 lines gets messy); you can enable later if you want
    # plt.legend(ncol=2, fontsize=7)
    plt.tight_layout()
    plt.savefig(OUT, dpi=200)
    print("Saved:", OUT)

if __name__ == "__main__":
    main()