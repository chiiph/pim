import imp, os, os.path, types, sys
from zope.interface import Interface, Attribute, implements
try:
    from scribe import loggingapi as logging
except ImportError:
    import logging

# config

class Cache(object):
    cachedPaths = {}
    cachedFiles = {}
    cachedPackages = {}
    cachedModules = {}

    def getCachedPath(self, path):
        if path in self.cachedPaths.keys():
            logging.debug("Found cached path: %s"%(path))
            return self.cachedPaths[path]
        return None
    def getCachedFile(self, path, filename):
        f = os.path.join(path, filename)
        if f in self.cachedFiles.keys():
            logging.debug("Found cached file: %s"%(f))
            return self.cachedFiles[f]
        return None
    def getCachedPackage(self, package):
        if package in self.cachedPackages.keys():
            logging.debug("Found cached package: %s"%(package))
            return self.cachedPackages[package]
        return None
    def getCachedModule(self, module):
        if module in self.cachedModules.keys():
            logging.debug("Found cached module: %s"%(module))
            return self.cachedModules[module]
        return None

    def addCachedPath(self, path, l):
        self.cachedPaths[path] = l
    def addCachedFile(self, path, filename, l):
        f = os.path.join(path, filename)
        self.cachedFiles[f] = l
    def addCachedPackage(self, package, l):
        self.cachedPackages[package] = l
    def addCachedModule(self, module, l):
        self.cachedModules[module] = l

    def flush(self):
        self.cachedPaths = {}
        self.cachedFiles = {}
        self.cachedPackages = {}
        self.cachedModules = {}
        
        
_cache = Cache()

_caching = True
def enableCache():
    _caching = True

def disableCache():
    _caching = False

def flushCache():
    _cache.flush()

"""Thanks to Molly for the superb name of this module"""
def fromPath(path, filterer=None):
    logging.debug('Looking for sprinkles in path: %s...'%(path))
    o = None
    if _caching:
        o = _cache.getCachedPath(path)
    if not o:
        o = []
        files = set([os.path.splitext(x)[0] for x in os.listdir(path)])
        for f in files:
            logging.debug('Found file: %s'%(f))
            loaded = fromFile(path, f)
            o = o + loaded
        if _caching:
            _cache.addCachedPath(path, o)
    if filterer:
        logging.debug('Filtering %s with %s'%(o, filterer))
        o = filter(filterer, o)
    logging.debug("Passed: %s"%(o))
    return o
def fromFile(path, filename, filterer=None):
    logging.debug('Looking for file: %s'%(os.path.join(path, filename)))
    o = None
    if _caching:
        o = _cache.getCachedFile(path, filename)
    if not o:
        o = []
        mod_name = os.path.splitext(filename)[0]
        new_mod = None
        try:
            fp, pathname, desc = imp.find_module(mod_name,[path])
            try:
                logging.debug('Found, attempting to load...')
                new_mod = imp.load_module(mod_name,fp,pathname,desc)
                logging.debug('Loaded: %s'%(new_mod))
            finally:
                if fp: fp.close()
        except ImportError, err:
            logging.debug('Failed to import %s, %s'%(mod_name, err))
        if not new_mod:
            return []
        o = fromModule(new_mod)
        if _caching:
            _cache.addCachedFile(path, filename, o)
        if filterer:
            o = filter(filterer, o)
    return o
def fromPackage(package, filterer = None):
    logging.debug("Attempting to load from package: %s"%(package))
    if _caching:
        o = _cache.getCachedPackage(package)
    if not o:
        o = []
        new_mod = __import__(package, None, None, "*")
        if not hasattr(new_mod, "__path__"):
            raise Exception("Not a package")
        for p in new_mod.__path__:
            o = o + fromPath(p)
        if _caching:
            _cache.addCachedPackage(package, o)
    if filterer:
        o = filter(filterer, o)
    return o
def fromModule(mod, filterer=None):
    if _caching:
        o = _cache.getCachedModule(mod)
    if not o:
        o = []
        if type(mod) is type(""):
            mod = _import(mod)
        if hasattr(mod, "EXPORTS"):
            s = getattr(mod, "EXPORTS")
        else:
            s = [getattr(mod, x) for x in dir(mod)]
        s = filter(lambda _: (type(_) is type(object)), s)
        o = filter(ISprinkle.implementedBy, s)
        logging.debug("Found sprinkles: %s"%(o))
        if _caching:
            _cache.addCachedModule(mod, o)
    if filterer:
        logging.debug('Filtering %s with %s'%(o, filterer))
        o = filter(filterer, o)
    return o

class ISprinkle(Interface):
    pass


"""Here is a helpful pattern"""
class IManagedSprinkle(ISprinkle):
    enabled = Attribute("""the enabled state of the sprinkle""")
    name = Attribute("""the name of the sprinkle""")
    manager = Attribute("""the Manager instance holding this sprinkle""")

    def setManager(self, mgr):
        """set this sprinkle's manager"""

    def load(self):
        """initialize the sprinkle"""

    def unload(self):
        """clean up the sprinkle"""

    def enable(self):
        """turn on the sprinkle"""

    def disable(self):
        """turn off the sprinkle"""
class ManagedSprinkle(object):
    implements(IManagedSprinkle)
    enabled = False
    name = "ManagedSprinkle"
    manager = None
    
    def setManager(self, mgr):
        self.manager = mgr
    
    def load(self):
        pass

    def unload(self):
        pass

    def enable(self):
        self.enabled = True

    def disable(self):
        self.disabled = True

