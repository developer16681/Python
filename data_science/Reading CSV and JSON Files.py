from pathlib import Path
import pandas as pd

# Resolve path to sample data file
base_dir = Path(__file__).resolve().parent.parent
csv_path = base_dir / "text_files" / "people.csv"

if not csv_path.exists():
    csv_path = Path("people.csv")

df = pd.read_csv(csv_path)
print(df)