.. :changelog:

Release History
---------------

0.3.0.1 (2014-08-17)
++++++++++++++++++++

* Added wheel universal support to both python 2 and 3.
* Fixed beta release date in HISTORY.rst.

0.3.0 (2014-08-17)
++++++++++++++++++

* Added support to py33 and py34 without using ``2to3``.
* Added testing support to py33 and py34 without using ``2to3``.
* First *Beta Release*.

0.2.1 (2014-07-13)
++++++++++++++++++

* Added --finish option; now ``pda`` is feature-complete.
* Improved coding style for ``control.py`` by removing redundant if-else branches.
* Updated tool description.
* Improved unit test and test automation process.

0.2.0 (2014-07-10)
++++++++++++++++++

* Improved ``pda`` README documentation.

0.1.9.1 (2014-07-06)
++++++++++++++++++++

* Remove installing ``unittest2``, since it's not used at all by ``pda``.

0.1.9 (2014-04-27)
++++++++++++++++++

* Added ``--clear`` option to allow ``pda`` to remove all tasks stored.

0.1.8 (2014-04-26)
++++++++++++++++++

* Improved configuration module for runtime usage.
* Sorted ``pda`` output based on DUE TIME, PRIORITY, LIST TYPE and TASK#.

0.1.7 (2014-04-08)
++++++++++++++++++

* Completed syncing data section in README.rst.

0.1.6 (2014-04-05)
++++++++++++++++++

* Refined README.rst to provide instructions for ``.pdaconfig`` file.

0.1.5 (2014-04-04)
++++++++++++++++++

* Refined README.rst.

0.1.4 (2014-04-01)
++++++++++++++++++

* Fixed broken reStructuredText.

0.1.3 (2014-04-01)
++++++++++++++++++

* Removed unused import PdaConfig.
* Fixed sync_remote_dbstore method bug for transition between local mode and remote mode.
* Fixed max_task_number attribute getter for shelve is empty.

0.1.2 (2014-03-31)
++++++++++++++++++

* Fixed format string bug (#50) to be compatible with python 2.6.

0.1.1 (2014-03-30)
++++++++++++++++++

* Removed debugging assert statements.

0.1.0 (2014-03-30)
++++++++++++++++++

* Birth!
