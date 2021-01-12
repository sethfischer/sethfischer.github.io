==============================
Deploying Drupal 8 with Fabric
==============================

:authors: Seth Fischer
:category: DevOps
:date: 2015-02-06 09:38
:slug: drupal-8-fabric-deploy
:software: Composer: 1.0-dev
:software: Drupal: 8.0.0-beta4
:software: Drush: 7.0-dev
:software: Fabric 1.10.1
:software: Git: 1.7.10.4
:software: Paramiko 1.15.2
:software: PHP: 5.4.36-0+deb7u3
:tags: Drupal 8, Drupal, Fabric, Python
:summary:
    This Drupal 8 article is obsolete.

    An automated build and deployment process saves time and, more
    importantly, provides a safeguard against failed deployments. Fabric is a
    tool that can be used to automate application deployment and related tasks.
    This article describes using Fabric to deploy a Drupal 8 site.


.. warning::

    This Drupal 8 article is obsolete. It was published in February 2015, nine
    months before Drupal 8 was released.


An automated build and deployment process saves time and, more importantly,
provides a safeguard against failed deployments. `Fabric`_ is a tool that can
be used to automate application deployment and related tasks. This article
describes using Fabric to deploy a Drupal 8 site.

Visit `github.com/sethfischer/fabric-deploy`_ for the most recent version of
the fabfile which is an adaptation of `fabric-deploy by halcyonCorsair`_ -- a
fabfile for the deployment of Drupal 7 sites.


.. contents::
    :depth: 2


Drupal project structure
------------------------

The fabfile is designed to deploy a site having a project structure as
described in `A Drupal 8 workflow using the Git subtree merge strategy`_, but
may be easily adapted to accommodate another project structure.


Synchronise site UUID across instances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So that configuration can be shared between instances of the site (development,
staging, production) they must share a common
:abbr:`UUID (Universally unique identifier)`.

.. code-block:: console

    $ drush cget system.site
    uuid: cdd9a662-e53d-0944-be57-8765c04d38f1
    name: example.com
    mail: admin@example.com
    slogan: ''
    page:
      403: ''
      404: ''
      front: node
    admin_compact_mode: false
    weight_select_max: 100
    langcode: en

The site UUID may be edited with the command ``drush cedit system.site``. For
a robust approach to synchronising UUIDs across instances of a site see
`An approach to code-driven development in Drupal 8`_ by `Albert Albala`_.


Exclude files from release tarball
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As an enhancement files can be excluded from the release tarball by including
a ``.gitattributes`` file in the root of the repository and specifying the
`export-ignore attribute`_ for files that should not be included in the
release. Use this
`.gitattributes export-ignore template for Druapl 8 projects`_.


Target host configuration
-------------------------

User account
~~~~~~~~~~~~

The user who executes the deployment must have ssh access to the target host
and permissions to execute commands as both the ``root`` and web server user --
usually ``www-data`` on Debian–based systems.


Directory structure
~~~~~~~~~~~~~~~~~~~

Variable data such as the Drupal ``files/`` directory, ``settings.php``,
and ``services.yml`` is located in ``/var/lib/www/example.com/``.

.. code-block:: console

    $ tree -AF /var/lib/www/example.com/
    /var/lib/www/example.com/
    ├── files/
    ├── services.yml
    └── settings.php

The Drupal site code base is installed in ``/var/www/`` with symlinks to the
variable data being created during deployment.

.. code-block:: console

    $ tree -AFL 4 /var/www/example.com/
    /var/www/example.com/
    ├── current -> /var/www/example.com/releases/tag_x/
    └── releases/
        └── tag_x/
            ├── config/
            │   ├── active/
            │   ├── deploy/
            │   └── staging/
            ├── drupal/
            │   ├── composer.json
            │   ├── core/
            │   ├── example.gitignore
            │   ├── index.php
            │   ├── modules/
            │   ├── profiles/
            │   ├── README.txt
            │   ├── robots.txt
            │   ├── sites/
            │   ├── themes/
            │   └── web.config
            └── README.md

    $ tree -AFL /var/www/example.com/releases/tag_x/drupal/sites/default/
    /var/www/example.com/releases/tag_x/drupal/sites/default/
    ├── files -> /var/lib/www/uat.reptiles.veri.co.nz/files/
    ├── services.yml -> /var/lib/www/uat.reptiles.veri.co.nz/services.yml
    └── settings.php -> /var/lib/www/uat.reptiles.veri.co.nz/settings.php


