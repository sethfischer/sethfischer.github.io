Title: Optimising page speed: A case study
Date: 2015-03-27 20:47
Category: Misc
Slug: optimising-page-speed-case-study
Authors: Seth Fischer
Summary: As an exercise in optimising page speed the Pelican theme
    pelican-bootstrap3 by Daan Debie was customised according to the specific
    requirements of seth.fischer.nz. The customisations reduced the total
    number of requests on the index page by 66% and the page size was reduced
    by 62%.


As an exercise in optimising page speed the [Pelican][1] theme
[pelican-bootstrap3][2] by Daan Debie was customised in order to improve page
speed. The customisations reduced the total number of requests on the index
page by 66% and the page size was reduced by 62%.
    

[TOC]


## Pre-optimisation

Before optimisation, as configured for this site, the index page generated 17
requests and had a total page size of 182.9&nbsp;kB.

| http://seth.fischer.nz/          | Pre-optimisation |
|----------------------------------|------------------|
| Requests                         | 15               |
| Requests (SSL)                   | 1                |
| Redirects                        | 1                |
| Page size                        | 182.9&nbsp;kB    |
| Pingdom performance grade        | 81/100           |
| Google PageSpeed score (mobile)  | 74/100           |
| Google PageSpeed score (desktop) | 87/100           |
 
<figure>
    <img src="/images/seth.fischer.nz_2015-03-15_1905_pingdom.png"
        width="582"
        height="133"
        alt="Pingdom speed test summary pre-optimisation; Performance grade: 81/100; Requests: 17; Load time: 591&nbsp;ms; Page size 182.9&nbsp;kB"/>
    <figcaption>Pingdom speed test summary pre-optimisation.</figcaption>
</figure>

Full details are available in the [pre-optimisation HAR file][3].


## Optimisations

Six main  optimisations were made as detailed below. Unless stated the file
sizes specified are for minified but uncompressed versions of the file.


### Custom font

Improvements:

<dl class="dl-horizontal">
    <dt>Page size</dt>
    <dd>−96.1&nbsp;kB</dd>
</dl>

[FontAwesome][4] version 4.1.0 contains a total of 439 icons giving
`fontawesome-webfont.woff` a file size of 83.8&nbsp;kB. A custom font
(`font-custom.woff`) containing only the 12 icons that were required reduced
the size to to 7.4&nbsp;kB.

The associated style sheet `font-awesome.min.css` with a file size of
20.8&nbsp;kB was replaced with `font-custom.css` having a file size of
1.1&nbsp;kB.

[Font Custom][5] was used to create the custom font and Font Custom vectors
were obtained from [Font-Awesome-SVG-PNG][6] by Code Charm.

Font Custom configuration is stored in `fontcustom.yml`, or can be integrated
into a [Grunt][7] build with [grunt-webfont][8] by Artem Sapegin. See the next
section for the `Gruntfile.js` which includes a `grunt-webfont` task.


### Custom Bootstrap

Improvements:

<dl class="dl-horizontal">
    <dt>Page size</dt>
    <dd>−15.3&nbsp;kB</dd>
</dl>

A custom build of [Bootstrap][9] was built with [Compass][10]. By excluding ten
unused components from the build `bootstrap.min.css` was reduced from
109.5&nbsp;kB to 94.2&nbsp;kB.

The Bootstrap build process was included as a Grunt task using
[grunt-contrib-compass][11] by Sindre Sorhus.

Below is the `Gruntfile.js` for this theme which includes both a
`grunt-webfont` task and a `grunt-contrib-compass` task.

    :::javascript
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


### Reduce AJAX requests

Improvements:

<dl class="dl-horizontal">
    <dt>Requests (SSL)</dt>
    <dd>−1</dd>
</dl>

The original theme included a script which obtained a list of GitHub
repositories directly from the [GitHub API][12]. To reduce the overhead of a
SSL request the list of GitHub repositories was generated during the build
process with [pelican-githubprojects][13] by Kura.


### Custom jQuery

Improvements:

<dl class="dl-horizontal">
    <dt>Page size</dt>
    <dd>−18.5&nbsp;kB</dd>
</dl>


A custom build of [jQuery][14] was created according to the instructions in the
[jQuery README file][15].

By excluding the modules ajax, deprecated, offset, and effects, `jquery.min.js`
was reduced from 84.2&nbsp;kB to 65.7&nbsp;kB.

Below is the Grunt command used to build `jquery-custom.min.js`.

    :::console
    jquery((2.1.3))$ grunt custom:-ajax,-deprecated,-offset,-effects


### Merge and minify assets

Improvements:

<dl class="dl-horizontal">
    <dt>Requests</dt>
    <dd>−5</dd>
</dl>

Both JavaScript and CSS were combined using [webassets][16] via the
[Pelican assets plug-in][17].

Five CSS files were merged into a single file and compressed with the
[YUI Compressor][18].

    :::jinja
    {% assets filters="yui_css", output="css/styles.%(version)s.min.css", "css/bootstrap-custom.css", "css/font-custom.css", "css/github-repos.css", "css/style.css", "pygments" %}
        <link href="{{ SITEURL }}/{{ ASSET_URL }}" rel="stylesheet" />
    {% endassets %}

Three JavaScript files were merged and compressed, again with the YUI
Compressor.

    :::jinja
    {% assets filters="yui_js", output="js/scripts.%(version)s.min.js", "js/jquery/jquery-custom.min.js", "js/bootstrap/transition.js", "js/bootstrap/collapse.js" %}
        <script src="{{ SITEURL }}/{{ ASSET_URL }}"></script>
    {% endassets %}

While the homepage of this site did not include images, page size can often be
significantly reduced by optimising images. For example, the two Pingdom screen
shots were were reduced by [pngcrush][19] to approximately 27&nbsp;% of the
original size.


