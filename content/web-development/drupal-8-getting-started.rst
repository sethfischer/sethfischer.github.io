=============================
Getting started with Drupal 8
=============================

:authors: Seth Fischer
:category: Web development
:date: 2014-11-28 22:22
:slug: drupal-8-getting-started
:software: Composer: 1.0-dev
:software: Drupal: 8.0.0-beta3
:software: Drush: 7.0-dev
:software: Git: 1.7.10.4
:software: PHP: 5.4.35-0+deb7u2
:tags: Drupal 8, Drupal
:summary:
    This Drupal 8 article is obsolete.

    Now that Drupal 8 is in beta phase it is a great time for site
    developers to start exploring the API. This article serves as an
    introduction to installing and configuring Drupal 8 using Git and Drush.


.. warning::

    This Drupal 8 article is obsolete. It was published in November 2014, 12 months
    before Drupal 8 was released.


Now that `Drupal 8`_ is in beta phase it is time for site developers to start
exploring the API. This article describes the installation and configuration of
Drupal 8 using Git and Drush. Bear in mind that as of 2014-11-28 there were 22
`issues tagged with D8 upgrade path`_, so it may be necessary to rebuild your
site with the next core update.


.. contents::
    :depth: 2


Before starting
---------------

*   set-up a :abbr:`LAMP (Linux, Apache, MySQL, PHP)` or
    :abbr:`LNMP (Linux, nginx, MySQL, PHP)` stack conforming with the
    `Drupal 8 system requirements`_
*   `install git`_
*   `install Composer`_
*   using composer, `install Drush 7.x (dev)`_


Clone Drupal 8
--------------

.. code-block:: console

    :::console
    $ git clone -b 8.0.x --single-branch http://git.drupal.org/project/drupal.git
    $ git remote rename origin upstream
    $ git remote add origin [url]
    $ git checkout -b master
    $ cp example.gitignore .gitignore


Create the files directory and set permissions
----------------------------------------------

.. code-block:: console

    $ mkdir sites/default/files

To work efficiently with drush the files in ``sites/default/files`` should be
writeable both by the web server and command line user. An alternative to
``chmod -R 777 sites/default/files`` is to use `Access Control Lists`_.

Those familiar with the Symfony 2 documentation will recognise the following
shell commands which have been adapted from the
`Installing and Configuring Symfony`_ chapter of the The Symfony Book.

.. code-block:: console

    $ HTTPDUSER=`ps aux | grep -E '[a]pache|[h]ttpd|[_]www|[w]ww-data|[n]ginx' | grep -v root | head -1 | cut -d\  -f1`
    $ sudo setfacl -R -m u:"$HTTPDUSER":rwX -m u:`whoami`:rwX sites/default/files
    $ sudo setfacl -dR -m u:"$HTTPDUSER":rwX -m u:`whoami`:rwX sites/default/files

``HTTPDUSER`` is usually ``www-data`` on Debian-based distributions.

Before setting the access control only the drush user will have ``rw``
permissions:

.. code-block:: console

    $ getfacl sites/default/files
    # file: cache
    # owner: drushuser
    # group: drushuser
    user::rwx
    group::rwx
    other::rwx

After setting the access control both the web server user and drush user will
have ``rw`` permissions:

.. code-block:: console

    $ getfacl sites/default/files
    # file: cache
    # owner: drushuser
    # group: drushuser
    user::rwx
    user:www-data:rwx
    user:drushuser:rwx
    group::rwx
    mask::rwx
    other::rwx
    default:user::rwx
    default:user:www-data:rwx
    default:user:drushuser:rwx
    default:group::rwx
    default:mask::rwx
    default:other::rwx


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

.. code-block:: console

    $ drush site-install standard --db-url=mysql://dbuser:password@localhost/db --site-name=drupal8
    $ drush upwd admin --password=password

Drupal 8 beta is now configured and you may login with the username “admin” and
password “password”.


Configure a Drush alias
-----------------------

.. code-block:: console

    $ cp ~/.composer/vendor/drush/drush/examples/example.aliases.drushrc.php ~/.drush/aliases.drushrc.php
    $ drush site-alias @self --full --with-optional >> ~/.drush/aliases.drushrc.php

Edit ``~/.drush/aliases.drushrc.php`` and enter your site’s URI.

