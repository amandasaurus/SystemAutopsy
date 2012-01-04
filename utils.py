
from functools import wraps
import subprocess
import tempfile, os
from multiprocessing import Process

def diagnostic_function(func):
    func.diagnostic_function = True
    func.name = func.__name__.lower()
    return func

def bash_command(func):
    @diagnostic_function
    @wraps(func)
    def inner(*args, **kwargs):
        command = func(*args, **kwargs)
        try:
            output = subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as err:
            output = "Error: "+repr(err)
        return output

    return inner

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

            def run():
                print 'start', component.name, function.name
                with open(os.path.join(root, function.name), 'w') as fp:
                    output = function()
                    fp.write(output)
                print 'end', component.name, function.name

            proc = Process(target=run)
            all_procs.append(proc)
            proc.start()

    while True:
        alive_procs = [p for p in all_procs if p.is_alive()]
        if len(alive_procs) == 0:
            break
        else:
            # wait for one of them to finish
            alive_procs[0].join()
    
