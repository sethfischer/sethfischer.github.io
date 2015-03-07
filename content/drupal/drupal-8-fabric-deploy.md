Title: Deploying Drupal 8 with Fabric
Date: 2015-02-06 09:38
Category: Drupal
Tags: Drupal 8, Drupal, Fabric, Python
Slug: drupal-8-fabric-deploy
Authors: Seth Fischer
Software: Composer: 1.0-dev
Software: Drupal: 8.0.0-beta4
Software: Drush: 7.0-dev
Software: Git: 1.7.10.4
Software: PHP: 5.4.36-0+deb7u3
Software: Fabric 1.10.1
Software: Paramiko 1.15.2
Summary: An automated build and deployment process saves time and, more
    importantly, provides a safeguard against failed deployments. Fabric is a
    tool that can be used to automate application deployment and related tasks.
    This article describes using Fabric to deploy a Drupal 8 site.


An automated build and deployment process saves time and, more importantly,
provides a safeguard against failed deployments. [Fabric][1] is a tool that can
be used to automate application deployment and related tasks. This article
describes using Fabric to deploy a Drupal&nbsp;8 site.

Visit [github.com/sethfischer/fabric-deploy][2] for the most recent version of
the fabfile which is an adaptation of [fabric-deploy by halcyonCorsair][3] — a
fabfile for the deployment of Drupal&nbsp;7 sites.


[TOC]


## Drupal project structure

The fabfile is designed to deploy a site having a project structure as
described in [A Drupal&nbsp;8 workflow using the Git subtree merge strategy][4],
but may be easily adapted to accommodate another project structure.


### Synchronise site UUID across instances

So that configuration can be shared between instances of the site (development,
staging, production) they must share a common UUID.

    :::console
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

The site UUID may be edited with the command `drush cedit system.site`. For a
robust approach to synchronising UUIDs across instances of a site see
[An approach to code-driven development in Drupal 8][5] by [Albert Albala][6].


### Exclude files from release tarball

As an enhancement files can be excluded from the release tarball by including a
`.gitattributes` file in the root of the repository and specifying the
[export-ignore attribute][7] for files that should not be included in the
release. Use this
[.gitattributes export-ignore template for Druapl&nbsp;8 projects][8].


## Target host configuration


### User account

The user who executes the deployment must have ssh access to the target host
and permissions to execute commands as both the `root` and web server user —
usually `www-data` on Debian–based systems.


### Directory structure

Variable data such as the Drupal `files/` directory, `settings.php`, and
`services.yml` is located in `/var/lib/www/example.com/`.

    :::console
    $ tree -AF /var/lib/www/example.com/
    /var/lib/www/example.com/
    ├── files/
    ├── services.yml
    └── settings.php


The Drupal site code base is installed in `/var/www/` with symlinks to the
variable data being created during deployment.

    :::console
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


### Dependencies

The following tools must be installed on the target host:

  * [OpenSSH server][9]
  * [Drush][10]


### Manual configuration

The database, `settings.php` and `services.yml` must be manually created on the
target host before the first deployment.

Create the database and database user:

    :::console
    $ ssh host
    $ mysql -uroot -p
    mysql> CREATE DATABASE db;
    mysql> CREATE USER 'dbuser'@'localhost' IDENTIFIED BY 'password';
    mysql> GRANT ALL PRIVILEGES ON db.* TO 'dbuser'@'localhost';
    mysql> FLUSH PRIVILEGES;
    mysql> \q

Copy `sites/default/settings.php` and `sites/default/services.yml`to the target
host and edit as appropriate according to the environment.

    :::console
    $ scp settings.php host:/var/lib/www/example.com/settings.php
    $ scp services.yml host:/var/lib/www/example.com/services.yml


## Fabfile

Source code is hosted at [github.com/sethfischer/fabric-deploy][2].


### Configuration

Configuration is expressed via [YAML][11] with one file per project. Below is an
example configuration file.


    :::yaml
    % example.yml

    % global configuration common to all environments
    _global:
        repository:     ssh+git://github.com/user/repo.git
        build_dir:      /home/tmp/builds
        remote_tmp_dir: /tmp

    % staging environment
    staging:
        hosts:
            - staging.example.com
        remote_tmp_dir: /tmp

    % production environment
    prod:
        hosts:
            - example.com


### Available commands

`fab -f drupal8 -l` will list the available commands with a short description:

deploy
:   Deploy release

init_deploy
:   Deploy initial release

init_host
:   Initialise directory structure on target host

site
:   Load configuration from YAML file


### Usage

Initialise directory structure on the `uat` host of `example.com`:

    :::console
    $ fab -f drupal8 site:example.com,uat init_host

