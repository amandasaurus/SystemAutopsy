from utils import * 

class Basics(Component):
    @bash_command
    def disk_usage(self):
        return "df"

    @bash_command
    def open_files(self):
        return 'lsof'

class Apache(Component):
    @bash_command
    def running(self):
        return "ps -fp $(pgrep -u www-data)"

class Network(Component):
    @bash_command
    def open_connections_lsof(self):
        return "lsof -i"

    @bash_command
    def netstat(self):
        return 'netstat'

class MySQL(Component):
    @bash_command
    def running(self):
        return "ps -fp $(pgrep -u mysql)"