Dependencies
~~~~~~~~~~~~

The following tools must be installed on the target host:

*   `OpenSSH server`_
*   `Drush`_


Manual configuration
~~~~~~~~~~~~~~~~~~~~

The database, ``settings.php`` and ``services.yml`` must be manually created on
the target host before the first deployment.

Create the database and database user:

.. code-block:: console

    $ ssh host
    $ mysql -uroot -p
    mysql> CREATE DATABASE db;
    mysql> CREATE USER 'dbuser'@'localhost' IDENTIFIED BY 'password';
    mysql> GRANT ALL PRIVILEGES ON db.* TO 'dbuser'@'localhost';
    mysql> FLUSH PRIVILEGES;
    mysql> \q

Copy ``sites/default/settings.php`` and ``sites/default/services.yml`` to the
target host and edit as appropriate according to the environment.

.. code-block:: console

    $ scp settings.php host:/var/lib/www/example.com/settings.php
    $ scp services.yml host:/var/lib/www/example.com/services.yml


Fabfile
-------

Source code is hosted at `github.com/sethfischer/fabric-deploy`_.


Configuration
~~~~~~~~~~~~~

Configuration is expressed via `YAML`_ with one file per project. Below is an
example configuration file.

.. code-block:: yaml

    # example.yml

    # global configuration common to all environments
    _global:
        repository:     ssh+git://github.com/user/repo.git
        build_dir:      /home/tmp/builds
        remote_tmp_dir: /tmp

    # staging environment
    staging:
        hosts:
            - staging.example.com
        remote_tmp_dir: /tmp

    # production environment
    prod:
        hosts:
            - example.com


Available commands
~~~~~~~~~~~~~~~~~~

``fab -f drupal8 -l`` will list the available commands with a short
description:

deploy
    Deploy release
init_deploy
    Deploy initial release
init_host
    Initialise directory structure on target host
site
    Load configuration from YAML file


Usage
~~~~~

Initialise directory structure on the ``uat`` host of ``example.com``:

.. code-block:: console

    $ fab -f drupal8 site:example.com,uat init_host

Deploy ``tag_x`` for ``example.com`` to ``uat``:

.. code-block:: console

    $ fab -f drupal8 site:example.com,uat deploy:tag_x


Source code
~~~~~~~~~~~

For the latest code ``git clone https://github.com/sethfischer/fabric-deploy``
or `create a fork`_.


.. include:: ../static/drupal-8-fabric-deploy/drupal-8-fabric-deploy.py
    :code: python


Further reading
---------------

*   `Drush 7.x commands`_
*   `Fabric’s documentation`_
*   `Drupal core issue: Allow a site to be installed from existing
    configuration`_
*   `Managing configuration in Drupal 8`_


.. _`Fabric`: http://www.fabfile.org/
.. _`github.com/sethfischer/fabric-deploy`: https://github.com/sethfischer/fabric-deploy
.. _`fabric-deploy by halcyonCorsair`: https://github.com/halcyonCorsair/fabric-deploy
.. _`A Drupal 8 workflow using the Git subtree merge strategy`: |filename|/web-development/drupal-8-workflow-using-git-subtree-merge.rst
.. _`An approach to code-driven development in Drupal 8`: http://dcycleproject.org/blog/68/approach-code-driven-development-drupal-8
.. _`Albert Albala`: https://github.com/alberto56/
.. _`export-ignore attribute`: http://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes#Exporting-Your-Repository
.. _`.gitattributes export-ignore template for Druapl 8 projects`: https://gist.github.com/sethfischer/bdda9753837ab1da680a
.. _`OpenSSH server`: https://wiki.debian.org/SSH
.. _`Drush`: http://docs.drush.org/en/master/install/#composer-one-drush-for-all-projects
.. _`YAML`: http://yaml.org/
.. _`create a fork`: https://github.com/sethfischer/fabric-deploy/fork
.. _`Drush 7.x commands`: http://www.drushcommands.com/drush-7x/
.. _`Fabric’s documentation`: http://docs.fabfile.org/en/1.10/
.. _`Drupal core issue: Allow a site to be installed from existing configuration`: https://www.drupal.org/node/1613424
.. _`Managing configuration in Drupal 8`: https://www.drupal.org/documentation/administer/config
