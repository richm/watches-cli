"""
watches

Usage:
  watches ( cluster_health | cluster_state ) [--url=URL]
  watches -h | --help
  watches --version

Options:
  -h --help         Show this screen.
  --version         Show version.
  --url=URL         URL of ES node HTTP endpoint [default: http://localhost:9200].

Examples:
  watches cluster_health --url=http://localhost:9200

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/lukas-vlcek/watches-cli
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for k, v in options.iteritems():
        if hasattr(commands, k) and v:
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
