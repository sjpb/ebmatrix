Identify common toolchains between multiple EasyBuild packages.

Usage:

    python ebmatrix.py PACKAGE1 [PACKAGE2 ... PACKAGE_N]

where PACKAGE* is the full easybuild package name (case-sensitive), e.g. OSU-Micro-Benchmarks.

Note this is *not* the same as accepted by `eb -S`, which takes a regex.

This will print (to stdout) info all toolchains which have easyconfigs for all given packages, and the easyconfigs for those packages.

Requires python 3.