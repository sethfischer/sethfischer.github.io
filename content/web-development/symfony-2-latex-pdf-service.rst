=================================
Symfony 2 PDF service using LaTeX
=================================

:authors: Seth Fischer
:category: Web development
:date: 2015-04-19 20:11
:slug: symfony-2-latex-pdf-service
:status: published
:tags: Symfony 2, LaTeX
:software: Symfony: 2.3.18
:software: LaTeX: pdfTeX, Version 3.1415926-2.4-1.40.13 (TeX Live 2012/Debian)
:software: PHP: 5.4.36-0+deb7u3
:software: rubber-pipe: 1.1
:summary:
    This Symfony 2 article is obsolete.

    Portable Document Format (PDF) has become a universally accepted format
    for sharing documentation. As a result, the dynamic generation of PDF
    documents is an expected feature of many web applications. After reviewing
    a number of libraries for generating PDF documents it was decided to write
    a service wrapping the LaTeX typesetting system . LaTeX is ideally suited
    to the production of scientific and technical documentation.


.. warning::

    This Symfony 2 article is obsolete. Symfony 2 reached end-of-life in
    November 2018.


Portable Document Format (PDF) has become a universally accepted format for
sharing documentation. As a result, the dynamic generation of PDF documents is
an expected feature of many web applications. After reviewing a number of
libraries for generating PDF documents it was decided to write a service
wrapping the `LaTeX`_ typesetting system . LaTeX is ideally suited to the
production of scientific and technical documentation.

The code examples used in this article are from the certificate generation
component of IB2020, a `Symfony`_ 2 web application for the management of
welder qualifications.


.. contents::
    :depth: 2


PDF generating libraries
------------------------

Before implementing the LaTeX service the following PDF generating libraries
were considered:

1.  `TCPDF`_

    *   HTML layout and rendering engine written in PHP.
    *   Coordinate-based interface.

2.  `dompdf`_

    *   HTML layout and rendering engine written in PHP.
    *   Style-driven renderer.

3.  `wkhtmltopdf`_

    *   Command line tools to render HTML into PDF (and various other image
        formats) using the QT WebKit rendering engine.

4.  `KnpLabs/KnpSnappyBundle`_

    *   Symfony 2 bundle wrapping ``wkhtmltopdf``.

5.  `zendframework/ZendPdf`_

    *   HTML layout and rendering engine written in PHP.
    *   Coordinate-based interface.


LaTeX
-----

The LaTeX system is a markup language and high-quality typesetting system. It
is written in the `TeX macro language`_.

A PDF document may be generated directly from a LaTeX source document with the
``pdflatex`` binary, part of the Debian ``texlive-full`` meta-package. Some
LaTeX documents require multiple passes with ``pdflatex``, a process which is
automated with the script ``rubber-pipe``.

LaTeX and ``rubber-pipe`` may be installed on Debian-based distributions with
the following commands:

.. code-block:: console

    $ sudo apt-get install texlive-full
    $ sudo apt-get install rubber

The PDF LaTeX service is essentially a wrapper around ``rubber-pipe`` which in
turn invokes ``pdflatex``.


Symfony 2 service
-----------------

`Services`_ are re-usable, decoupled components, that may be accessed from any
part of the application. The `definition of a service`_ from the Symfony
documentation:

.. vale off

    A service is usually used “globally”, such as a database connection
    object or an object that delivers email messages. In Symfony,
    services are often configured and retrieved from the service
    container.

.. vale on

The PDF LaTeX service consists of the following three components:

1.  The **Symfony service container** configured in ``services.yml``.
2.  A **class** ``Pdflatex`` of which an instance is available in the service
    container.
3.  A **Twig template** ``show.tex.twig`` used to output the LaTeX source
    document.


Configure the service container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The service container is configured with ``services.yml``. Two services are
defined in the `YAML`_ below: 1. ``electrotech.twig.ib2020_extension``, which
provides a Twig filer to escape LaTeX special characters; and
2. ``electrotech.pdf.pdflatex``, the PDF LaTeX service itself.

For convenience the ``rubber-pipe`` binary is defined as a parameter.

.. code-block:: yaml

    # src/Electrotech/WeldqualBundle/Resources/config/services.yml

    parameters:
        electrotech.twig.ib2020_extension.class: Electrotech\WeldqualBundle\Twig\Ib2020Extension
        electrotech.pdf.pdflatex.rubber-pipe: /usr/bin/rubber-pipe

    services:
        electrotech.twig.ib2020_extension:
            class: %electrotech.twig.ib2020_extension.class%
            arguments: [%kernel.bundles%]
            tags:
                - { name: twig.extension }

        electrotech.pdf.pdflatex:
            class:        Electrotech\WeldqualBundle\Pdf\Pdflatex
            arguments:    [%electrotech.pdf.pdflatex.rubber-pipe%]