Deploy `tag_x` for `example.com` to `uat`:

    :::console
    $ fab -f drupal8 site:example.com,uat deploy:tag_x


### Source code

For the latest code `git clone https://github.com/sethfischer/fabric-deploy` or
[create a fork][12].

    :::python
    # -*- coding: utf-8 -*-
    """Fabric deploy for Drupal 8
    
    https://github.com/sethfischer/fabric-deploy
    """
    
    import os
    
    from fabric.api import env, lcd, local, put, run, runs_once, settings, sudo, \
        task
    from fabric.colors import red
    from fabric.utils import abort, warn
    import yaml
    
    
    @task
    @runs_once
    def site(site_name, tier):
        """Load configuration from YAML file
        :param site_name: Site name
        :type site_name: str
        :param tier: Staging tier
        :type tier: str
        """
        env.site_name = site_name
        env.tier = tier
    
        site_config_filename = 'config/{site_name}.yml'.format(**env)
    
        try:
            site_config_file = open(site_config_filename, 'r')
        except IOError:
            abort('Unable to read {site_config_filename}'.format(
                site_config_filename=site_config_filename))
        else:
            site_config_data = yaml.safe_load(site_config_file)
            site_config_file.close()
    
            global_config_data = site_config_data['_global']
            env.update(global_config_data)
    
            tier_config_data = site_config_data[tier]
            env.update(tier_config_data)
    
            env.site_build_dir = os.path.join(env.build_dir, env.site_name)
            env.site_repo_dir = os.path.join(env.site_build_dir, 'repo')
            env.tar_basename = '{site_name}.tar'.format(**env)
            env.tar_gz_basename = '{tar_basename}.gz'.format(**env)
            env.tar_pathname = os.path.join(
                env.site_build_dir, env.tar_basename)
            env.tar_gz_pathname = os.path.join(
                env.site_build_dir, env.tar_gz_basename)
    
    
    @task
    def init_host():
        """Initialise directory structure on target host"""
        project_dir = '/var/www/{host}'.format(**env)
        release_dir = '{project_dir}/releases'.format(project_dir=project_dir)
        data_dir = '/var/lib/www/{host}'.format(**env)
    
        sudo('mkdir -p {release_dir}/'.format(release_dir=release_dir))
        sudo('chown -R www-data:www-data {project_dir}'.format(
            project_dir=project_dir))
    
        sudo('mkdir -p {data_dir}/files'.format(data_dir=data_dir))
        sudo('chown -R www-data:www-data {data_dir}'.format(data_dir=data_dir))
    
        warn('Database must be manually created.')
        warn('{data_dir}/settings.php must be manually created.'.format(
            data_dir=data_dir))
        warn('{data_dir}/services.yml must be manually created.'.format(
            data_dir=data_dir))
    
    
    @task
    def init_deploy(tag):
        """Deploy initial release
        :param tag: Git tags from which to build release
        :type tag: str
        """
        build_exists(tag)
        build(tag)
        upload()
        extract()
        symlink_settings()
        symlink_release()
        run_drush('state-set system.maintenance 1')
        run_drush('config-import deploy')
        run_drush('updatedb')
        run_drush('cache-rebuild')
        run_drush('state-set system.maintenance 0')
    
    
    @task
    def deploy(tag):
        """Deploy release
        :param tag: Git tags from which to build release
        :type tag: str
        """
        build_exists(tag)
        build(tag)
        upload()
        extract()
        run_drush('state-set system.maintenance 1')
        symlink_settings()
        symlink_release()
        run_drush('config-import deploy')
        run_drush('updatedb')
        run_drush('cache-rebuild')
        run_drush('state-set system.maintenance 0')
    
    
    def make_dirs(directory):
        """Create directories recursively
        :param directory: Directory to be created
        :type directory: str
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    
    def build_exists(tag):
        """Test if release has previously been deployed
        :param tag: Git tags from which to build release
        :type tag: str
        """
        project_dir = '/var/www/{host}'.format(**env)
        release_dir = '{project_dir}/releases'.format(project_dir=project_dir)
    
        with settings(warn_only=True):
            result = run('! test -d {release_dir}/{tag}'.format(
                release_dir=release_dir, tag=tag))
            if result.failed:
                abort(red('Release has previously been deployed.'))
    
    
    @runs_once
    def build(tag):
        """Build release tarball
        :param tag: Git tags from which to build release
        :type tag: str
        """
        env.release_tag = tag
    
        make_dirs(env.site_repo_dir)
    
        with lcd(env.site_repo_dir):
            with settings(warn_only=True):
                inside_work_tree = local('git rev-parse --is-inside-work-tree')
    
            if inside_work_tree.failed:
                local('git clone {repository} .'.format(**env))
    
            if local('git pull').succeeded:
                local(('git archive '
                       '--format=tar '
                       '--output={tar_pathname} '
                       '--prefix={release_tag}/ '
                       '{release_tag}').format(**env))
                local('gzip --force -9 {tar_pathname}'.format(**env))
    
    
    def upload():
        """Copy tarball to target host"""
        put(env.tar_gz_pathname, env.remote_tmp_dir)
    
    
    def extract():
        """Extract tarball into release directory"""
        project_dir = '/var/www/{host}'.format(**env)
        release_dir = '{project_dir}/releases'.format(project_dir=project_dir)
    
        with settings(sudo_user='www-data'):
            tar_cmd = ('tar '
                       '--gzip '
                       '--extract '
                       '--verbose '
                       '--file {remote_tmp_dir}/{tar_gz_basename} '
                       '--directory {release_dir}/')
            sudo(tar_cmd.format(
                remote_tmp_dir=env.remote_tmp_dir,
                tar_gz_basename=env.tar_gz_basename,
                release_dir=release_dir))
    
        run('rm {remote_tmp_dir}/{tar_gz_basename}'.format(**env))
    
    
    def symlink_settings():
        """Symlink configuration files and variable data"""
        project_dir = '/var/www/{host}'.format(**env)
        release_dir = '{project_dir}/releases'.format(project_dir=project_dir)
        sites_default = '{release_dir}/{release_tag}/drupal/sites/default'.format(
            release_dir=release_dir,
            release_tag=env.release_tag)
        data_dir = '/var/lib/www/{host}'.format(**env)
    
        with settings(sudo_user='www-data'):
            files_target = '{data_dir}/files'.format(data_dir=data_dir)
            files_dir = '{sites_default}/files'.format(sites_default=sites_default)
    
            sudo('ln -nfs {files_target} {files_dir}'.format(
                files_target=files_target,
                files_dir=files_dir))
    
            settings_target = '{data_dir}/settings.php'.format(data_dir=data_dir)
            settings_file = '{sites_default}/settings.php'.format(
                sites_default=sites_default)
    
            sudo('ln -nfs {settings_target} {settings_file}'.format(
                settings_target=settings_target,
                settings_file=settings_file))
    
            services_target = '{data_dir}/services.yml'.format(data_dir=data_dir)
            services_file = '{sites_default}/services.yml'.format(
                sites_default=sites_default)
    
            sudo('ln -nfs {services_target} {services_file}'.format(
                services_target=services_target,
                services_file=services_file))
    
        sudo('chown www-data:www-data {settings_target}'.format(
            settings_target=settings_target))
        sudo('chmod 0400 {settings_target}'.format(
            settings_target=settings_target))
    
        sudo('chown www-data:www-data {services_target}'.format(
            services_target=services_target))
        sudo('chmod 0400 {services_target}'.format(
            services_target=services_target))
    
    
    def symlink_release():
        """Symlink release"""
        release_dir = '/var/www/{host}/releases/{release_tag}'.format(**env)
        current = '/var/www/{host}/current'.format(**env)
        with settings(sudo_user='www-data'):
            sudo('ln -nfs {release_dir} {current}'.format(
                release_dir=release_dir,
                current=current))
    
    
    def run_drush(command):
        """Run a Drush command
        :param command: Drush command to run
        :type command: str
        """
        with settings(sudo_user='www-data'):
            sudo('drush -u 1 -y -r {drupal_root} {command}'.format(
                drupal_root='/var/www/{host}/current/drupal'.format(**env),
                command=command))



## Further reading

  * [Drush 7.x commands][13]
  * [Fabric’s documentation][14]
  * [Drupal core issue: Allow a site to be installed from existing configuration][15]
  * [Managing configuration in Drupal 8][16]


*[UUID]: Universally unique identifier


[1]: http://www.fabfile.org/
[2]: https://github.com/sethfischer/fabric-deploy
[3]: https://github.com/halcyonCorsair/fabric-deploy
[4]: |filename|drupal-8-workflow-using-git-subtree-merging.md
[5]: http://dcycleproject.org/blog/68/approach-code-driven-development-drupal-8
[6]: https://github.com/alberto56/
[7]: http://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes#Exporting-Your-Repository
[8]: https://gist.github.com/sethfischer/bdda9753837ab1da680a
[9]: https://wiki.debian.org/SSH
[10]: http://docs.drush.org/en/master/install/#composer-one-drush-for-all-projects
[11]: http://yaml.org/
[12]: https://github.com/sethfischer/fabric-deploy/fork
[13]: http://www.drushcommands.com/drush-7x/
[14]: http://docs.fabfile.org/en/1.10/
[15]: https://www.drupal.org/node/1613424
[16]: https://www.drupal.org/documentation/administer/config
