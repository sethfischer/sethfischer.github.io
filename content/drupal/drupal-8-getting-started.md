Title: Getting started with Drupal 8
Date: 2014-11-28 22:22
Modified: 2014-11-29 20:33
Category: Drupal
Tags: Drupal 8, Drupal
Slug: drupal-8-getting-started
Authors: Seth Fischer
Software: Composer: 1.0-dev
Software: Drupal: 8.0.0-beta3
Software: Drush: 7.0-dev
Software: Git: 1.7.10.4
Software: PHP: 5.4.35-0+deb7u2
Summary: Now that Drupal 8 is in beta phase it is a great time for site
    developers to start exploring the API. This article serves as an
    introduction to installing and configuring Drupal 8 using Git and Drush.


Now that [Drupal 8][1] is in beta phase it is time for site developers to start
exploring the API. This article describes the installation and configuration of
Drupal 8 using Git and Drush. Bear in mind that as of 2014-11-28 there were 22
[issues tagged with D8 upgrade path][2], so it may be necessary to rebuild your
site with the next core update.


[TOC]


## Before starting

  * set-up a [LAMP][3] or LNMP stack conforming with the
    [Drupal 8 system requirements][4]
  * [install git][5]
  * [install Composer][6]
  * using composer, [install Drush 7.x (dev)][7]


## Clone Drupal 8

    :::console
    $ git clone -b 8.0.x --single-branch http://git.drupal.org/project/drupal.git
    $ git remote rename origin upstream
    $ git remote add origin [url]
    $ git checkout -b master
    $ cp example.gitignore .gitignore


## Create the files directory and set permissions

    :::console
    $ mkdir sites/default/files

To work efficiently with drush the files in `sites/default/files` should be
writeable both by the web server and command line user. An alternative to
`chmod -R 777 sites/default/files` is to use [Access Control Lists][8].

Those familiar with the Symfony 2 documentation will recognise the following
shell commands which have been adapted from the
[Installing and Configuring Symfony][9] chapter of the The Symfony Book.

    :::console
    $ HTTPDUSER=`ps aux | grep -E '[a]pache|[h]ttpd|[_]www|[w]ww-data|[n]ginx' | grep -v root | head -1 | cut -d\  -f1`
    $ sudo setfacl -R -m u:"$HTTPDUSER":rwX -m u:`whoami`:rwX sites/default/files
    $ sudo setfacl -dR -m u:"$HTTPDUSER":rwX -m u:`whoami`:rwX sites/default/files

`HTTPDUSER` is usually `www-data` on Debian-based distributions.

Before setting the access control only the drush user will have `rw` permissions:

    :::console
    $ getfacl sites/default/files
    # file: cache
    # owner: drushuser
    # group: drushuser
    user::rwx
    group::rwx
    other::rwx

After setting the access control both the web server user and drush user will
have `rw` permissions:

    :::console
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


## Create database

    :::console
    $ mysql -uroot -p
    mysql> CREATE DATABASE db;
    mysql> CREATE USER 'dbuser'@'localhost' IDENTIFIED BY 'password';
    mysql> GRANT ALL PRIVILEGES ON db.* TO 'dbuser'@'localhost';
    mysql> FLUSH PRIVILEGES;
    mysql> \q


## Site installation

    :::console
    $ drush site-install standard --db-url=mysql://dbuser:password@localhost/db --site-name=drupal8
    $ drush upwd admin --password=password

Drupal 8 beta is now configured and you may login with the username "admin" and
password "password".


## Configure a Drush alias

    :::console
    $ cp ~/.composer/vendor/drush/drush/examples/example.aliases.drushrc.php ~/.drush/aliases.drushrc.php
    $ drush site-alias @self --full --with-optional >> ~/.drush/aliases.drushrc.php

Edit `~/.drush/aliases.drushrc.php` and enter your site's URI.

    :::php
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

    :::console
    $ drush @drupal8 core-requirements

Check the status of the site installation by running `drush @drupal8 status`.
The output will be similar to the following:

    :::console
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


## Install contrib modules

Two useful modules for developers are [devel][10] and [examples][11].

### Devel

    :::console
    $ drush @drupal8 pm-download devel
    $ drush @drupal8 pm-enable devel

### Examples

    :::console
    $ drush @drupal8 pm-download examples
    $ drush @drupal8 pm-enable examples

The single command `drush @drupal8 pm-enable module` will download module (if
required) before enabling it.


## Regularly update Drupal core

As Drupal 8 pushes on through beta releases you should regularly merge in the
latest code:

    :::console
    (master)$ git checkout master
    (master)$ git fetch upstream
    (master)$ git merge upstream/8.0.x

Remember to rebuild the site after each merge:

    :::console
    $ drush cache-rebuild

Before all issues tagged with "D8 upgrade path" have been closed you may find
that you are required to repeat the site installation commands as described
above after updating Drupal core.


## Further reading

  * [Building a Drupal site with Git][12]
  * [Git Reference][13]


*[LAMP]: Linux, Apache, MySQL, PHP
*[LNMP]: Linux, nginx, MySQL, PHP

[1]: https://www.drupal.org/drupal-8.0
[2]: https://www.drupal.org/project/issues/search/drupal?project_issue_followers=&status%5B%5D=1&status%5B%5D=13&status%5B%5D=8&status%5B%5D=14&status%5B%5D=15&status%5B%5D=4&priorities%5B%5D=400&categories%5B%5D=1&categories%5B%5D=2&version%5B%5D=8.x&issue_tags_op=%3D&issue_tags=D8+upgrade+path
[3]: https://wiki.debian.org/LaMp "Setting up a LAMP stack on Debian"
[4]: https://api.drupal.org/api/drupal/core!INSTALL.txt/8 "Drupal 8 INSTALL.txt"
[5]: http://git-scm.com/book/en/v2/Getting-Started-Installing-Git "Installing Git"
[6]: https://getcomposer.org/doc/00-intro.md#installation-nix "Install Composer on Unix type systems"
[7]: https://github.com/drush-ops/drush#installupdate---composer "How to install Drush 7.x (dev)"
[8]: https://wiki.debian.org/Permissions#Access_Control_Lists_in_Linux "Access Control Lists in Linux"
[9]: http://Symfony.com/doc/2.3/book/installation.html#configuration-and-set-up
[10]: https://www.drupal.org/project/devel
[11]: https://www.drupal.org/project/examples
[12]: https://www.drupal.org/node/803746
[13]: http://gitref.org/


