=============================================
An introduction to Drupal 8 development tools
=============================================

:authors: Seth Fischer
:category: Web development
:date: 2015-07-07 21:19
:slug: drupal-8-development-tools
:tags: Drupal 8, Drupal
:summary:
    This Drupal 8 article is obsolete.

    The use of third party components in Drupal 8 has inspired two new
    tools for Drupal 8 developers: the Drupal Console and the Drupal Web
    Profiler. Based on the Symfony Console component, the Drupal Console is a
    scaffolding generator which allows developers to reduce development time by
    automating the generation of boilerplate code. The Drupal Web Profiler is a
    port of the Symfony 2 Web Profiler Bundle as a Drupal 8 module providing a
    toolbar with convenient access to performance and profile information.


.. warning::

    This Drupal 8 article is obsolete. It was published in July 2015, four
    months before Drupal 8 was released.


The use of third party components in `Drupal 8`_ has inspired two new tools for
Drupal 8 developers: the Drupal Console and the Drupal Web Profiler. Based on
the `Symfony 2 Console`_ component, the `Drupal Console`_ is a scaffolding
generator which allows developers to reduce development time by automating the
generation of boilerplate code. The `Drupal Web Profiler`_ is a port of the
`Symfony 2 WebProfiler bundle`_ as a Drupal 8 module providing a toolbar with
convenient access to performance and profile information.


.. contents::
    :depth: 2


Drupal Console
--------------

The Drupal Console (`hechoendrupal/DrupalConsole`_ on GitHub) is a
`Symfony 2 console application`_ which provides a number of generators to
assist developers in creating boilerplate code. In addition to increasing
productivity Drupal Console is a valuable learning tool which allows developers
to get up and running with best practice code by kick-starting a
`PSR-4 compliant directory structure`_.

Commands are namespaced, the top-level namespaces currently being:

*   ``cache``
*   ``config``
*   ``container``
*   ``generate``
*   ``migrate``
*   ``module``
*   ``rest``
*   ``router``
*   ``site``
*   ``test``


Commands in the generate namespace
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Drupal Console currently has thirteen commands in the generate namespace:

generate:authentication:provider
    Generate an authentication provider.
generate:command
    Generate commands for the console.
generate:controller
    Generate & register a controller.
generate:entity
    - **generate:entity:config** Generate a new “EntityConfig”.
    - **generate:entity:content** Generate a new “EntityContent”.

generate:form:config
    Generate a new “ConfigFormBase”.
generate:module
    Generate a module.
generate:permissions
    Generate module permissions.
generate:plugin
    - **generate:plugin:block** Generate a plugin block.
    - **generate:plugin:imageeffect** Generate image effect plugin.
    - **generate:plugin:rest:resource** Generate plugin rest resource.
    - **generate:plugin:rulesaction** Generate a plugin rule action.

generate:service
    Generate a service.


.. rubric:: Example: Generating a module

The examples below demonstrate how a module is generated with
``generate:module`` All other commands follow a similar pattern.

.. code-block:: console

    $ drupal generate:module

     Welcome to the Drupal module generator

    Enter the new module name: awesome
    Enter the module machine name [awesome]:
    Enter the module Path [/modules/custom]:
    Enter module description [My Awesome Module]:
    Enter package name [Other]:
    Enter Drupal Core version [8.x]:
    Do you want to generate a default Controller [no]? yes
    Would you like to add module dependencies [yes]? no
    Do you want to generate a unit test class [yes]? yes
    Do you confirm generation [yes]? yes

     Generated or updated files

    Site path: /var/www/drupal8
    1 - /modules/custom/awesome/awesome.info.yml
    2 - /modules/custom/awesome/awesome.module
    3 - /modules/custom/awesome/src/Controller/DefaultController.php
    4 - /modules/custom/awesome/awesome.routing.yml
    5 - /modules/custom/awesome/Tests/Controller/DefaultControllerTest.php

Rather than using the default interactive prompt, options can be passed
to the command.

.. code-block:: console

    $ drupal generate:module \
    --module="awesome" \
    --machine-name="awesome" \
    --module-path="modules/custom" \
    --description="My Awesome Module" \
    --core="8.x" \
    --package="Other" \
    --controller \
    --dependencies


Additional commands
~~~~~~~~~~~~~~~~~~~

In addition to commands in the generate namespace Drupal Console has many other
commands. Run ``drupal list`` to list available commands. Modules can define
their own commands so the available commands may vary according to the modules
installed.

Site status information may be viewed with the command ``site:status``,
optionally passing the ``--format=json`` option.

.. code-block:: console

    $ drupal site:status --format=json

Output of above command:

