import argparse
import json
import copy
import sys

from basic_block import form_basic_blocks
from control_flow_graph import *
from visualizer import CFGVisualizer, DomTreeVisualizer
from to_ssa import cfg_to_ssa
from from_ssa import cfg_from_ssa

def main(args):
    
    file = args.filename
    if file is not None:
        with open(file, "r") as infile:
           prog = json.load(infile)
    else:
        trace = json.load(sys.stdin)
        lines = list()
        for line in sys.stdin:
            if not line.startswith('>'): continue
            line = line.replace(">", "")
            line = json.loads(line)
            lines.append(line)
        print(json.dumps(lines, indent=2))
    # read source file
    src = args.src
    # need to convert from bril to json first
    assert src is not None, "need to specify source file"
    

def main_old(args):
    # get options
    from_ssa = args.from_ssa
    to_ssa = args.to_ssa
    roundtrip = args.roundtrip
    if roundtrip:
        to_ssa = True
        from_ssa = True
    viz = args.visualize
    file = args.filename

    if file is not None:
        with open(file, "r") as infile:
           prog = json.load(infile)
    else: 
        prog = json.load(sys.stdin)

    for func in prog['functions']:
        blocks = form_basic_blocks(func['instrs'])
        blocks = [b for b in blocks if len(b) > 0]
        cfg_object = CFG(blocks)
        cfg = cfg_object.cfg
        if to_ssa:
            cfg_to_ssa(cfg)
        if from_ssa:
            cfg_from_ssa(cfg)
        if viz:        
            cfg_visualizer = CFGVisualizer(cfg, func['name'] + '-cfg')
            cfg_visualizer.show()

        # put updated instrs back to func
        func['instrs'] = cfg_object.gen_instrs()
    
    print(json.dumps(prog, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('-from-ssa', dest='from_ssa',
    #                     default=False, action='store_true',
    #                     help='Convert SSA-form program to original')
    # parser.add_argument('-to-ssa', dest='to_ssa',
    #                     default=False, action='store_true',
    #                     help='Convert program to SSA form')
    # parser.add_argument('-roundtrip', dest='roundtrip',
    #                     default=False, action='store_true',
    #                     help='Convert program to SSA form then convert it back')
    # parser.add_argument('-visualize', dest='visualize',
    #                     default=False, action='store_true',
    #                     help='visualize results')
    parser.add_argument('-f', dest='filename', 
                        action='store', type=str, help='json file')
    parser.add_argument("-src", dest='src',
                        action='store', type=str, help="bril source file")
    args = parser.parse_args()
    main(args)