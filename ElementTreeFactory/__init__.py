# vim: set et sw=4 ts=4:

import elementtree.ElementTree as et

__all__ = ['ElementTreeFactory', 'tag']

class ElementTreeFactory(object):
    """A class inspired by Genshi for easy creation of ElementTree Elements.

    The ElementFactory class was inspired by the Genshi builder unit in that it
    permits simple creation of Elements by calling methods on the tag object
    named after the element you wish to create. Positional arguments become
    content within the element, and keyword arguments become attributes.

    If you need an attribute or element tag that conflicts with a Python
    keyword, simply append an underscore to the name (which will be
    automatically stripped off).

    Content can be just about anything, including booleans, integers, longs,
    dates, times, etc. This class simply applies their default string
    conversion to them (except basestring derived types like string and unicode
    which are simply used verbatim).

    For example:

    >>> import xml.etree.ElementTree as et
    >>> from etreefactory import tag
    >>> et.tostring(tag.a('A link'))
    '<a>A link</a>'
    >>> et.tostring(tag.a('A link', class_='menuitem'))
    '<a class="menuitem">A link</a>'
    >>> et.tostring(tag.p('A ', tag.a('link', class_='menuitem')))
    '<p>A <a class="menuitem">link</a></p>'
    """

    def __init__(self, namespace=None):
        """Intializes an instance of the ElementTreeFactory.

        Most users should have no need to instantiate an ElementTreeFactory
        instance directly. Most will wish to use the "tag" instance created in
        the module, while those that wish to customize the output will subclass
        ElementTreeFactory and create an instance of their subclass.

        The optional namespace parameter can be used to specify the namespace
        used to qualify all elements generated by an instance of the class.
        Rather than specifying this explicitly when constructing the class it
        is recommended that developers sub-class this class, and specify the
        namespace as part of an overridden __init__ method. In other words,
        make dialect specific sub-classes of this generic class (an
        HTMLElementFactory class for instance).
        """
        self._namespace = namespace

    def _find(self, root, tagname, id=None):
        """Returns the first element with the specified tagname and id"""
        if id is None:
            result = root.find('.//%s' % tagname)
            if result is None:
                raise LookupError('Cannot find any %s elements' % tagname)
            else:
                return result
        else:
            result = [
                elem for elem in root.findall('.//%s' % tagname)
                if elem.attrib.get('id', '') == id
            ]
            if len(result) == 0:
                raise LookupError('Cannot find a %s element with id %s' % (tagname, id))
            elif len(result) > 1:
                raise LookupError('Found multiple %s elements with id %s' % (tagname, id))
            else:
                return result[0]

    def _format(self, content):
        """Reformats content into a human-readable string"""
        if isinstance(content, basestring):
            # Strings (including unicode) are returned verbatim
            return content
        else:
            # Everything else is converted to a unicode string
            return unicode(content)

    def _append(self, node, contents):
        """Adds content (string, node, node-list, etc.) to a node"""
        if isinstance(contents, basestring):
            if contents != '':
                if len(node) == 0:
                    if node.text is None:
                        node.text = contents
                    else:
                        node.text += contents
                else:
                    last = node[-1]
                    if last.tail is None:
                        last.tail = contents
                    else:
                        last.tail += contents
        elif iselement(contents):
            contents.tail = ''
            node.append(contents)
        else:
            try:
                for content in contents:
                    self._append(node, content)
            except TypeError:
                self._append(node, self._format(contents))

    def _element(self, _name, *contents, **attrs):
        if self._namespace:
            _name = '{%s}%s' % (self._namespace, _name)
            attrs = dict(
                ('{%s}%s' % (self._namespace, key), value)
                for (key, value) in attr.iteritems()
            )
        def clean_attr(key, value):
            # This little utility routine is used to clean up attributes:
            # boolean True is represented as the key (as in checked="checked"),
            # boolean False is discarded, all other values are converted to
            # strings, and trailing underscores are removed from key names
            # (convenience for names which are python keywords)
            if not isinstance(key, basestring):
                key = unicode(key)
            else:
                key = key.rstrip('_')
            if value is True:
                value = key
            elif not isinstance(value, basestring):
                value = unicode(value)
            return key, value
        e = Element(_name, dict(
            clean_attr(key, value)
            for key, value in attrs.iteritems()
            if value is not None and value is not False
        ))
        for content in contents:
            self._append(e, content)
        return e

    def __getattr__(self, name):
        elem_name = name.rstrip('_')
        # We could simply return the generated tag, but it's more efficient in
        # the long-run to cache the created generator method
        def generator(*content, **attrs):
            return self._element(elem_name, *content, **attrs)
        setattr(self, name, generator)
        return generator

