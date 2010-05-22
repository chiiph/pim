from core.plugger import Plugger

import curses

class Editor:
	def __init__(self):
		self.texts= []
		self.activeText= 0
		self.lineText= None
		self.lastKey = 0

		self.row= 0
		self.col= 0
		
		self.maxrow= 0
		self.maxcol= 0

		self.activation= dict() # (keyCode, object)
		self.activeMode= None

		self.tabsize= 7 # FIXME

		self.actions= dict()
		self.states= dict()

		self.plugger= Plugger()

		self.registerAll()

		self.activateDefaultMode()
	
	def register(self, var, place):
		for c in place:
			print "Adding "+c
			var[c]= self.plugger.classes[c](self)
			var[c].register()
	
	def registerAll(self):
		self.register(self.actions, self.plugger.actions)
		self.register(self.states, self.plugger.states)
	
	def activateDefaultMode(self):
		self.activeMode= self.actions["edit"]
	
	def changeMode(self):
		""" Changes the active mode if there's another mode register for that key, or leaves it as it is """
		oldMode= self.activeMode
		self.activeMode= self.activation.get(curses.keyname(self.lastKey), self.activeMode)
		return oldMode!=self.activeMode
	
	def run(self):
		self.activeMode.run(self.texts[self.activeText])
	
	def runLine(self):
		self.activeMode.run(self.lineText)
	
	def updateRowCol(self, text):
		there= False
		i= 0
		chars= 0
		self.row= 0
		self.col= 0
		while not there:
			if i<len(text.lines):
				tmp= chars+len(text.lines[i])+1
				if tmp>text.cursor and tmp<self.maxcol:
					self.col= text.cursor-chars
					there= True
				else:
					self.row+= 1
					chars+=(len(text.lines[i])+1)
					i+=1
			else:
				there= True
	
	def updateCursor(self, text):
		i= 0
		sumat= 0
		for l in text.lines:
			if i==self.row:
				text.cursor= sumat+self.col
				break
			else:
				sumat+=len(l)+1
				i+= 1
	
	def getText(self, init, end):
		return self.texts[self.activeText].getText(init, end)
