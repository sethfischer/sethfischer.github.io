===================================
Optimising page speed: a case study
===================================

:authors: Seth Fischer
:category: Web development
:date: 2015-03-27 20:47
:slug: optimising-page-speed-case-study
:status: published
:tags: Client side, Pelican
:summary: As an exercise in optimising page speed the Pelican theme
    pelican-bootstrap3 by Daan Debie was customised according to the specific
    requirements of seth.fischer.nz. The customisations reduced the total
    number of requests on the index page by 66% and the page size was reduced
    by 62%.


.. note::

    This site is no longer using the theme `sethfischer/pelican-bootstrap3`_.


As an exercise in optimising page speed the `Pelican`_ theme
`DandyDev/pelican-bootstrap3`_ was customised to improve page speed. The
customisations reduced the total number of requests on the index page by 66%
and the page size was reduced by 62%.


.. contents::
    :depth: 2


Pre-optimisation
----------------

Before optimisation, as configured for this site, the index page generated
17 requests and had a total page size of 182.9 kB.

================================ ================
seth.fischer.nz                  Pre-optimisation
================================ ================
Requests                         15
Requests (SSL)                   1
Redirects                        1
Page size                        182.9 kB
Pingdom performance grade        81/100
Google PageSpeed score (mobile)  74/100
Google PageSpeed score (desktop) 87/100
================================ ================

Full details are available in the `pre-optimisation HAR file`_.

.. figure:: /static/optimising-page-speed-case-study/seth.fischer.nz_2015-03-15_1905_pingdom.png
    :width: 582
    :height: 133
    :alt: Pingdom speed test summary pre-optimisation;
        Performance grade: 81/100; Requests: 17; Load time: 591 ms;
        Page size 182.9 kB

    Pingdom speed test summary pre-optimisation.


Optimisations
-------------

Six main optimisations were made as detailed below. Unless stated the file
sizes specified are for minified but uncompressed versions of the file.


Custom font
~~~~~~~~~~~

Improvements:

Page size
    −96.1 kB

`FontAwesome`_ version 4.1.0 contains a total of 439 icons giving
``fontawesome-webfont.woff`` a file size of 83.8 kB. A custom font
(``font-custom.woff``) containing only the 12 icons that were required reduced
the size to to 7.4 kB.

The associated style sheet ``font-awesome.min.css`` with a file size of 20.8 kB
was replaced with ``font-custom.css`` having a file size of 1.1 kB.

`Font Custom`_ was used to create the custom font and Font Custom vectors were
obtained from `encharm/Font-Awesome-SVG-PNG`_.

Font Custom configuration is stored in ``fontcustom.yml``, or can be integrated
into a `Grunt`_ build with `sapegin/grunt-webfont`_. See the next section for
the ``Gruntfile.js`` which includes a ``grunt-webfont`` task.


Custom Bootstrap
~~~~~~~~~~~~~~~~

Improvements:

Page size
    −15.3 kB

A custom build of `Bootstrap`_ was built with `Compass`_. By excluding ten
unused components from the build ``bootstrap.min.css`` was reduced from
109.5 kB to 94.2 kB.

The Bootstrap build process was included as a Grunt task using
`gruntjs/grunt-contrib-compass`_.

Below is the ``Gruntfile.js`` for this theme which includes both a
``grunt-webfont`` task and a ``grunt-contrib-compass`` task.

.. code-block:: javascript

    module.exports = function(grunt) {
        "use strict";

        grunt.initConfig({
            compass: {
                dist: {
                    options: {
                        config: 'config.rb'
                    }
                }
            },
            webfont: {
                icons: {
                    src: 'fontcustom/vectors/*.svg',
                    dest: 'static/font',
                    destCss: 'static/css',
                    options: {
                        htmlDemo: false,
                        hashes: false,
                        font: 'font-custom',
                        types: 'eot,woff,svg,ttf',
                        syntax: 'bem',
                        templateOptions: {
                            baseClass: 'fa',
                            classPrefix: 'fa-'
                        }
                    }
                }
            }
        });

        grunt.loadNpmTasks('grunt-contrib-compass');
        grunt.loadNpmTasks('grunt-webfont');

        grunt.registerTask("default", ["compass", "webfont"]);
    };


