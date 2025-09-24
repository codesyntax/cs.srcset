.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

.. image:: https://github.com/collective/cs.srcset/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/cs.srcset/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/cs.srcset/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/cs.srcset?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/cs.srcset/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/cs.srcset

.. image:: https://img.shields.io/pypi/v/cs.srcset.svg
    :target: https://pypi.python.org/pypi/cs.srcset/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/cs.srcset.svg
    :target: https://pypi.python.org/pypi/cs.srcset
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/cs.srcset.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/cs.srcset.svg
    :target: https://pypi.python.org/pypi/cs.srcset/
    :alt: License


=========
cs.srcset
=========

Backport of the `srcset` method added to the `@@images` view in plone.namedfile 7.1.0 to be able to use it in older Plone versions

Features
--------

It adds a view called `@@image-srcset` that has a single method called `srcset` to be able to create an `img` tag with the `srcset` and `sizes`
attributes to render responsive images.

Read more about responsive images and its use in the `MDN documentation`_


Documentation
-------------

::
    <img tal:define="images context/@@images-srcset;"
     tal:replace="structure python:images.srcset(
                                 fieldname='image',
                                 scale_in_src='huge',
                                 sizes='(min-width: 570px) 550px,90vw',
                                 css_class='mini w-100 h-100 responsive-3-2',
                                 alt=context.Title(),
                                 title=context.Title(),
                                 loading='lazy')"
    />





Installation
------------

Install cs.srcset by adding it to your buildout::

    [buildout]

    ...

    eggs =
        cs.srcset


and then running ``bin/buildout``



Contribute
----------

- Issue Tracker: https://github.com/codesyntax/cs.srcset/issues
- Source Code: https://github.com/codesyntax/cs.srcset


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the GPLv2.

.. _`MDN documentation`: https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images
