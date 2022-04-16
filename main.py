import argparse
import json
import copy
import sys

from basic_block import form_basic_blocks
from control_flow_graph import *
from visualizer import CFGVisualizer, DomTreeVisualizer
from to_ssa import cfg_to_ssa
from from_ssa import cfg_from_ssa

"""
This function binds the function call arguments and return value.
The goal is to output a straight-line program that can be executed
and return the correct value.
"""
def bind_func_args(prog, trace):
    pass

def main(args):
    with open(args.src, 'r') as f:
        prog = json.load(f)
    with open(args.trace, 'r') as f:
        trace = json.load(f)
    straight_prog = bind_func_args(prog, trace)
    print(json.dump(straight_prog, sys.stdout, indent=2))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-trace', dest='trace', 
                        action='store', type=str, help='json trace file')
    parser.add_argument("-src", dest='src',
                        action='store', type=str, help="bril source file")
    args = parser.parse_args()
    main(args)