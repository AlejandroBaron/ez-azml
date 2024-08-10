import argparse
from pathlib import Path

# Argument parsing
parser = argparse.ArgumentParser(description="Print input")
parser.add_argument("--path", type=Path, default="outputs", help="output to read")
args = parser.parse_args()
path: Path = args.path
for file in path.glob("*.txt"):
    content = (path / file).read_text()
    print(content)
