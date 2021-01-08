========================================================
A Drupal 8 workflow using the Git subtree merge strategy
========================================================

:authors: Seth Fischer
:category: Web development
:date: 2015-01-23 19:20
:slug: drupal-8-workflow-using-git-subtree-merge
:tags: Drupal 8, Drupal, Git
:software: Composer: 1.0-dev
:software: Drupal: 8.0.0-beta4
:software: Drush: 7.0-dev
:software: Git: 1.7.10.4
:software: PHP: 5.4.36-0+deb7u3
:summary:
    This Drupal 8 article is obsolete.

    Often there are components of a Drupal website that should not be
    located in the document root such as configuration files. It is convenient
    to keep these files in version control but outside of the Drupal root. By
    utilising Git subtrees, a Drupal installation root may be below the root of
    the main repository, and upstream changes to Drupal core conveniently
    merged with git read-tree.


.. warning::

    This Drupal 8 article is obsolete. It was published in January 2015, eleven
    months before Drupal 8 was released.


Often there are components of a Drupal website that should not be located in
the document root such as configuration files, deployment scripts, and
functional tests. By utilising Git subtrees, a Drupal installation root (or web
server document root) may be below the root of the main repository, and
upstream changes to Drupal core may be conveniently merged with
``git read-tree``.


.. contents::
    :depth: 2


Initialise Git repository
-------------------------

Initialise Git repository and add your ``.gitignore``, ``README``, and
``LICENSE`` files.

.. code-block:: console

    $ mkdir myproject
    $ cd myproject
    $ git init
    Initialized empty Git repository in /var/www/myproject/.git/
    $ vi README.md
    $ git add README.md
    $ git commit -m "Add README.md"
    [master (root-commit) 3a30763] Add README.txt
     1 file changed, 1 insertion(+)
     create mode 100644 README.txt


Add upstream remote
-------------------

Add the drupal.org git repository as a remote with the name ``upstream``. To
improve efficiency specify that only the ``8.0.x`` branch is to be tracked with
the ``-t`` option.

.. code-block:: console

    $ git remote add -t 8.0.x upstream http://git.drupal.org/project/drupal.git
    $ git fetch upstream


Checkout a local copy of the upstream branch
--------------------------------------------

Checkout a local copy of the ``upstream/8.0.x`` branch.

.. code-block:: console

    $ git checkout -b upstream upstream/8.0.x
    Branch upstream set up to track remote branch 8.0.x from upstream by rebasing.
    Switched to a new branch 'upstream'


Pull upstream into a subdirectory in the master branch
------------------------------------------------------

The ``upstream/8.0.x`` branch is pulled in as a subdirectory of the master
branch using the ``git read-tree`` command. The name of the subdirectory is
specified with the ``--prefix`` option; in this case ``drupal/``.

.. code-block:: console

    $ git checkout master
    $ git merge -s ours --no-commit upstream/8.0.x
    Automatic merge went well; stopped before committing as requested
    $ git read-tree --prefix=drupal/ -u upstream/8.0.x
    $ git commit
    [master bd410e7] Merge remote-tracking branch 'upstream/8.0.x'

The upstream branch will now be a subdirectory of the master branch.

.. code-block:: console

    $ tree -L 2
    .
    |-- drupal
    |   |-- composer.json
    |   |-- core
    |   |-- example.gitignore
    |   |-- index.php
    |   |-- modules
    |   |-- profiles
    |   |-- README.txt
    |   |-- robots.txt
    |   |-- sites
    |   |-- themes
    |   ``-- web.config
    ``-- README.md

    6 directories, 7 files


Create a .gitingore for Drupal core
-----------------------------------

Drupal core has an example ``.gitignore`` file which provides an excellent
starting point and is sufficient for most projects.

.. code-block:: console

    $ cp drupal/example.gitignore drupal/.gitignore
    $ git add drupal/.gitignore
    $ git commit -m "Add .gitignore for Drupal core"


Create directories above the document root
------------------------------------------

As the document root is now below the repository root, files and directories
may be committed to the repository without exposing them to the web server.

In this example -- when configuring the web server -- the document root will be
set to ``/var/www/myproject/drupal``.

