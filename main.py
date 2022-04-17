import argparse
import json
import copy
import sys

"""
This function binds the function call arguments and return value.
The goal is to output a straight-line program that can be executed
and return the correct value.
"""
def bind_func_args(prog, trace):
    # copy the main functions's input argument to trace
    for func in prog['functions']:
        if func['name'] == 'main':
            trace['functions'][0]['args'] = func['args']
            main_labels = [instr["label"] for instr in func["instrs"] if "label" in instr]
    # we need to be careful not to modify instructions
    # while iterating over them
    ret_stack = list()
    new_instrs = list()
    # add speculate instruction
    new_instrs.append({"op" : "speculate"})
    for instr in trace['functions'][0]['instrs']:
        if instr['op'] == 'call':
            # find the function that is being called
            for func in prog['functions']:
                if func['name'] == instr['funcs'][0]:
                    # copy the call's input arguments to the function
                    for i in range(len(func['args'])):
                        src = [instr['args'][i]]
                        dst = func['args'][i]['name']
                        typ = func['args'][i]['type']
                        id_instr = {
                            "op": "id",
                            "args" : src,
                            "dest": dst,
                            "type": typ
                        }
                        new_instrs.append(id_instr)
                    
                    # copy the function's return value to the call
                    if 'dest' in instr:
                        ret_stack.append({"type" : instr['type'], "dest" : instr['dest']})
        elif instr['op'] == 'ret':
            # look into the return stack for the return value
            if len(ret_stack) > 0:
                ret_val = ret_stack.pop()
                id_instr = {
                    "op": "id",
                    "args" : instr['args'],
                    "dest" : ret_val['dest'],
                    "type" : ret_val['type']
                }
                new_instrs.append(id_instr)
        elif instr['op'] == 'br':
            # turn br to guard
            dest = instr['labels'][1]
            cond = instr['args']
            guard_instr = {
                "op": "guard",
                "args" : cond,
                "labels" : [dest]
            }
            if dest in main_labels:
                new_instrs.append(guard_instr)
        else:
            if instr['op'] not in ['jmp']:
                new_instrs.append(instr)
    # add commit instruction
    new_instrs.append({"op" : "commit"})
    trace['functions'][0]['instrs'] = new_instrs
    return trace
        

def insert_trace(prog, trace):
    new_instrs = list()
    new_instrs.extend(trace['functions'][0]['instrs'])
    # add a ret instr for the main function
    if new_instrs[-1]['op'] != 'ret':
        new_instrs.append({"op" : "ret"})
    new_instrs.append({"label" : "main_entry"})

    for func in prog['functions']:
        if func['name'] == 'main':
            new_instrs.extend(func['instrs'])
            # replace the main function's instructions
            func['instrs'] = new_instrs
            break
    return prog

def main(args):
    with open(args.src, 'r') as f:
        prog = json.load(f)
    with open(args.trace, 'r') as f:
        trace = json.load(f)
    straight_prog = bind_func_args(prog, trace)
    new_prog = insert_trace(prog, straight_prog)
    print(json.dumps(new_prog, indent=2))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-trace', dest='trace', 
                        action='store', type=str, help='json trace file')
    parser.add_argument("-src", dest='src',
                        action='store', type=str, help="bril source file")
    args = parser.parse_args()
    main(args)