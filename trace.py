import argparse
import json
import sys

def main(args):
    file = args.filename
    if file is not None:
        with open(file, "r") as infile:
           prog = json.load(infile)
    else:
        lines = list()
        for line in sys.stdin:
            if not line.startswith('>'): continue
            line = line.replace(">", "")
            line = json.loads(line)
            lines.append(line)
        prog = {'functions' : [{"name" : "main", "instrs" : lines}]}
        print(json.dumps(prog, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='filename', 
                        action='store', type=str, help='json file')
    args = parser.parse_args()
    main(args)