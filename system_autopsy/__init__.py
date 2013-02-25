import imp, os.path, inspect, os
import datetime, shutil

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
            if issubclass(value, Component) and value != Component:
                results.append(value)
        except TypeError:
            pass
    return results


def main():
    start_datetime = datetime.datetime.utcnow().isoformat()

    tempdir = tempfile.mkdtemp(prefix=("autopsy.%s." % start_datetime))
    components = [kls(tempdir) for kls in all_components()]

    # run all 
    run_all(tempdir, components)

    # zip it up
    archive_name = shutil.make_archive(os.path.join(os.path.expanduser("~"), "autopsy.%s" % start_datetime), format="gztar", root_dir=tempdir)
    print "Archive of results in %s" % archive_name
    shutil.rmtree(tempdir)


    
if __name__ == '__main__':
    main()

