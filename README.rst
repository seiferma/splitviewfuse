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

Symbolic links are resolved and treated as regular files and folders.

Installation
------------
The file system is available for Python 2 via pypi (splitviewfuse).

Usage
-----
``splitviewfuse <source directory> <mount point> -o segmentsize=<size>,loglevel=debug,logfile=<path>``

``unionviewfuse <source directory> <mount point> -o segmentsize=<size>,loglevel=debug,logfile=<path>``

+-------------------------+----------------------------------------------------------------------------------------+
| Option Value            | Meaning                                                                                |
+=========================+========================================================================================+
| ``source directory``    | The directory containing the files to be encrypted                                     |
+-------------------------+----------------------------------------------------------------------------------------+
| ``mount point``         | The mount point for the encrypted view                                                 |
+-------------------------+----------------------------------------------------------------------------------------+
| ``segmentsize``         | The maximum size of a segment in bytes (part of mount options)                         |
+-------------------------+----------------------------------------------------------------------------------------+
| ``loglevel``            | The loglevel ``debug``, ``info``, ``warn``, or ``error`` (optional, default: ``info``) |
+-------------------------+----------------------------------------------------------------------------------------+
| ``logfile``             | The path of a file that contains the log messages (optional)                           |
+-------------------------+----------------------------------------------------------------------------------------+

The values for the mount options (-o) are not restricted to the ones mentioned above. Values not specific to this file system are passed to the underlying fuse implementation and are processed there. For instance, you can add the ``allow_other`` option and it will be processed as known from other filesystems.
