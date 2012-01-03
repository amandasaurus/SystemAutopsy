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
