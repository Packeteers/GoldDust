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


import json
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
    gdust = GoldDust(gdhome)
    gdust.save_global_config()


class GlobalConfig:
    """GoldDust global configuration.

    This configuration holds information about repositories and their
    mirrors.
    """
    def __init__(self):
        self.repositories = []

    def get_repository(self, repo):
        """Get the repository dict from a repository name.

        Takes:
            repo (str): The repository name to get.

        Raises:
            KeyError if the repository doesn't exist in the configuration.

        Returns the dict for the requested repository."""
        target = None
        for repo_dict in self.repositories:
            if repo_dict["name"] == repo:
                target = repo_dict

        if not target:
            raise KeyError("Repository doesn't exist in configuration.")

        return target

    def add_repository(self, name, mirrors):
        """Add a repository to the global configuration.

        Takes:
            name (str): The name for this repository. Traditionally
                        alphanumeric-only in lowercase.
            mirrors (list of str): HTTP(S) mirrors of this repository.

        Raises:
            ValueError: The repository already exists in the configuration.
        """
        for repo in self.repositories:
            if repo["name"] == name:
                raise ValueError("Repository already exists in configuration.")

        self.repositories.append({"name": name, "mirrors": mirrors})

    def remove_repository(self, name):
        """Remove a repository from the GoldDust configuration.

        Takes:
            name (str): The name of the repository to remove.

        Raises:
            KeyError: The repository does not exist in the configuration.
        """
        self.repositories.remove(self.get_repository(name))

    def add_mirror(self, repo, mirror):
        """Add a mirror to the configuration for a repository.

        Takes:
            repo (str): The repo name to add the mirror to.
            mirror (str): The HTTP(S) URI of the mirror.

        Raises:
            KeyError: The repository doesn't exist in the configuration.
        """
        target = self.get_repository(repo)["mirrors"]
        if mirror in target:
            raise KeyError("Mirror already exists for repository.")
        target.append(mirror)


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


class GoldDust:
    """An instance of the GoldDust package manager."""
    def __init__(self, root):
        self.config = GlobalConfig()
        self.root = root

        if os.path.isfile(os.path.join(self.root, "config.json")):
            self.load_global_config()

    def save_global_config(self):
        """Save the global configuration."""
        config = open(os.path.join(self.root, "config.json"), "w+")
        json.dump(self.config.__dict__, config, sort_keys=True, indent=4)
        config.close()

    def load_global_config(self):
        """Load the global configuration from a file."""
        pass