.. code-block:: json

    {
        "system": {
            "Drupal": "8.0.0-dev",
            "Access to update.php": "Protected",
            "Configuration files": "Protected",
            "Cron maintenance tasks": "Last run 44 min 45 sec ago",
            "D3.js library": "Enabled",
            "Database system": "MySQL, MariaDB, Percona Server, or equivalent",
            "Database system version": "5.5.43-0+deb7u1",
            "Database updates": "Out of date",
            "Drupal core update status": "<a href=\"\/admin\/reports\/updates\">Unknown release date (version 8.0.0-beta11 available)<\/a>",
            "File system": "Writable (<em>public<\/em> download method)",
            "GD library": "2.0.36",
            "GD library PNG support": "2.0.36",
            "Image toolkit": "gd",
            "Module and theme update status": "<a href=\"\/admin\/reports\/updates\">Out of date<\/a>",
            "Node Access Permissions": "Disabled",
            "PHP": "5.4.41-0+deb7u1 (<a href=\"\/admin\/reports\/status\/php\">more information<\/a>)",
            "PHP extensions": "Enabled",
            "PHP memory limit": "-1 (Unlimited)",
            "Search index progress": "100% (0 remaining)",
            "Trusted Host Settings": "Not enabled",
            "Unicode library": "PHP Mbstring Extension",
            "Update notifications": "Enabled",
            "Upload progress": "Not enabled",
            "Web server": null,
            "highlight.js library": "Enabled"
        },
        "database": {
            "Driver": "mysql",
            "Host": "localhost",
            "Database connection": "drupal8",
            "Port": "",
            "Username": "drupal8",
            "Password": "redacted",
            "Connection": "mysql\/\/drupal8:redacted@localhost\/drupal8"
        },
        "theme": {
            "theme_default": "bartik",
            "theme_admin": "seven"
        },
        "directory": {
            "Site root directory": "\/var\/www\/drupal8\/",
            "Site temporary directory": "\/tmp",
            "Default theme directory": "\/core\/themes\/bartik",
            "Admin theme directory": "\/core\/themes\/seven"
        }
    }


Custom commands
~~~~~~~~~~~~~~~

Modules may define commands by extending
``Symfony\Component\Console\Command\Command``. Drupal Console can create
scaffolding for a custom command with the command ``generate:command``. Refer
to the `Symfony 2 Console Component documentation`_ for additional information.
For an example implementation refer to the source code of Web Profiler
``git clone http://git.drupal.org/project/webprofiler.git``.


Chain command execution
~~~~~~~~~~~~~~~~~~~~~~~

Commands may be recorded in YAML and executed with the ``chain`` command:

.. code-block:: console

    $ drupal chain --file=~/d8-project-init.yml

In the example below a module will be created, followed by a controller
for that module.

.. code-block:: yaml

    # d8-project-init.yml
    commands:
        - command: generate:module
          options:
            module: awesome
            machine-name: awesome
            module-path: /modules/custom/
            description: My Awesome module
            core: 8.x
            package: Test
            controller: false
            dependencies:
            test: false
        - command: generate:controller
          options:
            module: awesome
            class-name: AwesomeController
            method-name: index
            route: /awesome/index
            services: twig


Web Profiler
------------

The `Drupal Web Profiler`_ provides convenient access to a selection of
performance and profile information on a per request basis.


Data collectors
~~~~~~~~~~~~~~~

The Web Profiler provides a number of data collectors which include:

*   PHP configuration
*   route and controller name
*   page load timeline and memory use
*   front-end statistics (timings for: DNS lookup time; TCP handshake;
    :abbr:`TTFB (Time to first byte)`; data download; and DOM build)
*   database query time and number of queries
*   authentication details
*   number of views
*   number of blocks loaded and rendered
*   number of modules and themes available
*   cache statistics
*   asset statistics

A summary of the data collected is displayed in the Web Profiler toolbar
which is displayed along the lower edge of the viewport.

.. raw:: html

    <figure>
        <picture>
            <source srcset="/static/drupal-8-development-tools/drupal-8-webprofiler-toolbar-large.png"
                media="(min-width: 950px)"/>
            <img src="/static/drupal-8-development-tools/drupal-8-webprofiler-toolbar-medium.png"
                alt="Drupal 8 Web Profiler toolbar"/>
        </picture>
        <figcaption>The Drupal 8 Web Profiler toolbar.</figcaption>
    </figure>

Additional detail for each data collector may be viewed by clicking the
relevant icon in the toolbar overlay. Below is the detailed report for the page
load timeline.

.. raw:: html

    <figure>
        <picture>
            <source srcset="/static/drupal-8-development-tools/drupal-8-webprofiler-report-large.png"
                media="(min-width: 950px)"/>
            <source srcset="/static/drupal-8-development-tools/drupal-8-webprofiler-report-medium.png"
                media="(min-width: 600px)"/>
            <img src="/static/drupal-8-development-tools/drupal-8-webprofiler-report-small.png"
                alt="Drupal 8 Web Profiler toolbar"/>
        </picture>
        <figcaption>Example of a Drupal 8 Web Profiler report timeline.</figcaption>
    </figure>



