import sys,os,re
class Plugger:
	def __init__(self):
		self.actions= dict()
		self.states= dict()

		self.classes= dict()
		self.loadAll()

	def loadAll(self):
		""" Loads all the plugins in the base path """

		self.load("actions", self.actions)
		self.load("states", self.states)
		print self.classes

	def load(self, dir, var):
		""" Loads all the plugins in dir to var and saves them to classes """
		
		filt= re.compile(".py$", re.IGNORECASE)
		files= filter(filt.search,os.listdir("plugins/"+dir+"/"))
		for f in files:
			file= f.replace(".py", "")
			if file!= "__init__":
				var[file]= file.capitalize()

		for act in var:
			print "Loading "+act+"..."
			res = __import__("plugins."+dir+"."+act, globals(), locals(), [var[act]], -1)
			self.classes[act]= getattr(res, var[act])
