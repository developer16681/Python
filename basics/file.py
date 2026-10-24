import os
from pathlib import Path

# Resolve path relative to repository root or text_files directory
base_dir = Path(__file__).resolve().parent.parent
data_path = base_dir / "text_files" / "data.txt"

if not data_path.exists():
    data_path = Path("data.txt")

with open(data_path, "r", encoding="utf-8") as my_file:
    data = my_file.read()

print("File Content:")
print(data)
