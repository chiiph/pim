#    Pim: A vim/emacs like text editor
#    Copyright (C) 2010 Tomas Touceda
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 2 as 
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from core.plugger import Plugger
from core.logger import Logger
from core.text import Text

import curses

class Editor:
	def __init__(self):
		self.logger= Logger() # Logger class

		self.texts= [] # Text objets in use

		self.activeText= 0 # The first active text will be an empty one
		self.lastKey= "" # Last key pressed
		self.status_message= "" # Last status message
		self.lineText= Text(self) # Text object for the command_line
		self.baseProperties= dict() # Plugin provided properties

		self.row= 0
		self.col= 1
		self.pref_col= 1
		
		self.maxrow= 0
		self.maxcol= 0

		self.activation= dict() # (keyCode string, plugin object)
		self.activeMode= None

		self.tabsize= 4

		self.actions= dict()
		self.states= dict()

		self.plugger= Plugger() # Plugin manager

		self.registerAll() # Register every plugin with self

		self.activateDefaultMode() # Activate the default mode

		self.addNewText() # Start with an empty text
	
	def register(self, var, place):
		for c in place:
			print "Adding "+c
			var[c]= self.plugger.classes[c](self)
			var[c].register()
	
	def registerAll(self):
		self.register(self.actions, self.plugger.actions)
		self.register(self.states, self.plugger.states)
	
	def addNewText(self):
		text= Text(self)
		self.texts.append(text)
		text.properties= self.baseProperties
		self.activeText=len(self.texts)-1 # Activate the last added text
	
	def activateDefaultMode(self):
		self.activeMode= self.actions["edit"]
	
	def changeMode(self):
		""" Changes the active mode if there's another mode register for that key, or leaves it as it is """
		oldMode= self.activeMode
		self.activeMode= self.activation.get(self.lastKey, self.activeMode)
		change= oldMode!=self.activeMode
		return change
	
	def run(self):
		self.activeMode.run(self.texts[self.activeText])
	
	def runLine(self):
		self.activeMode.run(self.lineText)
	
	def getLine(self, text):
		there= False
		i= 0
		chars= 0
		line= 0
		while not there:
			if i<len(text.lines):
				tmp= chars+len(text.lines[i])
				if not text.lines[i].marked:
					tmp+= 1
				if tmp>text.cursor:
					line= i
					there= True
				else:
					chars+=len(text.lines[i])
					if not text.lines[i].marked:
						chars+= 1
					i+=1
			else:
				there= True
		return (line, chars)

	def getText(self, init, end):
		txt= ""
		if len(self.texts)>0:
			txt= self.texts[self.activeText].getText(init, end)
		return txt
