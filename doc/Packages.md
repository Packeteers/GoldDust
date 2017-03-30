GoldDust Packages
=================

A package is an installable unit of code/resources/etc. Packages are sourced
from a repository in the form of a bzipped tarball (`.tar.bz2`). They are also
accompanied by a detached PGP signature (`.sig`).

Tree
----
```
    <root>
      package.json
      package.py
      game
        <package files>
      <optionally, more files that won't be automatically installed>
```

Install Scripts
---------------

A package may optionally have a install script (as `package.py`). This script
contains a class that extends `golddust.packages.InstallScript` which
implements the `pre_install` and `post_install` methods. These allow a package
to run code before or after it's been installed. An example of the use of this
is the Minecraft Forge package, which needs to make modifications to the
Minecraft JAR.