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


import json
import warnings


"""GoldDust Packages Classes/Utilities
"""


class Package:
    """A package managed by GoldDust"""
    def __init__(self):
        self.name = ""
        self.version = ""
        self.description = ""
        self.website = ""
        self.author = ""
        self.packager = ""
        self.dependencies = []

    @property
    def tarball(self):
        """The tarball file name for this package."""
        return "{}-{}.tar.bz2".format(self.name, self.version)

    @property
    def sig_file(self):
        """The detached signature file name for this package."""
        return "{}.sig".format(self.tarball)

    @classmethod
    def from_package_file(cls, file):
        """Create a Package instance using a package.json file.

        Takes:
            file: The path to the `package.json` file.

        Returns: A new Package instance with parameters set by the
                 package.json file.
        """
        package = cls()

        with open(file) as package_file:
            metafile = json.load(package_file)

        package.name = metafile['packagename']
        package.version = metafile['version']
        package.description = metafile['description']
        package.website = metafile['website']
        package.author = metafile['author']
        package.packager = metafile['packager']
        # TODO: Dependencies
        return package

    def verify(self):
        """Verify the integrity of this package.

        This verifies the package tarball using its detached PGP signature.
        """
        warnings.warn("Package verification is not yet implemented. "
                      "You are working with an unverified package.")
        return True


class InstallScript:
    """Package pre/post install action script.

    These functions are used to perform extra work beyond extracting
    files.

    Note that JAR modification should only be done using the `munge_jar`
    function. This lets GoldDust know that you're modifying the JAR so it
    can properly handle other JAR mod packages as well.
    """
    def pre_install(self):
        """Called before any files are installed.
        """
        pass

    def munge_jar(self, jar):
        """Modify the Minecraft JAR file.
        """
        pass

    def post_install(self):
        """Called after files are installed.
        """
        pass
