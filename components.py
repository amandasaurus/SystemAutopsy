from utils import * 

class Disk(Component):
    @command_output
    def usage(self):
        return ['df']

    @command_output
    def open_files(self):
        return ['lsof']

class Apache(Component):
    @bash_command
    def running(self):
        return "ps -fp $(pgrep -u www-data)"

class Network(Component):
    @command_output
    def open_connections_lsof(self):
        return ['lsof', 'i']

    @command_output
    def netstat(self):
        return ['netstat']

class MySQL(Component):
    @bash_command
    def running(self):
        return "ps -fp $(pgrep -u mysql)"
