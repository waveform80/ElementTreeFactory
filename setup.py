#!/usr/bin/env python
# vim: set et sw=4 ts=4:

"""A Genshi-inspired framework for easy use of ElementTree.

ElementTreeFactory is a class inspired by Genshi's ElementFactory class which
allows for construction of XML documents with code which directly reflects the
structure of the resulting document."""

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Topic :: Text Processing :: Markup :: XML',
    'Topic :: Text Processing :: Markup :: HTML',
]

def main():
    setup(
        name                 = 'ElementTreeFactory',
        version              = '1.0',
        description          = 'A Genshi-inspired framework for easy use of ElementTree',
        long_description     = __doc__,
        author               = 'Dave Hughes',
        author_email         = 'dave@waveform.org.uk',
        url                  = 'https://github.com/waveform80/ElementTreeFactory',
        keywords             = ['xml', 'etree'],
        packages             = find_packages(exclude=['ez_setup']),
        install_requires     = [],
        include_package_data = True,
        platforms            = 'ALL',
        zip_safe             = True,
        classifiers          = classifiers
    )

if __name__ == '__main__':
    main()
