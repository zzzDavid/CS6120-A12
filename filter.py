import sys
import json

if __name__ == "__main__":
    lines = ""
    for line in sys.stdin:
        if not line.startswith(">"):
            lines += line
    print(lines)