.. code-block:: php

    <?php
    /**
     * Drupal 8 beta
     */
    $aliases["drupal8"] = array (
      'root' => '/var/www/drupal8',
      'uri' => 'http://drupal8',
      '#name' => 'drupal8',
      'path-aliases' =>
      array (
        '%drush' => '/home/seth/.composer/vendor/drush/drush',
        '%site' => 'sites/default/',
      ),
    );

Check that your system meets the minimum core requirements:

.. code-block:: console

    $ drush @drupal8 core-requirements

Check the status of the site installation by running ``drush @drupal8 status``.
The output will be similar to the following:

.. code-block:: console

    $ drush @drupal8 status
     Drupal version         :  8.0.0-dev
     Site URI               :  http://drupal8
     Database driver        :  mysql
     Database hostname      :  localhost
     Database port          :
     Database username      :  drupal8
     Database name          :  drupal8
     Database               :  Connected
     Drupal bootstrap       :  Successful
     Drupal user            :  Anonymous
     Default theme          :  bartik
     Administration theme   :  seven
     PHP executable         :  /usr/bin/php
     PHP configuration      :  /etc/php5/cli/php.ini
     PHP OS                 :  Linux
     Drush version          :  7.0-dev
     Drush temp directory   :  /tmp
     Drush configuration    :
     Drush alias files      :  /home/user/.drush/aliases.drushrc.php
     Drupal root            :  /var/www/drupal8
     Site path              :  sites/default
     File directory path    :  sites/default/files
     Temporary file         :  /tmp
     directory path
     Active config path     :  sites/default/files/config_jP-uX_4rcMWllW18FM124krsM
                               An44d1rdD2t5zXZLAaQcrXQjUATnoTTQ5gtw-iH5fqcmlTFCQ/ac
                               tive
     Staging config path    :  sites/default/files/config_jP-uX_4rcMWllW18FM124krsM
                               An44d1rdD2t5zXZLAaQcrXQjUATnoTTQ5gtw-iH5fqcmlTFCQ/st
                               aging


Install contrib modules
-----------------------

Two useful modules for developers are `devel`_ and `examples`_.


Devel
~~~~~

.. code-block:: console

    $ drush @drupal8 pm-download devel
    $ drush @drupal8 pm-enable devel


Examples
~~~~~~~~

.. code-block:: console

    $ drush @drupal8 pm-download examples
    $ drush @drupal8 pm-enable examples

The single command ``drush @drupal8 pm-enable module`` will download module
(if required) before enabling it.


Regularly update Drupal core
----------------------------

As Drupal 8 pushes on through beta releases you should regularly merge in the
latest code:

.. code-block:: console

    (master)$ git checkout master
    (master)$ git fetch upstream
    (master)$ git merge upstream/8.0.x

Remember to rebuild the site after each merge:

.. code-block:: console

    $ drush cache-rebuild

Before all issues tagged with “D8 upgrade path” have been closed you may find
that you are required to repeat the site installation commands as described
above after updating Drupal core.


Further reading
---------------

*   `Building a Drupal site with Git`_
*   `Git Reference`_


.. _`Composer template for Drupal projects`: https://github.com/drupal-composer/drupal-project
.. _`Drupal 8`: https://www.drupal.org/drupal-8.0
.. _`issues tagged with D8 upgrade path`: https://www.drupal.org/project/issues/search/drupal?project_issue_followers=&status%5B%5D=1&status%5B%5D=13&status%5B%5D=8&status%5B%5D=14&status%5B%5D=15&status%5B%5D=4&priorities%5B%5D=400&categories%5B%5D=1&categories%5B%5D=2&version%5B%5D=8.x&issue_tags_op=%3D&issue_tags=D8+upgrade+path
.. _`Drupal 8 system requirements`: https://api.drupal.org/api/drupal/core!INSTALL.txt/8
.. _`install git`: http://git-scm.com/book/en/v2/Getting-Started-Installing-Git
.. _`install Composer`: https://getcomposer.org/doc/00-intro.md#installation-nix
.. _`install Drush 7.x (dev)`: https://github.com/drush-ops/drush#installupdate---composer
.. _`Access Control Lists`: https://wiki.debian.org/Permissions#Access_Control_Lists_in_Linux
.. _`Installing and Configuring Symfony`: http://Symfony.com/doc/2.3/book/installation.html#configuration-and-set-up
.. _`devel`: https://www.drupal.org/project/devel
.. _`examples`: https://www.drupal.org/project/examples
.. _`Building a Drupal site with Git`: https://www.drupal.org/node/803746
.. _`Git Reference`: http://gitref.org/
