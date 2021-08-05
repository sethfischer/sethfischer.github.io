==================================================
Include a Git revision in firmware with PlatformIO
==================================================

:authors: Seth Fischer
:category: Mechatronics
:date: 2021-05-20 22:16
:slug: platformio-git-revision-in-firmware
:status: published
:tags: Arduino, Git, PlatformIO, Python
:summary: How to include a Git revision in constant your firmware at build time
    with PlatformIO.


How to include a Git revision in your firmware at build time with `PlatformIO`_.

.. contents::
    :depth: 2

.. note::

    This article is a comprehensive write up of two PlatformIO issues I
    responded to on GitHub.com in late 2020:

    * `platformio/platformio-core/issues/3698`_
    * `platformio/platformio-core/issues/3759`_


PlatformIO supports the generation of `dynamic build flags`_. This feature
allows the creation of build flags by executing a user defined script. The
script should output one or more gcc ``-D`` options to standard output. For
example::

-D SRC_REVISION="b4837070c4b10d37acfbf0283b758d38e739a670"


The ``-D`` option allows the defination of a macro. From the `gcc(1) man page`_:

    \-D name
        Predefine name as a macro, with definition 1.

    -D name=definition
        The contents of definition are tokenized and processed as if they
        appeared during translation phase three in a #define directive. In
        particular, the definition will be truncated by embedded newline
        characters. 


Project structure
-----------------

This example uses a typical PlatformIO project structure:

.. raw:: html

    <pre class="literal">
    .
    ├── src
    │   └── main.cpp
    ├── define-git-revision.py
    └── platformio.ini
    </pre>


Configuration file
------------------

The script to run is defined by the ``build_flags`` option in
``platformio.ini``. Scripts are indicated by prepending them with a ``!``.

.. include:: ../static/platformio-git-revision-in-firmware/platformio.ini
    :code: ini

`Download platformio.ini`_.


User defined script
-------------------

The following Python script ``define-git-revision.py`` will set two predefined
macros:

1.  ``SRC_REVISION`` containing the Git revision, for example
    ``97c333a4b3c732523e09742318d7acc52b33dbcc``, and
2.  ``SRC_STATE`` defining the state of the working tree as either ``clean`` or
    ``dirty``.

.. include:: ../static/platformio-git-revision-in-firmware/define-git-revision.py
    :code: python

`Download define-git-revision.py`_.


Main.cpp
--------

The predefined macros may be used in ``src/main.cpp`` as follows:

.. include:: ../static/platformio-git-revision-in-firmware/main.cpp
    :code: cpp

`Download main.cpp`_.


Output
------

Example output on the PlatformIO device monitor::

    > Executing task: platformio device monitor <

    --- Available filters and text transformations: colorize, debug, default, direct, esp32_exception_decoder, hexlify, log2file, nocontrol, printable, send_on_enter, time
    --- More details at http://bit.ly/pio-monitor-filters
    --- Miniterm on /dev/ttyUSB0  115200,8,N,1 ---
    --- Quit: Ctrl+C | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H ---
    b4837070c4b10d37acfbf0283b758d38e739a670
    dirty

    b4837070c4b10d37acfbf0283b758d38e739a670
    dirty


.. _`PlatformIO`: https://platformio.org/
.. _`platformio/platformio-core/issues/3698`: https://github.com/platformio/platformio-core/issues/3698#issuecomment-704672408
.. _`platformio/platformio-core/issues/3759`: https://github.com/platformio/platformio-core/issues/3759#issuecomment-740188206
.. _`dynamic build flags`: https://docs.platformio.org/en/latest/projectconf/section_env_build.html#dynamic-build-flags
.. _`gcc(1) man page`: https://linux.die.net/man/1/gcc
.. _`Download platformio.ini`: {static}/static/platformio-git-revision-in-firmware/platformio.ini
.. _`Download define-git-revision.py`: {static}/static/platformio-git-revision-in-firmware/define-git-revision.py
.. _`Download main.cpp`: {static}/static/platformio-git-revision-in-firmware/main.cpp
