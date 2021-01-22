===============
seth.fischer.nz
===============

|test-status| |link-check|


.. code-block:: text

    virtualenv .venv
    . .venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt
    pelican-themes -i ~/path/to/alexandrevicenzi/Flex
    make devserver

Built with `Pelican`_.


.. _`Pelican`: http://getpelican.com/


.. |test-status| image:: https://github.com/sethfischer/sethfischer.github.io/workflows/test/badge.svg
    :target: https://github.com/sethfischer/sethfischer.github.io/actions?query=workflow%3Atest
    :alt: Test status

.. |link-check| image:: https://github.com/sethfischer/sethfischer.github.io/workflows/link%20check/badge.svg
    :target: https://github.com/sethfischer/sethfischer.github.io/actions?query=workflow%3A%22link+check%22
    :alt: Link check status