class ManagedSprinkleMixin(object):
    enabled = False
    name = "ManagedSprinkle"
    manager = None
    
    def setManager(self, mgr):
        self.manager = mgr
    
    def load(self):
        pass

    def unload(self):
        pass

    def enable(self):
        self.enabled = True

    def disable(self):
        self.disabled = True

class Manager(object):
    loaded = []
    
    def __init__(self, packages=[], parent=None, 
                 filter=IManagedSprinkle.implementedBy):
        #self.loaded = []
        self.packages = packages
        self.parent = parent
        self.filter = filter

    def load(self, sprinkles=None):
        if sprinkles is None:
            sprinkles = []
            for p in self.packages:
                for s in fromPackage(p, self.filter):
                    sprinkles.append(s)
        sprinkles = list(set(sprinkles))
        for x in sprinkles:
            g = x(self.parent)
            g.load()
            self.loaded.append(g)

    def unload(self, sprinkles=None):
        """ensure a sprinkle is disabled and unload it"""
        """maybe this is useful to free memory?"""
        if sprinkles is None:
            sprinkles = self.loaded[:]
        for m in sprinkles:
            if m.enabled:
                m.disable()
            m.unload()
            self.loaded.remove(m)

    def enable(self, sprinkles=None):
        if sprinkles is None:
            sprinkles = self.loaded
        for x in sprinkles:
            if not x.enabled:
                x.enable()

    def disable(self, sprinkles=None):
        if sprinkles is None:
            sprinkles = self.enabled
        for x in sprinkles:
            if x.enabled:
                x.disable()
    
    @property
    def enabled(self):
        return [x for x in self.loaded if x.enabled]


    # group actions
    def each(self, method, *args, **kw):
        for x in self.enabled:
            if hasattr(x, method):
                getattr(x, method)(*args, **kw)

    def all(self, method, *args, **kw):
        for x in self.enabled:
            if hasattr(x, method):
                if not getattr(x, method)(*args, **kw):
                    return False
        return True

    def any(self, method, *args, **kw):
        for x in self.enabled:
            if hasattr(x, method):
                if getattr(x, method)(*args, **kw):
                    return True
        return False

    def which(self, method, *args, **kw):
        o = []
        for x in self.enabled:
            if hasattr(x, method):
                if getattr(x, method)(*args, **kw):
                    o.append(x)
        return o

    def gather(self, method, *args, **kw):
        o = []
        for x in self.enabled:
            if hasattr(x, method):
                o.append(getattr(x, method)(*args, **kw))
        return o

    def __getattr__(self, name):
        for x in self.loaded:
            if x.name == name:
                return x
        raise AttributeError



"""Mostly a bunch of stuff directly from the 'knee' demo module"""
# Replacement for __import__()
def _import(name):
    logging.debug("Importing: %s" % (name))
    mod = import_hook(name)
    logging.debug("Found module: %s" % (mod))
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
        logging.debug("Found module: %s" % (mod))
    return mod
def import_hook(name, globals=None, locals=None, fromlist=None):
    parent = determine_parent(globals)
    q, tail = find_head_package(parent, name)
    m = load_tail(q, tail)
    if not fromlist:
        return q
    if hasattr(m, "__path__"):
        ensure_fromlist(m, fromlist)
    return m
def determine_parent(globals):
    if not globals or  not globals.has_key("__name__"):
        return None
    pname = globals['__name__']
    if globals.has_key("__path__"):
        parent = sys.modules[pname]
        assert globals is parent.__dict__
        return parent
    if '.' in pname:
        i = pname.rfind('.')
        pname = pname[:i]
        parent = sys.modules[pname]
        assert parent.__name__ == pname
        return parent
    return None
def find_head_package(parent, name):
    if '.' in name:
        i = name.find('.')
        head = name[:i]
        tail = name[i+1:]
    else:
        head = name
        tail = ""
    if parent:
        qname = "%s.%s" % (parent.__name__, head)
    else:
        qname = head
    q = import_module(head, qname, parent)
    if q: return q, tail
    if parent:
        qname = head
        parent = None
        q = import_module(head, qname, parent)
        if q: return q, tail
    raise ImportError, "No module named " + qname
def load_tail(q, tail):
    m = q
    while tail:
        i = tail.find('.')
        if i < 0: i = len(tail)
        head, tail = tail[:i], tail[i+1:]
        mname = "%s.%s" % (m.__name__, head)
        m = import_module(head, mname, m)
        if not m:
            raise ImportError, "No module named " + mname
    return m
def ensure_fromlist(m, fromlist, recursive=0):
    for sub in fromlist:
        if sub == "*":
            if not recursive:
                try:
                    all = m.__all__
                except AttributeError:
                    pass
                else:
                    ensure_fromlist(m, all, 1)
            continue
        if sub != "*" and not hasattr(m, sub):
            subname = "%s.%s" % (m.__name__, sub)
            submod = import_module(sub, subname, m)
            if not submod:
                raise ImportError, "No module named " + subname
def import_module(partname, fqname, parent):
    try:
        return sys.modules[fqname]
    except KeyError:
        pass
    try:
        fp, pathname, stuff = imp.find_module(partname,
                                              parent and parent.__path__)
    except ImportError:
        return None
    try:
        m = imp.load_module(fqname, fp, pathname, stuff)
    finally:
        if fp: fp.close()
    if parent:
        setattr(parent, partname, m)
    return m


# deprecated names
from_path = fromPath
from_dir = fromPath
form_mod = fromModule
from_module = fromModule
from_mod_dir = fromPackage
from_package = fromPackage
from_file = fromFile