.. code-block:: console

    $ mkdir -p config/active config/staging config/deploy
    $ tree -L 2
    .
    |-- config
    |   |-- active
    |   |-- deploy
    |   ``-- staging
    |-- drupal
    |   |-- composer.json
    |   |-- core
    |   |-- example.gitignore
    |   |-- index.php
    |   |-- modules
    |   |-- profiles
    |   |-- README.txt
    |   |-- robots.txt
    |   |-- sites
    |   |-- themes
    |   ``-- web.config
    ``-- README.md

    9 directories, 7 files


Create the files directory and set permissions
----------------------------------------------

The Drupal ``files`` directory must be manually created.

.. code-block:: console

    $ mkdir drupal/sites/default/files

To work efficiently with drush the files in ``sites/default/files`` should be
writeable both by the web server and command-line user. An alternative to
``chmod -R 777 sites/default/files`` is to use `Access Control Lists`_.

.. code-block:: console

    $ HTTPDUSER=``ps aux | grep -E '[a]pache|[h]ttpd|[_]www|[w]ww-data|[n]ginx' | \
    grep -v root | head -1 | cut -d\  -f1``
    $ sudo setfacl -R -m u:"$HTTPDUSER":rwX -m u:`whoami`:rwX drupal/sites/default/files
    $ sudo setfacl -dR -m u:"$HTTPDUSER":rwX -m u:`whoami`:rwX drupal/sites/default/files

``HTTPDUSER`` is usually ``www-data`` on Debian-based distributions.

It may be convenient to add similar ACL permissions to the ``config/active``,
``config/staging``, and ``config/deploy`` directories.


Create database
---------------

.. code-block:: console

    $ mysql -uroot -p
    mysql> CREATE DATABASE db;
    mysql> CREATE USER 'dbuser'@'localhost' IDENTIFIED BY 'password';
    mysql> GRANT ALL PRIVILEGES ON db.* TO 'dbuser'@'localhost';
    mysql> FLUSH PRIVILEGES;
    mysql> \q


Site installation
-----------------

Install the site with the standard install profile and change the admin
password.

.. code-block:: console

    $ cd drupal
    $ drush site-install standard --db-url=mysql://dbuser:password@localhost/db \
    --site-name=drupal8
    $ drush upwd admin --password=password


Drupal configuration directories
--------------------------------

Edit ``sites/default/settings.php`` and update the location of the
configuration directories.

.. code-block:: php

   <?php

   // Default config directories provided by the installer.
   $config_directories['active'] = '../config/active';
   $config_directories['staging'] = '../config/staging';

   // Config directory used for deployments.
   $config_directories['deploy'] = '../config/deploy';


Export configuration
--------------------

Export the configuration from the database into the ``deploy`` configuration
directory.

.. code-block:: console

    $ cd drupal/
    $ drush config-export deploy
    Configuration successfully exported to ../config/deploy.             [success]

Once exported, this configuration may be committed to the Git repository. As
part of the deployment process the configuration may be imported with the
command ``drush config-import deploy``.


Update Drupal core
------------------

To merge upstream change to Drupal core the `Git subtree merge strategy`_ is
used.

.. code-block:: console

    $ git pull -s subtree upstream 8.0.x

The above command will merge the history of ``upstream`` with the main
repository. If it is not preferable to merge histories the ``--squash`` and
``--no-commit`` options can be used along with the ``-s subtree`` strategy
option:

.. code-block:: console

    $ git checkout master
    $ git merge --squash -s subtree --no-commit upstream
    Squash commit -- not updating HEAD
    Automatic merge went well; stopped before committing as requested

Remember to rebuild the cache after each merge:

.. code-block:: console

    $ drush cache-rebuild


Further reading
---------------

*   `Git Tools - Subtree Merging`_
*   `How to use the subtree merge strategy`_
*   `Deploying Drupal 8 with Fabric`_

.. _`Composer template for Drupal projects`: https://github.com/drupal-composer/drupal-project
.. _`Access Control Lists`: https://wiki.debian.org/Permissions#Access_Control_Lists_in_Linux
.. _`Git subtree merge strategy`: http://git-scm.com/book/en/v1/Git-Tools-Subtree-Merging
.. _`Git Tools - Subtree Merging`: http://git-scm.com/book/en/v1/Git-Tools-Subtree-Merging
.. _`How to use the subtree merge strategy`: https://www.kernel.org/pub/software/scm/git/docs/howto/using-merge-subtree.html
.. _`Deploying Drupal 8 with Fabric`: |filename|/devops/drupal-8-fabric-deploy.rst
