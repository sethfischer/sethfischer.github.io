Title: An introduction to Drupal 8 development tools
Date: 2015-07-07 21:19
Category: Drupal
Tags: Drupal 8, Drupal
Slug: drupal-8-development-tools
Authors: Seth Fischer
Summary: The use of third party components in Drupal 8 has inspired two new
    tools for Drupal 8 developers: the Drupal Console and the Drupal Web
    Profiler. Based on the Symfony Console component, the Drupal Console is a
    scaffolding generator which allows developers to reduce development time by
    automating the generation of boilerplate code. The Drupal Web Profiler is a
    port of the Symfony 2 Web Profiler Bundle as a Drupal 8 module providing a
    toolbar with convenient access to performance and profile information. 


The use of third party components in [Drupal&nbsp;8][1] has inspired two new
tools for Drupal&nbsp;8 developers: the Drupal Console and the Drupal Web
Profiler. Based on the [Symfony&nbsp;2 Console][2] component, the
[Drupal Console][3] is a scaffolding generator which allows developers to
reduce development time by automating the generation of boilerplate code. The
[Drupal Web Profiler][4] is a port of the
[Symfony&nbsp;2 WebProfiler bundle][5] as a Drupal&nbsp;8 module providing a
toolbar with convenient access to performance and profile information.


[TOC]


## Drupal Console

The Drupal Console ([hechoendrupal/DrupalConsole][6] on GitHub) is a
[Symfony&nbsp;2 console application][7] which provides a number of generators
to assist developers in creating boilerplate code. In addition to increasing
productivity Drupal Console is a valuable learning tool which allows developers
to get up and running with best practice code by kick-starting a
[PSR-4 compliant directory structure][8].

Commands are namespaced, the top-level namespaces currently being:

  * `cache`
  * `config`
  * `container`
  * `generate`
  * `migrate`
  * `module`
  * `rest`
  * `router`
  * `site`
  * `test`


### Commands in the generate namespace

Drupal Console currently has thirteen commands in the generate namespace: 

generate:authentication:provider
:   Generate an authentication provider.

generate:command
:   Generate commands for the console.

generate:controller
:   Generate & register a controller.

generate:entity
:   * __generate:entity:config__ Generate a new "EntityConfig".
    * __generate:entity:content__ Generate a new "EntityContent".

generate:form:config
:   Generate a new "ConfigFormBase".

generate:module
:   Generate a module.

generate:permissions
:   Generate module permissions.

generate:plugin
:   * __generate:plugin:block__ Generate a plugin block.
    * __generate:plugin:imageeffect__ Generate image effect plugin.
    * __generate:plugin:rest:resource__ Generate plugin rest resource.
    * __generate:plugin:rulesaction__ Generate a plugin rule action.

generate:service
:   Generate a service.


#### Example: Generating a module

The examples below demonstrate how a module is generated with `generate:module`
All other commands follow a similar pattern.

    ::console
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

Rather than using the default interactive prompt, options can be passed to the
command.

    :::console
    $ drupal generate:module \
    --module="awesome" \
    --machine-name="awesome" \
    --module-path="modules/custom" \
    --description="My Awesome Module" \
    --core="8.x" \
    --package="Other" \
    --controller \
    --dependencies


### Additional commands

In addition to commands in the generate namespace Drupal Console has many other
commands. Run `drupal list` to list available commands. Modules can define
their own commands so the available commands may vary according to the modules
installed.

Site status information may be viewed with the command `site:status`,
optionally passing the `--format=json` option.

    :::console
    $ drupal site:status --format=json

Output of above command:

    :::json
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


### Custom commands

Modules may define commands by extending
`Symfony\Component\Console\Command\Command`. Drupal Console can create
scaffolding for a custom command with the command `generate:command`.
Refer to the [Symfony&nbsp;2 Console Component documentation][7] for additional
information. For an example implementation refer to the source code of Web
Profiler `git clone http://git.drupal.org/project/webprofiler.git`.


### Chain command execution

Commands may be recorded in YAML and executed with the `chain` command:

    $ drupal chain --file=~/d8-project-init.yml

In the example below a module will be created, followed by a controller for
that module.

    :::yaml
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


## Web Profiler

The [Drupal Web Profiler][4] provides convenient access to a selection of
performance and profile information on a per request basis.


### Data collectors

