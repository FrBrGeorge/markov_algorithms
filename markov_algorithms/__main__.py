#!/usr/bin/env python3
'''
'''
import sys
import argparse
from . import NAM

HELPURL = "https://cmcmsu.info/1course/alg.schema.nam.htm"
RUNLIMIT = 32768

def run(machine, word, debug, limit=RUNLIMIT):
    nw = len(str(limit-1))
    trace = [word]
    loop = machine(word)
    for word, rule, neword in loop:
        if debug:
            print(f"{word} [{rule}] {neword}")
            match input(f"{len(trace):>{nw}}> ")[:1]:
                case "q":
                    return neword
                case "b" if len(trace) > 2:
                    trace.pop()
                    trace.pop()
                    word, rule, neword = loop.send(trace[-1])
        trace.append(neword)
        if len(trace) >= limit:
            raise RuntimeError(f"Limit of {limit} steps is reached, still running")
    return neword

def main(prog, text, debug=None):
    try:
        machine = NAM(prog)
        print(run(machine, text, debug))
    except Exception as E:
        if debug:
            raise E
        else:
            print(f"Error: {E}", file=sys.stderr)
            exit(1)

def parseargs(*args):
    parser = argparse.ArgumentParser(description="Markov's Normal Algorithm runner",
                                     epilog=f"See {HELPURL} for syntax and examples")
    parser.add_argument("scheme", type=argparse.FileType("r"), help="Scheme (program)")
    parser.add_argument("--debug", "-d", action="store_true", help="Step-by-step execution")
    parser.add_argument("--verbose", "-v", default=0, action='count', help="Increase verbosity")
    parser.add_argument("--input", "-i", help="Input word")
    args = parser.parse_args(args or None)
    return args


if __name__ == "__main__":
    args = parseargs()
    prog = args.scheme.read()
    if args.scheme == sys.stdin:
        sys.stdin = open("/dev/tty", "r")
    word = args.input or input()
    main(prog, word, args.debug)