### Eliminate unnecessary resources and DNS lookups

Improvements:

<dl class="dl-horizontal">
    <dt>Requests</dt>
    <dd>−4</dd>
    <dt>Redirects</dt>
    <dd>−1</dd>
    <dt>Page size</dt>
    <dd>−8.5&nbsp;kB</dd>
    <dt>DNS look-ups</dt>
    <dd>−1</dd>
</dl>

Some unnecessary resources were removed from the page including:

  * The Creative Commons licence badge was removed saving two requests (one of
    which was a 301 redirect) and 483&nbsp;B.
  * The JavaScript files `github.js` (1.5&nbsp;kB) and `jXHR.js` (2.5&nbsp;kB)
    were removed as they were replaced by pelican-githubprojects.
  * `respond.js` (4.0&nbsp;kB) was removed as it was decided not to support
     older browsers.


## Post-optimisation

Below is a table summarising the changes made to improve page speed.


| http://seth.fischer.nz/          | Pre-optimisation | Post-optimisation | Improvement    |
|----------------------------------|------------------|-------------------|----------------|
| Requests                         | 16               | 6                 | −10 requests   |
| Requests (SSL)                   | 1                | 0                 | −1 request     |
| Redirects                        | 1                | 0                 | −1 redirect    |
| Page size                        | 182.9&nbsp;kB    | 69.0&nbsp;kB      | −113.9&nbsp;kB |
| Pingdom performance grade        | 81/100           | 88/100            | +7/100         |
| Google PageSpeed score (mobile)  | 74/100           | 89/100            | +15/100        |
| Google PageSpeed score (desktop) | 87/100           | 95/100            | +8/100         |

<figure>
    <img src="/images/seth.fischer.nz_2015-03-16_2149_pingdom.png"
        width="582"
        height="133"
        alt="Pingdom speed test summary post-optimisation; Performance grade: 88/100; Requests: 6; Load time: 194&nbsp;ms; Page size 69.0&nbsp;kB"/>
    <figcaption>Pingdom speed test summary post-optimisation.</figcaption>
</figure>

Full details are available in the [post-optimisation HAR file][20].


## Hosting environment

This site is currently hosted by [GitHub Pages][21]. Besides free-of-charge
managed hosting, GitHub Pages also offers all the advantages of their global
content delivery network.

GitHub Pages compresses \*.html, \*.css, and \*.js files using gzip and set the
appropriate HTTP header `Content-Encoding: gzip`.

A disadvantage of using GitHub Pages as a hosting platform (in relation to
page speed) is the inability to modify HTTP headers to control client-side
caching.

The cache control HTTP headers set by GitHub Pages at the time of writing were:

| Content-Type           | Cache-Control |
|------------------------|---------------|
| text/html              | max-age=600   |
| text/css               | max-age=600   |
| application/javascript | max-age=600   |


If supported by the hosting environment a far future expires header i.e.
`Cache-Control: "max-age=31536000"` (one year) could safely be added to content
types text/css and application/javascript as the webassets plug-in adds a
version identifier to the filename of those content types.


## Summary

These optimisations have reduced the page size by 113.9&nbsp;kB and the number
of requests by twelve. These improvements result in a significantly
improved page load time.

As a result of the modifications made to achieve these improvements the
functionality and flexibility of the original theme has been reduced. In
addition, due to the extensive nature of the modifications merging upstream
commits is no longer a trivial task.

The ease of use of the original theme has also been affected by introducing the
following dependencies:


  * __Build from source__
    * jQuery
  * __Node packages__
    * Grunt
    * grunt-contrib-compass
    * grunt-webfont
  * __Pelican plug-ins__
    * pelican-assets
    * pelican-githubprojects
  * __Ruby gems__
    * bootstrap-sass
    * compass
    * fontcustom
    * sass


## Further reading

  * [HTTP Archive (HAR) format specification][22]
  * [URL Expiry (cache busting)][23] webassets documentation
  * [Make the web faster][24] Google Developers documentation
  * [Best Practices for Speeding Up Your Web Site][25] Yahoo! Developer Network
  * [GitHub Pages][26]
  * [Pingdom tools website speed test][27]


[1]: http://docs.getpelican.com/
[2]: https://github.com/DandyDev/pelican-bootstrap3
[3]: |static|/files/seth.fischer.nz_2015-03-15_1905.har
[4]: https://github.com/FortAwesome/Font-Awesome
[5]: http://fontcustom.com/
[6]: https://github.com/encharm/Font-Awesome-SVG-PNG
[7]: http://gruntjs.com/
[8]: https://github.com/sapegin/grunt-webfont
[9]: http://getbootstrap.com/
[10]: http://compass-style.org/
[11]: https://github.com/gruntjs/grunt-contrib-compass
[12]: https://developer.github.com/
[13]: https://github.com/kura/pelican-githubprojects
[14]: https://github.com/jquery/jquery
[15]: https://github.com/jquery/jquery/blob/master/README.md
[16]: https://github.com/miracle2k/webassets
[17]: https://github.com/getpelican/pelican-plugins
[18]: http://yui.github.io/yuicompressor/
[19]: http://pmt.sourceforge.net/pngcrush/
[20]: |static|/files/seth.fischer.nz_2015-03-16_2149.har
[21]: https://pages.github.com/
[22]: https://w3c.github.io/web-performance/specs/HAR/Overview.html
[23]: http://webassets.readthedocs.org/en/latest/expiring.html
[24]: https://developers.google.com/speed/pagespeed/
[25]: https://developer.yahoo.com/performance/rules.html
[26]: https://pages.github.com/
[27]: http://tools.pingdom.com/fpt/
