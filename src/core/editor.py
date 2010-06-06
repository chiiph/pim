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

import curses

class Editor:
	def __init__(self):
		self.logger= Logger()

		self.texts= []
		self.activeText= 0
		self.lineText= None
		self.lastKey= ""
		self.status_message= ""

		self.row= 0
		self.col= 0
		
		self.maxrow= 0
		self.maxcol= 0

		self.activation= dict() # (keyCode string, plugin object)
		self.activeMode= None

		self.tabsize= 3

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
		self.activeMode= self.activation.get(self.lastKey, self.activeMode)
		change= oldMode!=self.activeMode
		if change:
			if self.activeMode.mode == 1:
				self.updateRowCol(self.lineText)
			elif self.activeMode.mode == 0:
				self.updateRowCol(self.texts[self.activeText])
		return change
	
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
				tmp= chars+len(text.lines[i])
				if not text.lines[i].marked:
					tmp+= 1
				if tmp>text.cursor:
					self.col= text.cursor-chars
					if text.lines[i].marked:
						self.col+= 1
					there= True
				else:
					self.row+= 1
					chars+=len(text.lines[i])
					if not text.lines[i].marked:
						chars+= 1
					i+=1
			else:
				there= True
	
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
		return line

	def updateCursor(self, text):
		i= 0
		sumat= 0
		for l in text.lines:
			if i==self.row:
				text.cursor= sumat+self.col
				if l.marked:
					text.cursor-=1
				break
			else:
				sumat+=len(l)
				if not l.marked:
					sumat+=1
				i+= 1
	
	def getText(self, init, end):
		txt= ""
		if len(self.texts)>0:
			txt= self.texts[self.activeText].getText(init, end)
		return txt
