import imp, os.path, inspect, os

from system_autopsy.utils import *

# Figure out what components to import/use
# Try current directory
possible_local_module = os.path.join(os.getcwd(), 'system_autopsy_components.py')
possible_home_module = os.path.join(os.path.expanduser("~"), 'system_autopsy_components.py')
if os.path.isfile(possible_local_module):
    components = imp.load_source('components', possible_local_module)
elif os.path.isfile(possible_home_module):
    components = imp.load_source('components', possible_home_module)
else:
    import system_autopsy.default_components as components

def all_components():
    results = []
    for name, value in inspect.getmembers(components):
        try:
            if issubclass(value, Component):
                results.append(value)
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

