GoldDust Packages
=================

A package is an installable unit of code/resources/etc. Packages are sourced
from a repository in the form of a bzipped tarball (`.tar.bz2`). They are also
accompanied by a detached Ed25519 signature (`.sig`). This signature scheme
is based on (and compatible with) OpenBSD's `signify` utility.

Tree
----
```
    <root>
      package.json
      package.py (optional)
      game
        <package files>
      <optionally, more files that won't be automatically installed>
```

package.json
------------

`package.json` is the metadata file for the package. Its fields are:

- `packagename` (String): The package's name. This is case-sensitive and may
  contain only alphanumeric characters and underscores (_).
- `version` (String): XXX TODO versioning scheme (semver + epoch?)
- `description` (String): A description of the contents of this package.
- `website` (String): The package content's website (or similar).
- `author` (String): The package content's author (for example, mod creator).
- `packager` (String): Your name/contact as the packager.
- `dependencies` (List of Strings): XXX Not yet implemented.


Install Scripts
---------------

A package may optionally have a install script (as `package.py`). This script
contains a class that extends `golddust.packages.InstallScript` which
implements the `pre_install`, `post_install`, and `munge_jar` methods. These
allow a packageto run code before or after it's been installed. An example of
the use of thisis the Minecraft Forge package, which needs to make
modifications to theMinecraft JAR.

The contents of the `game` are extracted to the `.minecraft` (or equivalent)
folder of the instance.
