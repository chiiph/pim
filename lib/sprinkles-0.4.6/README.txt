! sprinkles 0.4.5


!! Intro
Why? Every time I want to release a project I end up thinking, "Gee, wouldn't
it be cool if I had some kind of plugin system so that people could easily
extend the functionality of whatever script I was writing."

This library isn't particularly security-minded, it basically scans a
directory you specify and loads up the python files in it to look for 
classes that can be imported.

!! Usage
How? This is the more complex of the libraries I've written (I think) but 
let's see if I can explain it. What is *does* is fairly simple, what you
need to do to write a plugin is a little more complex.

What it does is search a directory, file, module, or package for 
importable python files, attempts to import them and then searches them
for classes that implement the ISprinke interface and then, if a 
specific filterer has been provided -- usually one of your interface's
implementedBy method, it will make sure the item passes that 
filter as well. If that all goes off without a hitch, it returns 
a list of classes.

To get a list of sprinkles in a directory:

    foo_sprinkles = sprinkles.fromPath(somedir)

... from a file

    bar_sprinkles = sprinkles.fromFile(somepath, somefilename)

... from a module

    baz_sprinkles = sprinkles.fromModule("some.mod")

... or if you happen to have a module already loaded

    baz_sprinkles = sprinkles.fromModule(some.mod)

... from a package

    quux_sprinkles = sprinkles.fromPackage("some.package")

Now, the more complex part is how to use a sprinkle in some sort of plugin
system. It's not really that complex, in fact it can be superbly simple, but 
the actual architecture of a plugin system is something people seem to have 
issues with.

!!! A simple sprinkle:
<pre>
from sprinkles import implements, ISprinkle
class FooSprinkle(object):
    implements(ISprinkle)
    foo = lambda _: _
</pre>

That's all you need for a sprinkle, but this sprinkle probably won't be all
that useful for you.

!!! A slightly more useful example:
(taken from workspace)
Let's assume your package has a layout something like:

workspace/__init__.py
workspace/core.py
workspace/interfaces.py
workspace/plugins/__init__.py
workspace/plugins/items.py

!!!! core.py
<pre>
import sprinkles
from workspace.interfaces import IWorkspaceSection
class Workspace(object):
    def __init__(self):
        self.sections = sprinkes.fromPackage("workspace.plugins",
                                             IWorkspaceSection.implementedBy)
    
    @classmethod
    def fromSystem(cls):
        self = cls()
        for s in self.sections:
            d = s.fromSystem()
            self.data[d.name] = d
        return self
    
    ...
</pre>

!!!! interfaces.py
<pre>
from sprinkles import ISprinkle, implements
class IWorkspaceSection(ISprinkle):
    @classmethod
    def fromSystem(self):
        """ initialize a section from the current system """
        
    ...
</pre>

!!!! items.py
<pre>
from workspace.interfaces import ISprinkle, implements
class ItemsSection(object):
    implements(ISprinkle)

    @classmethod
    def fromSystem(cls):
        self = cls()
        for s in self.sections:
            d = s.fromSystem()
            self.data[d.name] = d
        return self

    ...
</pre>


!! Module Contents
* class ISprinkle
                -- The base interface something must implement to be parsed

* def enableCache
* def disableCache
* def flushCache
                -- Deal with caching of already scanned modules
                
* def fromPath
* def fromFile
* def fromModule
* def fromPackage
                -- Load files from path, file, module or package.

* class Manager
* class IManagedSprinkle
* class ManagedSprinkle
                -- Some helper stuff to use as a plugin management system
                
!! Todo
What next? 

* Some security stuff, I guess. Probably won't extend much beyond checking
    permissions on the file and making sure it isn't world-writable though.

!! Conclusion
Generally, these libraries are provided as an idea about what you may be
interested in doing for yourself, my own way of massaging a few more syntax
niceties into the language I enjoy so much. If you find them useful, I'd love
to hear from you, especially if you have suggestions on additions and
improvements.

!! Author
AndySmith

love.


