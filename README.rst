splitviewfuse
=============
.. image:: https://secure.travis-ci.org/seiferma/splitviewfuse.png
    :target: http://travis-ci.org/seiferma/splitviewfuse
.. image:: https://coveralls.io/repos/seiferma/splitviewfuse/badge.png?branch=master
    :target: https://coveralls.io/r/seiferma/splitviewfuse?branch=master

Description
-----------
A view on a given directory that splits large files into segments implemented as FUSE file system.
An additional filesystem that merges such segments into regular files is included as well.

Installation
------------
The file system is available for Python 2 via pypi (splitviewfuse).

Usage
-----
``splitviewfuse <source directory> <mount point> -o segmentsize=<size>``

``unionviewfuse <source directory> <mount point> -o segmentsize=<size>``

+-------------------------+-----------------------------------------------------------+
| Option Value            | Meaning                                                   |
+=========================+===========================================================+
| ``source directory``    | The directory containing the files to be encrypted        |
+-------------------------+-----------------------------------------------------------+
| ``mount point``         | The mount point for the encrypted view                    |
+-------------------------+-----------------------------------------------------------+
| ``segmentsize``         | The maximum size of a segment in bytes                    |
+-------------------------+-----------------------------------------------------------+