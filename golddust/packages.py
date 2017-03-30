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


"""GoldDust Packages Classes/Utilities
"""


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


class InstallScript:
    """Package pre/post install action script.
    """
    def pre_install(self):
        """Called before any files are installed.
        """
        pass

    def post_install(self):
        """Called after files are installed.
        """
        pass
