#!/usr/bin/env python3

#  Copyright 2015-2017 John "LuaMilkshake" Marion
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import os
import sys

import golddust


class GDGameTool:
    """Manage modded game installations with GoldDust."""
    def __init__(self):
        self._golddust = None
        argparser = argparse.ArgumentParser(description=("Manage modded game "
                                                         "installations with "
                                                         "GoldDust."))
        argparser.add_argument('-H', '--gdhome',
                               help=("The location of the GoldDust "
                                     "installation. This contains things like "
                                     "the primary config as well as package "
                                     "databases."),
                               metavar="PATH")
        argparser.add_argument('-q', '--noprompt',
                               help=("Disable user interaction, assume "
                                     "defaults unless otherwise specified."),
                               action='store_true')
        argparser.add_argument('-v', '--verbose',
                               help="Output more detailed status messages.",
                               action='store_true')
        subparser = argparser.add_subparsers(dest="subcommand")

        # 'newinstance' subcommand
        newinst_parse = subparser.add_parser('newinstance')
        newinst_parse.add_argument('-n', '--name',
                                   help="The short name of the instance. "
                                        "Should be alphanumeric and will be "
                                        "converted to lowercase.",
                                   required=True)
        newinst_parse.add_argument('-p', '--path',
                                   help="The path to the root of this "
                                        "instance.",
                                   required=True)
        newinst_parse.add_argument('-N', '--longname',
                                   help="The user-friendly name for this "
                                        "instance.")

        # 'deleteinstance' subcommand
        newinst_parse = subparser.add_parser('deleteinstance')
        newinst_parse.add_argument('-n', '--name',
                                   help="The short name of the instance. "
                                        "Should be alphanumeric and will be "
                                        "converted to lowercase.",
                                   required=True)
        newinst_parse.add_argument('-R', '--deletefiles',
                                   help="Delete the game files as well.",
                                   action='store_true')

        self.args = argparser.parse_args()
        if not self.args.gdhome:
            self.gdhome = golddust.default_home_dir()
        else:
            self.gdhome = self.args.gdhome

        if not os.path.isdir(self.gdhome):
            if not self.gd_not_installed():
                return

        self._golddust = golddust.GoldDust(self.gdhome)

        if self.args.subcommand == "newinstance":
            self.new_instance()
        elif self.args.subcommand == "deleteinstance":
            self.delete_instance()
        else:
            argparser.print_usage()

    def gd_not_installed(self):
        """Prompt the user (unless --noprompt) to install GoldDust.

        Returns:
            True for successful installation, False if the user
            refused installation.
        """
        if not self.args.noprompt:
            sys.stdout.write("GoldDust doesn't appear to be installed. ")
            sys.stdout.flush()
            if not golddust.gdcli.ask_confirm("Install GoldDust?", False):
                return False
            # If the user never specified --gdhome, ask them where they
            # might want GoldDust installed.
            if not self.args.gdhome:
                self.gdhome = golddust.gdcli.ask_string("Where should "
                                                        "GoldDust be "
                                                        "installed?",
                                                        self.gdhome)

        self.gdhome = os.path.abspath(os.path.expanduser(self.gdhome))

        if self.args.verbose:
            sys.stdout.write("Installing GoldDust to "
                             "'{}'...\n".format(self.gdhome))
            sys.stdout.flush()

        golddust.install_home_dir(self.gdhome)

        if self.args.verbose:
            sys.stdout.write("GoldDust successfully installed!\n")
            sys.stdout.flush()

        return True

    def new_instance(self):
        """Create a game instance.
        """
        if self.args.verbose:
            sys.stdout.write("Creating instance "
                             "'{}' at '{}'\n".format(self.args.name,
                                                     self.args.path))
            sys.stdout.flush()

        self._golddust.create_instance(self.args.name, self.args.longname,
                                       self.args.path)

        if self.args.verbose:
            sys.stdout.write("Instance '{}' created successfully.\n"
                             .format(self.args.name))
            sys.stdout.flush()

    def delete_instance(self):
        """Delete a game instance.
        """
        if self.args.verbose:
            sys.stdout.write("Removing instance '{}'\n".format(self.args.name))
            sys.stdout.flush()

        self._golddust.remove_instance(self.args.name,
                                       remove_game_files=self.args.deletefiles)

        if self.args.verbose:
            sys.stdout.write("Instance '{}' removed.\n".format(self.args.name))
            sys.stdout.flush()


def main():
    # An independent function is needed here because console_scripts prints
    # the return value of the script entry point, which for GDGameTool() is
    # a class instance. (We want None so it doesn't print anything.)
    GDGameTool()


if __name__ == "__main__":
    # Just in case someone calls this directly. I call main() instead of
    # instantiating GDGameTool() in case main() gets extra code at some point
    # in the future.
    main()
