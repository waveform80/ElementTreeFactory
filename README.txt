Still gotta write this. For now, I'll assume you know what you're doing and let
the code do the talking:

$ easy_install ElementTreeFactory


Then in your python code:

import xml.etree.ElementTree as et
from ElementTreeFactory import tag

print et.tostring(
    tag.html(
        tag.head(
            tag.link(rel='stylesheet', href='default.css', type_='text/css', media='screen'),
            tag.title('This is a test document'),
        ),
        tag.body(
            tag.h1('Welcome to ElementTreeFactory'),
            tag.p('This is a short demonstration of usage of ElementTreeFactory', class_='bodytext'),
            tag.ul(
                tag.li('Item %d' % n)
                for n in range(5)
            )
        )
    )
)
