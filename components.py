from utils import * 

class Basics(Component):
    @bash_command
    def disk_usage(self):
        return "df"

    @bash_command
    def open_files(self):
        return 'lsof'

    @bash_command
    def memory_usage(self):
        return "free"

class Apache(Component):
    @bash_command
    def running_procs(self):
            return "ps -p $(pgrep -u www-data) 2>/dev/null"

class Network(Component):
    @bash_command
    def open_connections_lsof(self):
        return "lsof -i"

    @bash_command
    def netstat(self):
        return 'netstat'

    @bash_command
    def ifconfig(self):
        return 'ifconfig -a'

    @bash_command
    def ip_link_show(self):
        return 'ip link show'


class MySQL(Component):
    @bash_command
    def running(self):
        return "ps -fp $(pgrep -u mysql)"

    @iterate_on(pids_matching('-u mysql'))
    @takes_own_filename
    def strace_mysqld(self, pid, filename):
        return "timeout 10s strace -o {filename} -f -p {pid}".format(filename=filename, pid=pid)
