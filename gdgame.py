#!/usr/bin/env python3

#  Copyright 2015-2016 John "LuaMilkshake" Marion
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
import gdcli


def newinstance():
    """Create a game instance."""
    pass


def main():
    argparser = argparse.ArgumentParser(description=("Manage modded game "
                                                     "installations with "
                                                     "GoldDust."))
    argparser.add_argument('-H', '--gdhome',
                           help=("The location of the GoldDust installation. "
                                 "This contains things like the primary "
                                 "config as well as package databases."),
                           metavar="PATH")
    argparser.add_argument('-q', '--noprompt',
                           help=("Disable user interaction, assume defaults "
                                 "unless otherwise specified."),
                           action='store_true')
    argparser.add_argument('-v', '--verbose',
                           help="Output more detailed status messages.",
                           action='store_true')
    subparser = argparser.add_subparsers()

    # 'newinstance' subcommand
    newinst_parse = subparser.add_parser('newinstance')
    newinst_parse.add_argument('-n', '--name',
                               help="The short name of the instance. Should "
                                    "be alphanumeric and will be converted to "
                                    "lowercase.", required=True)
    newinst_parse.add_argument('-p', '--path',
                               help="The path to the root of this instance.",
                               required=True)
    newinst_parse.add_argument('-N', '--longname',
                               help="The user-friendly name for this "
                                    "instance.")
    newinst_parse.set_defaults(func=newinstance)

    args = argparser.parse_args()

    gdhome = args.gdhome

    if not args.gdhome:
        gdhome = golddust.default_home_dir()

    if not os.path.isdir(gdhome):
        if not args.noprompt:
            sys.stdout.write("GoldDust doesn't appear to be installed. ")
            sys.stdout.flush()
            if not gdcli.ask_confirm("Install GoldDust?", False):
                return
            # If the user never specified --gdhome, ask them where they might
            # want GoldDust installed.
            if not args.gdhome:
                gdhome = gdcli.ask_string("Where should GoldDust be installed?",
                                          gdhome)

        gdhome = os.path.abspath(os.path.expanduser(gdhome))

        if args.verbose:
            sys.stdout.write("Installing GoldDust to '{}'...\n".format(gdhome))
            sys.stdout.flush()

        golddust.install_home_dir(gdhome)

        if args.verbose:
            sys.stdout.write("GoldDust successfully installed!\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