Reduce AJAX requests
~~~~~~~~~~~~~~~~~~~~

Improvements:

Requests (SSL)
    −1

The original theme included a script which obtained a list of GitHub
repositories directly from the `GitHub API`_. To reduce the overhead of a SSL
request the list of GitHub repositories was generated during the build process
with `kura/pelican-githubprojects`_.


Custom jQuery
~~~~~~~~~~~~~

Improvements:

Page size
    −18.5 kB

A custom build of `jQuery`_ was created according to the instructions in the
`jQuery README file`_.

By excluding the modules ajax, deprecated, offset, and effects,
``jquery.min.js`` was reduced from 84.2 kB to 65.7 kB.

Below is the Grunt command used to build ``jquery-custom.min.js``.

.. code-block:: console

    jquery((2.1.3))$ grunt custom:-ajax,-deprecated,-offset,-effects


Merge and minify assets
~~~~~~~~~~~~~~~~~~~~~~~

Improvements:

Requests
    −5

Both JavaScript and CSS were combined using `webassets`_ via the
`Pelican assets plug-in`_.

Five CSS files were merged into a single file and compressed with the
`YUI Compressor`_.

.. code-block:: jinja

    {% assets filters="yui_css", output="css/styles.%(version)s.min.css", "css/bootstrap-custom.css", "css/font-custom.css", "css/github-repos.css", "css/style.css", "pygments" %}
        <link href="{{ SITEURL }}/{{ ASSET_URL }}" rel="stylesheet" />
    {% endassets %}

Three JavaScript files were merged and compressed, again with the YUI
Compressor.

.. code-block:: jinja

    {% assets filters="yui_js", output="js/scripts.%(version)s.min.js", "js/jquery/jquery-custom.min.js", "js/bootstrap/transition.js", "js/bootstrap/collapse.js" %}
        <script src="{{ SITEURL }}/{{ ASSET_URL }}"></script>
    {% endassets %}

While the homepage of this site did not include images, page size can often be
significantly reduced by optimising images. For example, the two Pingdom screen
shots were reduced by `pngcrush`_ to approximately 27 % of the original size.


Eliminate unnecessary resources and DNS look-ups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Improvements:

Requests
    −4
Redirects
    −1
Page size
    −8.5 kB
DNS look-ups
    −1

Some unnecessary resources were removed from the page including:

*   The Creative Commons licence badge was removed saving two requests (one of
    which was a 301 redirect) and 483 B.
*   The JavaScript files ``github.js`` (1.5 kB) and ``jXHR.js`` (2.5 kB) were
    removed as they were replaced by pelican-githubprojects.
*   ``respond.js`` (4.0 kB) was removed as it was decided not to support older
    browsers.


Post-optimisation
-----------------

Below is a table summarising the changes made to improve page speed.

================================ ================ ================= ============
seth.fischer.nz                  Pre-optimisation Post-optimisation Improvement
================================ ================ ================= ============
Requests                         16               6                 −10 requests
Requests (SSL)                   1                0                 −1 request
Redirects                        1                0                 −1 redirect
Page size                        182.9 kB         69.0 kB           −113.9 kB
Pingdom performance grade        81/100           88/100            +7/100
Google PageSpeed score (mobile)  74/100           89/100            +15/100
Google PageSpeed score (desktop) 87/100           95/100            +8/100
================================ ================ ================= ============

Full details are available in the `post-optimisation HAR file`_.

.. figure:: /static/optimising-page-speed-case-study/seth.fischer.nz_2015-03-16_2149_pingdom.png
    :width: 582
    :height: 133
    :alt: Pingdom speed test summary post-optimisation;
        Performance grade: 88/100; Requests: 6; Load time: 194 ms;
        Page size 69.0 kB

    Pingdom speed test summary pre-optimisation.


Hosting environment
-------------------

This site is currently hosted by `GitHub Pages`_. Besides free-of-charge
managed hosting, GitHub Pages also offers all the advantages of their global
content delivery network.

GitHub Pages compresses ``*.html``, ``*.css``, and ``*.js`` files using gzip
and sets the appropriate HTTP header ``Content-Encoding: gzip``.