Service object
~~~~~~~~~~~~~~

An instance of the class ``Pdflatex`` provides the service. ``Pdflatex`` takes
a LaTeX source document and returns a PDF document.

.. code-block:: php

    <?php
    // src/Electrotech/WeldqualBundle/Pdf/Pdflatex.php

    namespace Electrotech\WeldqualBundle\Pdf;

    class Pdflatex
    {

        /**
         * Full system path to rubber-pipe binary
         * @var string
         */
        private $binary;

        /**
         * Options for rubber-pipe
         * @var array
         */
        private $options = array(
            '--pdf' => null,
            '--into' => '/tmp/'
        );

        /**
         * Tex source document
         * @var string
         */
        private $texSource;

        /**
         * Generated PDF document
         */
        private $pdf;

        /**
         * Initial working dir
         * @var string
         */
        private $cwd = '/tmp/';

        /**
         * Environment variables
         * @var array|null
         */
        private $env = null;

        /**
         * Error output
         * @var string
         */
        private $stderr = null;

        /**
         * Return value
         * @var integer
         */
        private $returnValue;


        public function __construct($binary)
        {
            $this->binary = $binary;
        }

        /**
         * Create rubber-pipe command
         */
        public function getCommand()
        {
            $args = '';
            foreach ($this->options as $option => $value)
            {
                $args .= ' '.$option;
                if ($value !== null)
                {
                    $args .= ' '.$value;
                }
            }
            return $this->binary.$args;
        }

        /**
         * Execute rubber-pipe command
         */
        public function execute()
        {
            $descriptorSpec = array(
                0 => array("pipe", "r"),
                1 => array("pipe", "w"),
                2 => array("pipe", "w"),
            );

            $process = proc_open(
                $this->getCommand(),
                $descriptorSpec,
                $pipes,
                $this->cwd,
                $this->env
            );

            if (is_resource($process)) {
                fwrite($pipes[0], $this->getTexSource());
                fclose($pipes[0]);

                $this->pdf = stream_get_contents($pipes[1]);
                $this->stderr = stream_get_contents($pipes[2]);
                $this->returnValue = proc_close($process);
            }

            if ($this->returnValue == 0)
            {
                return true;
            }
            return false;
        }

        /**
         * Set path to rubber-pipe binary
         * @param string $binary Full system path to rubber-pipe binary
         */
        public function setBinary($binary)
        {
            $this->binary = $binary;
        }

        /**
         * Get path to rubber-pipe binary
         * @return string Full system path to rubber-pipe binary
         */
        public function getBinary()
        {
            return $this->binary;
        }

        /**
         * Set LaTeX source
         * @param string $texSource LaTeX source document
         */
        public function setTexSource($texSource)
        {
            $this->texSource = $texSource;
        }

        /**
         * Get LaTeX source
         * @return string LaTeX source document
         */
        public function getTexSource()
        {
            return $this->texSource;
        }

        /**
         * Get PDF file contents
         * @return mixed Generated PDF file contents
         */
        public function getPdf()
        {
            return $this->pdf;
        }

        /**
         * Get errors
         * @return string Error output
         */
        public function getStderr()
        {
            return $this->stderr;
        }

        /**
         * Get return value
         * @return integer Return value from rubber-pipe command
         */
        public function getReturnValue()
        {
            return $this->returnValue;
        }

    }


Twig template
~~~~~~~~~~~~~

A `Twig`_ template ``show.tex.twig`` is used to generate the LaTeX source
document.

