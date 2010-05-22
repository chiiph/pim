import unittest
import sprinkles

s_dir = "test"
s_noexport = "test_noexport.py"
s_export = "test_export.py"
s_mod_dir = "test"
s_mod_export = "test.test_export"
s_mod_noexport = "test.test_noexport"

#f_noexport = open(s_noexport).read()
#f_export = open(s_export).read()

class baseTest:
    def testLength(self):
        self.assertEqual(len(mods),2)

    def testClass(self):
        self.assert_(issubclass(mods[0],sprinkles.Sprinkle))

    def testAttributes(self):
        self.assert_(mods[0].party == "fun" or mods[0].party == "time")

class TestFromFile(unittest.TestCase):
    def testExport(self):
        mods = sprinkles.from_file(s_dir, s_export)
        self.assertEqual(len(mods),2)
        self.assert_(issubclass(mods[0],sprinkles.Sprinkle))
        self.assert_(mods[0].party == "fun" or mods[0].party == "time")
    
    def testNoExport(self):
        mods = sprinkles.from_file(s_dir, s_noexport)
        self.assertEqual(len(mods),2)
        self.assert_(issubclass(mods[0],sprinkles.Sprinkle))
        self.assert_(mods[0].party == "fun" or mods[0].party == "time")

class TestFromDir(unittest.TestCase):
    def testLoad(self):
        mods = sprinkles.from_dir(s_dir)
        self.assertEqual(len(mods),4)
        self.assert_(issubclass(mods[0],sprinkles.Sprinkle))
        self.assert_(mods[0].party == "fun" or mods[0].party == "time")

class TestFromModule(unittest.TestCase):
    def testLoadExport(self):
        mods = sprinkles.from_mod(s_mod_export)
        self.assertEqual(len(mods),2)
        self.assert_(issubclass(mods[0],sprinkles.Sprinkle))
        self.assert_(mods[0].party == "fun" or mods[0].party == "time")
    
    def testLoadNoExport(self):
        mods = sprinkles.from_mod(s_mod_noexport)
        self.assertEqual(len(mods),2)
        self.assert_(issubclass(mods[0],sprinkles.Sprinkle))
        self.assert_(mods[0].party == "fun" or mods[0].party == "time")

class TestFromModuleDir(unittest.TestCase):
    def testLoad(self):
        mods = sprinkles.from_mod_dir(s_mod_dir)
        self.assertEqual(len(mods),4)
        self.assert_(issubclass(mods[0],sprinkles.Sprinkle))
        self.assert_(mods[0].party == "fun" or mods[0].party == "time")

if __name__ == "__main__":
    unittest.main()
