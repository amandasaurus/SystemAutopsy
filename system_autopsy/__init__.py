#! /usr/bin/python

from utils import *
from default_components import *

def all_components():
    results = []
    for i in globals().values():
        try:
            if issubclass(i, Component) and i != Component:
                results.append(i)
        except TypeError:
            pass
    return results


def main():
    tempdir = tempfile.mkdtemp(prefix="autopsy.")
    print "Working in ", tempdir
    components = [kls(tempdir) for kls in all_components()]

    # run all 
    run_all(tempdir, components)

    
if __name__ == '__main__':
    main()