.. code-block:: latex


    % src/Electrotech/WeldqualBundle/Resources/views/Testweld/show.tex.twig

    % This template has been simplified for the sake of brevity.

    \documentclass[10pt,a4paper]{article}

    \usepackage{array}
    \usepackage{calc}
    \usepackage{color}
    \usepackage{colortbl}
    \usepackage{graphicx}
    \usepackage[margin=1cm]{geometry}
    \usepackage{multirow}
    \usepackage{tabularx}
    \usepackage{wasysym}

    % width of table columns
    \newlength{\colOneWidth}
    \setlength{\colOneWidth}{0.13\textwidth}
    \newlength{\colThreeWidth}
    \setlength{\colThreeWidth}{0.13\textwidth}
    \newlength{\colFourWidth}
    \setlength{\colFourWidth}{0.25\textwidth}
    \newlength{\colFiveWidth}
    \setlength{\colFiveWidth}{0.13\textwidth}
    \newlength{\colThreeToFiveWidth}
    \setlength{\colThreeToFiveWidth}{\colThreeWidth + \colFourWidth + \colFiveWidth}
    \newlength{\colFourToFiveWidth}
    \setlength{\colFourToFiveWidth}{\colFourWidth + \colFiveWidth}


    % colours
    \definecolor{IB2020Blue}{RGB}{172,206,230} % #ACCEE6
    \definecolor{invalidBg}{RGB}{242,222,222}  % #F2DEDE
    \definecolor{invalidFg}{RGB}{185,74,72}    % #B94A48

    % page style
    \pagestyle{empty} % remove page numbering

    % PDF meta data
    \pdfinfo{
        /Title (Welder Qualification Certificate)
        /Creator (IB2020 {{ electrotech_system_owner | e_latex }})
        /Producer (IB2020 {{ electrotech_system_owner | e_latex }})
        /Author (IB2020 A Management Information System for Inspection Bodies)
        /CreationDate (D:{{ "now"|date("YmdGisO") | e_latex }})
        /ModDate (D:{{ "now"|date("YmdGisO") | e_latex }})
        /Subject (Welder Qualification Certificate)
        /Keywords (IB2020)
    }


    \begin{document}

    % remove left indent from table
    \noindent%
    \begin{tabularx}{\textwidth}{@{}|p{\colOneWidth}|X|p{\colThreeWidth}|p{\colFourWidth}|p{\colFiveWidth}| }
        \hline
            \centering \scriptsize{}Certificate Number\newline \normalsize {{ entity.certificateNumber | e_latex }} &
            \multicolumn{3}{c|}{ \cellcolor{IB2020Blue} \textbf{Welder Qualification Certificate} } &
            \raisebox{-0.5\height}{
                \includegraphics[width=0.13\textwidth]{{ '{' }}{{ logoFile | e_latex }}{{ '}' }}
            } \\
        \hline
            \multicolumn{5}{|c|}{
                {{ electrotech_system_owner | e_latex }}
                \enspace
                IANZ Accredited Inspection Body No. {{ electrotech_ianz_number | e_latex }}
            } \\
        \hline
    \end{tabularx}

    \end{document}

A `custom Twig filter`_ ``e_latex`` is used to escape LaTeX special characters.
Custom Twig filters are created by extending ``Twig_Extension``.

.. code-block:: php

    <?php
    // src/Electrotech/WeldqualBundle/Twig/Ib2020Extension.php

    namespace Electrotech\WeldqualBundle\Twig;

    use Twig_Extension;
    use Twig_Filter_Method;
    use Twig_Test_Method;

    class Ib2020Extension extends Twig_Extension
    {
        // Unrelated methods have been omitted from this code sample for the sake
        // of brevity.

        private $kernelBundles;

        public function __construct($kernelBundles)
        {
            $this->kernelBundles = $kernelBundles;
        }

        /**
         * Returns a list of filters to add to the existing list.
         *
         * @return array An array of filters
         */
        public function getFilters()
        {
            return array(
                'e_latex'     => new Twig_Filter_Method($this, 'escapeLatexFilter'),
            );
        }

        /**
         * Escape LaTeX special characters
         *
         * @return string
         */
        public function escapeLatexFilter($str = null)
        {
            $search = array('\\', '#', '$', '%', '&', '_', '{', '}', '~', '^',
                '>', '<');

            $replace = array('\textbackslash ', '\#', '\$', '\%', '\&', '\_',
                '\{', '\}', '\textasciitilde ', '\textasciicircum ',
                '\textgreater', '\textless');

            return str_replace($search ,$replace ,$str);
        }

        /**
         * Returns the name of the extension
         *
         * @return string The extension name
         */
        public function getName()
        {
            return 'electrotech_twig_ib2020_extension';
        }

    }


Utilising the service
~~~~~~~~~~~~~~~~~~~~~

The service is used in the controller by passing a certificate ID to the method
``pdfAction()``. The LaTeX source document is then generated by the method
``latexSource()``.

.. code-block:: php

    <?php

    // Utilising the PDF LaTeX service
    $pdflatex = $this->get('electrotech.pdf.pdflatex');
    $pdflatex->setTexSource($latexSource);
    $pdf = $pdflatex->getPdf()

Below is an example of how this service is used in a controller.

