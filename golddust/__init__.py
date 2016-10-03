# Copyright 2015-2016 John "LuaMilkshake" Marion
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

"""GoldDust package management library.

GoldDust manages modded installations of the game Minecraft. This
package implements a package manager for mod files (including
Minecraft Forge and texture packs).
"""


import os
import platform


def default_home_dir():
    """Get the default home directory path on this platform.

    This is an absolute form of "~/.golddust" on all platforms except
    for Windows, where it is "%APPDATA%/.golddust".

    In the strange case where APPDATA isn't set on Windows, will default
    to the non-Windows behavior.

    Returns str, the absolute path of "~/.golddust" (non-Windows),
        "%APPDATA/.golddust" (Windows).
    """
    path = "~/.golddust"

    if platform.system() == "Windows" and "APPDATA" in os.environ:
        path = os.path.join(os.environ["APPDATA"], ".golddust")

    return os.path.abspath(os.path.expanduser(path))


def write_default_config(path):
    """Write out a default GoldDust configuration.
    """
    config = open(path, "w+")
    # TODO Actually serialize a configuration
    config.write("{}")
    config.close()


def install_home_dir(path):
    """Install the GoldDust home directory.

    The home directory is used for global configuration, local package caches,
    and instance information.

    Takes:
        path (str): Path to install the home directory to. Should not exist.

    Raises:
        FileExistsError: The path supplied already exists.
    """

    if os.path.isdir(path):
        raise FileExistsError("Installation target directory shouldn't exist.")

    gdhome = os.path.abspath(os.path.expanduser(path))

    # Create directories and config file
    os.mkdir(gdhome, mode=0o755)
    os.mkdir(os.path.join(gdhome, "pkgcache"))
    os.mkdir(os.path.join(gdhome, "instances"))
    write_default_config(os.path.join(gdhome, "config.json"))


class Package:
    """A package managed by GoldDust"""
    def __init__(self):
        self.name = ""
        self.version = ""

    @property
    def tarball(self):
        """The tarball file name for this package."""
        return "{}-{}.tar.bz2".format(self.name, self.version)

    @property
    def sig_file(self):
        """The detached signature file name for this package."""
        return "{}.sig".format(self.tarball)
