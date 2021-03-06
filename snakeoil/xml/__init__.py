# Copyright: 2006-2009 Brian Harring <ferringb@gmail.com>
# License: BSD/GPL2

"""
Compatibility code, preferring cElementTree, falling back to ElementTree.
"""

try:
    # pylint: disable=import-error
    from xml.etree import cElementTree as etree
except ImportError:
    from xml.etree import ElementTree as etree
