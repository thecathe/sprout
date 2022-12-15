#!/usr/bin/env python

import os
import sys
import json

args = []
features = {}
default_feature_path = "featured.json"

valid_feature_fields = ["enabled","commands"]

flags = {
    "-p": True, # status print
    "-db": False, # debug printing
    "-vb": False, # verbose printing
    "-sp": False, # special, overrides all other printing
}
valid_flags = flags.keys()

valid_args = ["help","demo", "demoargs"]

class log_mgr():
    
    do_print = True
    do_verbose = False
    do_special = False
    
    def __init__(self, _print, _verbose, _special):
        self.do_print = _print
        self.do_verbose = _print and _verbose
        self.do_special = _special

    def log(self, msg):
        if self.do_print:
            print(msg)
            
    def vb(self, msg):
        if self.do_verbose:
            print(msg)
            
    def sp(self, msg):
        if self.do_special:
            print(msg)
            
    def spp(self, msg):
        if self.do_print:
            print(msg)
        elif self.do_special:
            print(msg)

def new_log() -> log_mgr:
    return log_mgr(flags["-p"], flags["-vb"], flags["-sp"])

def exec_featured():
    l.log("\nstarting up...")
    featlen = len(features.keys())
    for i, f_key in enumerate(features.keys()):
        ft = features[f_key]
        if ft["enabled"]:
            l.log(f"({i+1}/{featlen}) running {str.format(f_key)}...")
            for comm in ft["commands"]:
                # hide output?
                if flags["-vb"]:
                    os.system(comm)
                else:
                    os.system(f"{comm} >/dev/null 2>&1")
        else:
            l.vb(f"({i}/{featlen}) skipped {f_key}")

def print_args(_args):
    arglen = len(_args)
    if arglen == 0:
        l.vb(f"{arglen} arguments given")
    else :
        for i, arg in enumerate(_args):
            l.spp(f"({i+1}/{arglen}) : {arg}")

def parse_flags(_args) -> list:
    
    _flags = []
    _flagless = []
    
    l.log("\nparsing flags...")
    # unload flags
    for arg in _args:
        if arg in valid_flags:
            if arg not in _flags:
                _flags.append(arg)
        else:
            if arg[0] == "-":
                l.log(f"unknown flag \"{arg}\"")
            else:
                _flagless.append(arg)
                        
    # update flags: toggle defaults
    for arg in _flags:
        flags[arg] = not flags[arg]
    
    # if -sp then override other flags
    if flags["-sp"]:
        flags["-p"] = False
        flags["-vb"] = False
        flags["-db"] = False
    
    return _flagless

def parse_args(_args):
    l.log("\nparsing args...")
    if len(_args) > 0:
        if _args[0] not in valid_args:
            l.log(f"argument \"{_args[0]}\" was not expected")
            clean_exit()
        else:
            if _args[0] == "help":
                l.log("help ::\nvalid arguments:\n\t{0}".format('\n\t'.join(valid_args)))
                l.log("valid flags:\n\t{0}".format('\n\t'.join(valid_flags)))
                clean_exit()

            # runs the program with a set of example arguments to show how they are handed by sys
            elif _args[0] == "demo":
                demo_args = f'{["one", "2"]} three {{"four" : 5, "six" : 7}} {[{ }, {"2.1" : 2.2, "2.3" : [2.4, 2.5]}]}'
                demo_command = f"python startup.py -sp demoargs {demo_args}"
                l.log(f"example of argument parsing: \"{demo_command}\"\n")
                os.system(demo_command)
                clean_exit()

            # special arg for prining remaining args
            elif _args[0] == "demoargs":
                l.sp("see demoargs...")
                # print out remainding args
                print_args(_args[1:])
                clean_exit()
            
            else:
                # actual args, handle sensibly
                for arg in _args:
                    unknown_arg = True
                    for f_key in features.keys():
                        ft = features[f_key]
                        if arg == f_key or arg in ft["shorthand"]:
                            features[f_key]["enabled"] = True
                            unknown_arg = False
                    if unknown_arg:
                        l.log(f"unhandled arg: {arg}")

def get_file_contents(file_path) -> str:
    f = open(file_path, "r")
    ret = f.read()
    f.close()
    return ret

def clean_exit():
    l.log("\nexiting\n")
    exit(0)

def startup() -> list:
    global l
    # first is file name
    _args = parse_flags(sys.argv[1:])
    # re-init log with flags
    l = new_log()
    return _args

def load_features(_file) -> dict:
    l.log(f"\nloading {_file}...")
    # locate featured.json
    _features = json.loads(get_file_contents(_file))
    return validate_features(_features)

def validate_features(_features) -> dict:
    _valid = {}
    for f_key in _features.keys():
        if type(_features[f_key]) is dict:
            is_valid = True
            for field in valid_feature_fields:
                if field not in _features[f_key].keys():
                    is_valid = False
                    # notify of error
                    l.log(f"feature \"{f_key}\" is missing field \"{field}\"")
            if is_valid:
                _valid[f_key] = _features[f_key]
        else:
            l.log(f"feature \"{f_key}\" is not valid: {_features[f_key]}")
    return _valid

def update_valid_args(_valid_args):
    for ft in features.keys():
        _valid_args.append(ft)
        if "shorthand" in features[ft].keys():
            for sh in features[ft]["shorthand"]:
                _valid_args.append(sh)
    l.vb(f"updated valid args: {_valid_args}")
    return _valid_args

# set up log with defaults
l = new_log()

if __name__ == "__main__":
    
    # handle flags
    args = startup()
    
    # load features from file
    features = load_features(default_feature_path)
    # add loaded features to valid args
    valid_args = update_valid_args(valid_args)
    
    # handle remaining args
    parse_args(args)
    
    # run any macros
    exec_featured()

    l.log("\nfinished!\n")
    
else:
    l.log(f"else main?: {__name__}\n")