The Web Profiler provides a number of data collectors which include:

  * PHP configuration
  * route and controller name
  * page load timeline and memory use
  * front-end statistics (timings for: DNS lookup time; TCP handshake; TTFB;
      data download; and  DOM build)
  * database query time and number of queries
  * authentication details
  * number of views
  * number of blocks loaded and rendered
  * number of modules and themes available
  * cache statistics
  * asset statistics

A summary of the data collected is displayed in the Web Profiler toolbar which
is displayed along the lower edge of the viewport.

<figure>
    <picture>
        <source srcset="/images/drupal-8-webprofiler-toolbar-large.png"
            media="(min-width: 950px)"/>
        <img src="/images/drupal-8-webprofiler-toolbar-medium.png"
            alt="Drupal 8 Web Profiler toolbar"/>
    </picture>
    <figcaption>The Drupal&nbsp;8 Web Profiler toolbar.</figcaption>
</figure>

Additional detail for each data collector may be viewed by clicking the
relevant icon in the toolbar overlay. Below is the detailed report for the page
load timeline.

<figure>
    <picture>
        <source srcset="/images/drupal-8-webprofiler-report-large.png"
            media="(min-width: 950px)"/>
        <source srcset="/images/drupal-8-webprofiler-report-medium.png"
            media="(min-width: 600px)"/>
        <img src="/images/drupal-8-webprofiler-report-small.png"
            alt="Drupal 8 Web Profiler toolbar"/>
    </picture>
    <figcaption>Example of a Drupal&nbsp;8 Web Profiler report timeline.</figcaption>
</figure>


### Profiling decoupled (or headless) requests

The inclusion of a [HTTP routing framework][9] and [REST API][10] in
Drupal&nbsp;8 core will make make it significantly easier to develop decoupled
applications using a client-side framework such as [ember.js][11] which
connects to a Drupal backend.

When profiling an API or headless request the Web Profiler toolbar is not
available. However the profile data remains available for each request via a
token and link provided in the HTTP response headers `X-Debug-Token` and
`X-Debug-Token-Link`.

    :::http
    HTTP/1.1 200 OK
    Date: Fri, 26 Jun 2015 23:53:36 GMT
    Server: Apache/2.2.22 (Debian)
    X-Generator: Drupal 8 (https://www.drupal.org)
    ⋮
    X-Debug-Token: 0ac668
    X-Debug-Token-Link: /admin/reports/profiler/view/0ac668
    ⋮

Visiting the X-Debug-Token-Link (in this case
`/admin/reports/profiler/view/0ac668`) will provide access to the report for
the relevant request.


### Web Profiler console commands

Web profiler provides three console commands:

webprofiler:benchmark
:   Benchmark a url.

webprofiler:export
:   Export Webprofiler profile(s) to file.

webprofiler:list
:   List Webprofiler profiles.


#### benchmark

Benchmark a URL.

    :::console
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


#### export

Export profile data to a file for later analysis.

    :::console
    $ drupal webprofiler:export --directory=/tmp/
     266/266 [============================] 100% Done.                
    Exported 264 profiles



#### list

List and filter profiles.

    :::console
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


## Further reading

  * [The Drupal Console book][12]
  * [How to create a custom data collector][13]
  * [An introduction to RESTful web services in Drupal&nbsp;8][14]
  * [Headless websites: What's the big deal?][15]


*[TTFB]: Time to first byte


[1]: https://www.drupal.org/drupal-8.0
[2]: http://symfony.com/doc/current/components/console/introduction.html
[3]: http://drupalconsole.com/
[4]: https://www.drupal.org/project/webprofiler
[5]: https://github.com/symfony/WebProfilerBundle
[6]: https://github.com/hechoendrupal/DrupalConsole
[7]: http://symfony.com/doc/current/components/console/introduction.html
[8]: https://www.drupal.org/node/2156625
[9]: https://www.drupal.org/developing/api/8/routing
[10]: https://www.drupal.org/documentation/modules/rest
[11]: http://emberjs.com/
[12]: https://www.gitbook.com/book/hechoendrupal/drupal-console/details
[13]: http://symfony.com/doc/current/cookbook/profiler/data_collector.html
[14]: https://drupalize.me/blog/201401/introduction-restful-web-services-drupal-8
[15]: https://pantheon.io/blog/headless-websites-whats-big-deal

