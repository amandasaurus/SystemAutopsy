
from functools import wraps
import subprocess
import tempfile, os
from multiprocessing import Process

def diagnostic_function(func):
    func.diagnostic_function = True
    func.generate_arguments = lambda func=func: []
    return func

def bash_command(func):
    @diagnostic_function
    @wraps(func)
    def inner(self, root, *args, **kwargs):
        command = func(self, *args, **kwargs)
        name = func.__name__.lower()
        with open(os.path.join(root, name), 'w') as fp:
            try:
                fp.write(subprocess.check_output(command, shell=True))
            except subprocess.CalledProcessError as err:
                output = "Error: "+repr(err)

    return inner

def iterate_on(first_arg_func):
    def decorator(func):
    
        @wraps(func)
        def inner(self, root, *args, **kwargs):
            command = func(self, *args, **kwargs)
            name = func.__name__.lower()
            with open(os.path.join(root, name), 'w') as fp:
                try:
                    fp.write(subprocess.check_output(command, shell=True))
                except subprocess.CalledProcessError as err:
                    output = "Error: "+repr(err)

        def _generate_arguments():
            return first_arg_func()

        inner.generate_arguments = _generate_arguments
        inner.diagnostic_function = True

        return inner

    decorator.first_arg_func = first_arg_func

    #import pdb ; pdb.set_trace()

    return decorator

# TODO try with class

def command_output(func):
    @diagnostic_function
    @wraps(func)
    def inner(*args, **kwargs):
        command = func(*args, **kwargs)
        try:
            output = subprocess.check_output(command)
        except subprocess.CalledProcessError as err:
            output = "Error: "+repr(err)
        return output

    return inner


class Component(object):
    def __init__(self, working_dir):
        self.working_dir = working_dir

    @property
    def name(self):
        return self.__class__.__name__.lower()

    

def run_all(working_dir, components):
    """Runs each part of each component in a subprocess"""
    all_procs = []
    for component in components:
        root = os.path.join(working_dir, component.name)
        os.mkdir(root)
        functions = [getattr(component, x) for x in dir(component) if x[:2] != '__' and getattr(getattr(component, x), 'diagnostic_function', False)]
        for function in functions:
            # a function might correlate to one process, or it might need many processes
            arguments = function.generate_arguments()
            if len(arguments) == 0:
                # no special arguments needed
                proc = Process(target=function, args=(root,))
                all_procs.append(proc)
                proc.start()
            else:
                for args, kwargs in arguments:
                    proc = Process(target=function, args=([root]+args), kwargs=kwargs)
                    all_procs.append(proc)
                    proc.start()
                
    # wait for all subprocesses to finish
    for proc in all_procs:
        if proc.is_alive():
            proc.join()

def pids_matching(format):
    def inner():
        lines = subprocess.check_output("pgrep "+format, shell=True)
        lines = [x.strip() for x in lines.split("\n")]
        lines = [x for x in lines if x != '']
        pids = [int(x.strip()) for x in lines]
        return [ ( [pid], {} ) for pid in pids ]
    inner.__name__ = "pids_matching %s" % (format)
    return inner

