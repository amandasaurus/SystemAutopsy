
from functools import wraps
import subprocess
import tempfile, os

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

    def run(self):
        root = os.path.join(self.working_dir, self.name)
        os.mkdir(root)
        functions = [getattr(self, x) for x in dir(self) if x[:2] != '__' and getattr(getattr(self, x), 'diagnostic_function', False)]
        for function in functions:
            with open(os.path.join(root, function.name), 'w') as fp:
                output = function()
                fp.write(output)


