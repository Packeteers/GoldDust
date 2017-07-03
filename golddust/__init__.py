# Copyright 2015-2017 John "LuaMilkshake" Marion
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
import shutil


_CONFIG_FILE_NAME = "config.json"


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
        target = self.get_repository(repo)
        if mirror in target["mirrors"]:
            raise KeyError("Mirror already exists for repository.")
        target["mirrors"].append(mirror)


class Instance:
    """A game instance.

    Game instances are essentially a `.minecraft` folder that is managed
    by GoldDust.
    """
    def __init__(self, config_file):
        self._config_file = config_file
        """The path to the instance config."""
        self.path = ""
        """The path to this instance's game files on disk."""
        self.longname = ""
        """The long-form user-friendly name for this instance."""

    def load(self):
        """Load this instance from a config file.
        """
        with open(self._config_file, mode="r") as config:
            loaded_config = json.load(config)
            self.path = loaded_config["path"]
            self.longname = loaded_config["longname"]

    def save(self):
        """Save this instance's configuration to disk.
        """
        with open(self._config_file, mode="w") as config:
            config_out = {}
            config_out["path"] = self.path
            config_out["longname"] = self.longname
            json.dump(config_out, config, sort_keys=True, indent=4)


class GoldDust:
    """An instance of the GoldDust package manager."""
    def __init__(self, root):
        self.config = GlobalConfig()
        self.root = os.path.abspath(os.path.expanduser(root))

        if os.path.isfile(os.path.join(self.root, _CONFIG_FILE_NAME)):
            self.load_global_config()

    def save_global_config(self):
        """Save the global configuration."""
        with open(os.path.join(self.root, _CONFIG_FILE_NAME), "w") as config:
            json.dump(self.config.__dict__, config, sort_keys=True, indent=4)

    def load_global_config(self):
        """Load the global configuration from a file."""
        with open(os.path.join(self.root, _CONFIG_FILE_NAME), "r") as config:
            self.config.__dict__ = json.load(config)

    def create_instance(self, name, longname, path):
        """Create the files for a new game instance.

        Takes:
            name (str): The instance name. Must be alphanumeric and unique.
            longname (str): The user-friendly name of this instance.
            path (str): The path to the instance's files
                        (eg '~/.minecraft'). Must not yet exist.

        Raises:
            ValueError: The instance name must be alphanumeric.
            FileExistsError: Instance path already exists.
        """
        if not name.isalnum():
            raise ValueError("Instance name must be alphanumeric.")
        name = name.lower()

        # Expand '~' if the shell didn't already do it
        path = os.path.expanduser(path)

        if os.path.exists(path):
            raise FileExistsError("Instance path already exists.")
        os.mkdir(path)

        instance_file = os.path.join(self.root, "instances",
                                     "{}.json".format(name))
        if os.path.exists(instance_file):
            raise FileExistsError("Instance name is already in use.")

        instance = Instance(config_file=instance_file)
        instance.longname = longname
        instance.path = path
        instance.save()

    def remove_instance(self, instance_name, remove_game_files=False):
        """Removes an instance and (optionally) its game files.

        Takes:
            instance_name (str): The instance name as defined
                                 in <gdhome>/instances
            remove_game_files (bool): `True` to also delete the game
                                      installation directory.
        """
        config_file_name = os.path.join(self.root, "instances",
                                        "{}.json".format(instance_name))

        instance = Instance(config_file=config_file_name)
        instance.load()

        if remove_game_files:
            shutil.rmtree(instance.path)

        os.remove(config_file_name)
