# GoldDust Package Manager

GoldDust is a package manager for modded installations of the game Minecraft.


## Tools

GoldDust is made up of multiple tools to handle buidling packages, managing
package repositories, and installing packages.


### `gdmake` - Make packages

The `gdmake` tool creates packages from package specifications. The output of
`gdmake` will be a `.tar.bz2` archive containing installable content to a game
instance. A detached Ed25519 signature (`.tar.bz2.sig`) will also be created to
authenticate the package. This signature is based on OpenBSD's signify utility.


### `gdrepo` - Manage GoldDust repository

The `gdrepo` tool is used to maintain the repository of installable packages.


### `gdgame` - Manage game instances and their packages

The `gdgame` tool manages game installations. This includes creating, updating,
and deleting game instances and installing, updating, and removing packages.

A GUI frontend to gdgame is planned to make management of installations easier
for end users.


## License

	Copyright 2014-2017 John "LuaMilkshake" Marion

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

		http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.
