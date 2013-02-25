SystemAutopsy is a programme to take a quick snapshot of what your Linux system
is doing and save that to a file for later examination.

If a server has a problem, one often has to try to figure out what's going on
*and* also also get it back running. Sometimes one don't have the time to figure
out what's wrong, you have to get things works **now**. Sometimes there are easy
solutions you can do (like restart a server/service), but that means you can no
longer diagnose the problem. Additionally some problems might be intermittant
and go away soon, meaning the problem goes away.

SystemAutopsy is designed for these cases. It saves the output from various
commands to files, allowing you to pour over it later.

Quick Start Guide
-----------------

SystemAutopsy is installable with pip:

    pip install SystemAutopsy

To get an autopsy of your system just run:

    autopsy

This command will run and collect the default system statistics and save it in
a file in your home directory, called ``autopsy.$DATE_TIME_WHEN_RUN.tar.gz``

Configuration
-------------

What things to save is used via ``Components``. It includes some good defaults
for a LAMP server in ``system_autopsy.default_components``. You can define your
own Components in a python module file. By default SystemAutopsy will look for
a file ``system_autopsy_components.py`` in the current directory, failing that,
your home directory, or failing both of them, it'll use the default components
included with SystemAutopsy.

A simple Component looks like this:

    from system_autopsy.utils import Component, bash_command

    class Basics(Component):
        @bash_command
        def disk_usage(self):
            return "df"

This defines a Component called ``Basics`` which has one output (called
``disk_usage``). The archive file will have one directory called ``basics``,
which has one file called ``disk_usage``, which will be the output from running
``df``.

Every ``bash_command`` will have its output in it's own file, with filename
based on the function name. Some tools can save output themselves (e.g.
``strace``), so you can skip the default saving, by using the
``@takes_own_filename``. Your function should take a ``filename`` argument
which will be the filename.

    from system_autopsy.utils import Component, bash_command

    class Basics(Component):
        @bash_command
        @takes_own_filename
        def strace_something(self, filename):
            return "strace -o %s -p 1000" % filename

Producing more than one output file
===================================

By default one function will produce one file, however sometimes you want to
run on command on many things (e.g. for each pid that matches something), this
can be done with the ``@iterate_on`` decorator. It takes one argument, a
function that will return a list of ``(arg, kwargs)`` to pass into the
function. Every element in the list will produce a new file

SystemAutopsy comes with one utility function for this ``pids_matching``, which
will return all the PIDs that match this ``pgrep`` argument. So
``pids_matching('-u mysql')`` returns all PIDS that are from the ``mysql``
user.

For example to strace (for 10 seconds) all ``mysql`` processes, you can use
this command:

    from system_autopsy.utils import Component, iterate_on, pids_matching

    class Basics(Component):

        @iterate_on(pids_matching('-u mysql'))
        def strace_mysqld(self, pid):
            return "timeout 10s strace -f -p {pid}".format(pid=pid)


*(Note: since strace puts output on stderr, not stdout, you should use
@takes_own_filename here)*


Licence
-------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