A disadvantage of using GitHub Pages as a hosting platform (in relation to page
speed) is the inability to modify HTTP headers to control client-side caching.

The cache control HTTP headers set by GitHub Pages at the time of writing were:

====================== =============
Content-Type           Cache-Control
====================== =============
text/html              max-age=600
text/css               max-age=600
application/javascript max-age=600
====================== =============

If supported by the hosting environment a far future expires header
``Cache-Control: "max-age=31536000"`` (one year) could safely be added to
content types text/css and application/javascript as the webassets plug-in adds
a version identifier to the filename of those content types.


Summary
-------

These optimisations have reduced the page size by 113.9 kB and the number of
requests by twelve. These improvements result in a significantly improved page
load time.

As a result of the modifications made to achieve these improvements the
capability and flexibility of the original theme has been reduced. In addition,
due to the extensive nature of the modifications merging upstream commits is no
longer a trivial task.

The ease of use of the original theme has also been affected by introducing the
following dependencies:

*   **Build from source**

    *   jQuery

*   **Node packages**

    *   Grunt
    *   grunt-contrib-compass
    *   grunt-webfont

*   **Pelican plug-ins**

    *   pelican-assets
    *   pelican-githubprojects

*   **Ruby gems**

    *   bootstrap-sass
    *   compass
    *   fontcustom
    *   sass


Further reading
---------------

*   `HTTP Archive (HAR) format specification`_
*   `URL Expiry (cache busting)`_ webassets documentation
*   `Make the web faster`_ Google Developers documentation
*   `Best Practices for Speeding Up Your Web Site`_ Yahoo Developer Network
*   `GitHub Pages`_
*   `Pingdom tools website speed test`_


.. _`sethfischer/pelican-bootstrap3`: https://github.com/sethfischer/pelican-bootstrap3
.. _`Pelican`: https://docs.getpelican.com/
.. _`DandyDev/pelican-bootstrap3`: https://github.com/DandyDev/pelican-bootstrap3
.. _`pre-optimisation HAR file`: |static|/static/optimising-page-speed-case-study/seth.fischer.nz_2015-03-15_1905.har
.. _`FontAwesome`: https://github.com/FortAwesome/Font-Awesome
.. _`Font Custom`: https://github.com/FontCustom/fontcustom
.. _`encharm/Font-Awesome-SVG-PNG`: https://github.com/encharm/Font-Awesome-SVG-PNG
.. _`Grunt`: https://gruntjs.com/
.. _`sapegin/grunt-webfont`: https://github.com/sapegin/grunt-webfont
.. _`Bootstrap`: https://getbootstrap.com/
.. _`Compass`: http://compass-style.org/
.. _`gruntjs/grunt-contrib-compass`: https://github.com/gruntjs/grunt-contrib-compass
.. _`GitHub API`: https://docs.github.com/en/rest
.. _`kura/pelican-githubprojects`: https://github.com/kura/pelican-githubprojects
.. _`jQuery`: https://github.com/jquery/jquery
.. _`jQuery README file`: https://github.com/jquery/jquery/blob/master/README.md
.. _`webassets`: https://github.com/miracle2k/webassets
.. _`Pelican assets plug-in`: https://github.com/getpelican/pelican-plugins
.. _`YUI Compressor`: https://yui.github.io/yuicompressor/
.. _`pngcrush`: https://pmt.sourceforge.io/pngcrush/
.. _`post-optimisation HAR file`: |static|/static/optimising-page-speed-case-study/seth.fischer.nz_2015-03-16_2149.har
.. _`GitHub Pages`: https://pages.github.com/
.. _`HTTP Archive (HAR) format specification`: https://w3c.github.io/web-performance/specs/HAR/Overview.html
.. _`URL Expiry (cache busting)`: https://webassets.readthedocs.io/en/latest/expiring.html
.. _`Make the web faster`: https://developers.google.com/speed
.. _`Best Practices for Speeding Up Your Web Site`: https://developer.yahoo.com/performance/rules.html
.. _`Pingdom tools website speed test`: https://tools.pingdom.com/