Profiling decoupled (or headless) requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The inclusion of a `HTTP routing framework`_ and `REST API`_ in Drupal 8 core
will make it significantly easier to develop decoupled applications using a
client-side framework such as `ember.js`_ which connects to a Drupal backend.

When profiling an API or headless request the Web Profiler toolbar is not
available. However the profile data remains available for each request via a
token and link provided in the HTTP response headers ``X-Debug-Token`` and
``X-Debug-Token-Link``.

.. code-block:: http

    HTTP/1.1 200 OK
    Date: Fri, 26 Jun 2015 23:53:36 GMT
    Server: Apache/2.2.22 (Debian)
    X-Generator: Drupal 8 (https://www.drupal.org)
    X-Debug-Token: 0ac668
    X-Debug-Token-Link: /admin/reports/profiler/view/0ac668

Visiting the X-Debug-Token-Link (in this case
``/admin/reports/profiler/view/0ac668``) will provide access to the report for
he relevant request.


Web Profiler console commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Web profiler provides three console commands:

``webprofiler:benchmark``
    Benchmark a URL.
``webprofiler:export``
    Export Web Profiler profiles to file.
``webprofiler:list``
    List Web Profiler profiles.


.. rubric:: benchmark

Benchmark a URL.

.. code-block:: console

    $ drupal webprofiler:benchmark http://drupal8/
     105/105 [============================] 100% Done.
    date: 'Sun, 06/28/2015 - 21:00:43'
    git_commit: "e39a32842072bfbaa2b15c5284625ff63ebc4a08\n"
    number_of_runs: 100
    url: 'http://drupal8/'
    results:
        average: { time: '340 ms', memory: '38.8 MB' }
        median: { time: '336 ms', memory: '38.8 MB' }
        95_percentile: { time: '326 ms', memory: '38.8 MB' }


.. rubric:: export

Export profile data to a file for later analysis.

.. code-block:: console

    $ drupal webprofiler:export --directory=/tmp/
     266/266 [============================] 100% Done.
    Exported 264 profiles


.. rubric:: list

List and filter profiles.

.. code-block:: console

    $ drupal webprofiler:list --url=http://drupal8/ --method=GET --limit=5
    +--------+-----------+--------+-----------------+----------------------------+
    | Token  | IP        | Method | URL             | Time                       |
    +--------+-----------+--------+-----------------+----------------------------+
    | 6f6333 | 127.0.0.1 | GET    | http://drupal8/ | Sun, 06/28/2015 - 20:57:01 |
    | 429e2e | 127.0.0.1 | GET    | http://drupal8/ | Sun, 06/28/2015 - 20:57:00 |
    | dc1461 | 127.0.0.1 | GET    | http://drupal8/ | Sun, 06/28/2015 - 20:57:00 |
    | d00a91 | 127.0.0.1 | GET    | http://drupal8/ | Sun, 06/28/2015 - 20:56:59 |
    | ef359a | 127.0.0.1 | GET    | http://drupal8/ | Sun, 06/28/2015 - 20:56:59 |
    +--------+-----------+--------+-----------------+----------------------------+


Further reading
---------------

*   `The Drupal Console book`_
*   `How to create a custom data collector`_
*   `An introduction to RESTful web services in Drupal 8`_
*   `Headless websites: What’s the big deal?`_


.. _`Drupal 8`: https://www.drupal.org/8
.. _`Symfony 2 Console`: https://symfony.com/doc/2.7/components/console.html
.. _`Drupal Console`: https://drupalconsole.com/
.. _`Drupal Web Profiler`: https://www.drupal.org/project/webprofiler
.. _`Symfony 2 WebProfiler bundle`: https://github.com/symfony/web-profiler-bundle
.. _`hechoendrupal/DrupalConsole`: https://github.com/hechoendrupal/drupal-console
.. _`Symfony 2 console application`: https://symfony.com/doc/2.7/components/console.html
.. _`PSR-4 compliant directory structure`: https://www.drupal.org/node/2156625
.. _`Symfony 2 Console Component documentation`: https://symfony.com/doc/2.7/components/console.html
.. _`Drupal Web Profiler`: https://www.drupal.org/project/webprofiler
.. _`HTTP routing framework`: https://www.drupal.org/docs/8/api/routing-system/routing-system-overview
.. _`REST API`: https://www.drupal.org/docs/8/core/modules/rest/overview
.. _`ember.js`: https://emberjs.com/
.. _`The Drupal Console book`: https://www.gitbook.com/book/hechoendrupal/drupal-console/details
.. _`How to create a custom data collector`: https://symfony.com/doc/2.7/profiler/data_collector.html
.. _`An introduction to RESTful web services in Drupal 8`: https://drupalize.me/blog/201401/introduction-restful-web-services-drupal-8
.. _`Headless websites: What’s the big deal?`: https://pantheon.io/blog/headless-websites-whats-big-deal-decoupled-architecture