.. code-block:: php

    <?php

    // src/Electrotech/WeldqualBundle/Controller/TestweldController.php

    namespace Electrotech\WeldqualBundle\Controller;

    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\HttpKernel\Exception\HttpException;
    use Symfony\Bundle\FrameworkBundle\Controller\Controller;

    use Electrotech\WeldqualBundle\Entity\Testweld;
    use Electrotech\WeldqualBundle\Entity\Testweldassessment;
    use Electrotech\WeldqualBundle\Form\TestweldType;
    use Electrotech\WeldqualBundle\Helper\QualificationRangeHelper;


    /**
     * Testweld controller
     */
    class TestweldController extends Controller
    {
        // Unrelated methods have been omitted from this code sample for the sake
        // of brevity.

        /**
         * Creates a PDF certificate
         */
        public function pdfAction($id)
        {

            $latexSource = $this->latexSource($id, 'show.tex.twig');

            $pdflatex = $this->get('electrotech.pdf.pdflatex');
            $pdflatex->setTexSource($latexSource['latex']);

            if (!$pdflatex->execute())
            {
                throw new HttpException(500, 'Error creating PDF: '.$pdflatex->getStderr());
            }

            $response = new Response();
            $response->setContent($pdflatex->getPdf());
            $response->headers->set('Content-Type', 'application/pdf');
            $response->headers->set('Content-Disposition', 'inline; filename="'.$latexSource['filename'].'.pdf"');

            return $response;
        }

        /**
         * Creates LaTeX source
         */
        private function latexSource($id, $template)
        {
            $em = $this->getDoctrine()->getManager();

            $entity = $em->getRepository('ElectrotechWeldqualBundle:Testweld')->find($id);

            if (!$entity) {
                throw $this->createNotFoundException('Unable to find Testweld entity.');
            }

            $em = $this->getDoctrine()->getManager();

            $weldVariables = $em->getRepository('ElectrotechWeldqualBundle:Weldvariables')
                ->fetchWeldVariables(
                    $entity->getQualificationstandard()->getEdition()->getTechdoc(),
                    $entity->getProducttype(),
                    $entity->getWeldtype(),
                    $entity->getWeldposition(),
                    $entity->getWelddirection()
                );

            $qualifiedRange = null;

            if ($weldVariables !== null)
            {
                $qualifiedRange = new QualificationRangeHelper(
                    $entity->getProducttype(),
                    $entity->getPipeod(),
                    $weldVariables->getQualifiedweldvariablesid()
                );
            }

            $logoFile = $this->get('kernel')->getRootDir().DIRECTORY_SEPARATOR.
                $this->container->getParameter('electrotech_upload_dir').DIRECTORY_SEPARATOR.
                'sysowner'.DIRECTORY_SEPARATOR.'logo.pdf';

            $templating = $this->get('templating');

            $latexSource = $templating->render(
                'ElectrotechWeldqualBundle:Testweld:'.$template,
                array(
                    'entity'         => $entity,
                    'logoFile'       => $logoFile,
                    'qualifiedRange' => $qualifiedRange,
                )
            );

            return array(
                'latex'    => $latexSource,
                'filename' => $entity->getFilename()
            );
        }
    }


Further reading
---------------

*   `How to define controllers as services`_.
*   `The not so short introduction to LaTeX 2ε`_ by Tobias Oetiker.


.. _`LaTeX`: https://www.latex-project.org/
.. _`Symfony`: https://symfony.com/
.. _`TCPDF`: https://sourceforge.net/projects/tcpdf/
.. _`dompdf`: https://github.com/dompdf/dompdf
.. _`wkhtmltopdf`: https://github.com/wkhtmltopdf/wkhtmltopdf
.. _`KnpLabs/KnpSnappyBundle`: https://github.com/KnpLabs/KnpSnappyBundle
.. _`zendframework/ZendPdf`: https://github.com/zendframework/ZendPdf/
.. _`TeX macro language`: http://tug.org/
.. _`Services`: https://symfony.com/doc/2.3/book/service_container.html
.. _`definition of a service`: https://symfony.com/doc/2.3/glossary.html#term-service
.. _`YAML`: https://yaml.org/
.. _`Twig`: https://twig.symfony.com/
.. _`custom Twig filter`: https://twig.symfony.com/doc/3.x/advanced.html#filters
.. _`How to define controllers as services`: https://symfony.com/doc/2.3/cookbook/controller/service.html
.. _`The not so short introduction to LaTeX 2ε`: https://tobi.oetiker.ch/lshort/lshort.pdf
