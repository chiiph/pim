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

from core import keys
from core.text import Text
from core.editor import Editor

import curses

class Edit:
	def __init__(self, edt):
		self.editor= edt
		self.key= 0 # Activation key
		self.name= "Edit"
		self.mode= 0

		self.tabs= []

		self.cutchars= ['(',' ',')',',']
	
	def run(self,text):
		if self.editor.lastKey == "backspace":
			self.backspace(text)
		elif self.editor.lastKey == "delete":
			text.setText(text.text[:text.cursor]+text.text[text.cursor+1:])
		elif self.editor.lastKey == "up":
			if self.editor.row>0:
				self.editor.row-= 1
				if self.editor.col>len(text.lines[self.editor.row]):
					self.editor.col= len(text.lines[self.editor.row])
				self.editor.updateCursor(text)
		elif self.editor.lastKey == "down":
			if self.editor.row<len(text.lines)-1:
				self.editor.row+= 1
				if self.editor.col>len(text.lines[self.editor.row]):
					self.editor.col= len(text.lines[self.editor.row])
				self.editor.updateCursor(text)
		elif self.editor.lastKey == "left":
			self.moveLeft(text)
		elif self.editor.lastKey == "right":
			self.moveRight(text)
		elif self.editor.lastKey == "home":
			self.editor.col= 0
			self.editor.updateCursor(text)
			self.editor.lastKey= ""
		elif self.editor.lastKey == "end":
			self.editor.col= len(text.lines[self.editor.getLine(text)])
			self.editor.updateCursor(text)
			self.editor.lastKey= ""
		elif self.editor.lastKey == "ctrl left":
			self.findBackwards(text)
			self.editor.updateRowCol(text)
		elif self.editor.lastKey == "ctrl right":
			self.findForwards(text)
			self.editor.updateRowCol(text)
		elif self.editor.lastKey == "tab":
			text.setText(text.text[:text.cursor]+(" "*self.editor.tabsize)+text.text[text.cursor:])
			text.properties["tabs"].append(text.cursor)
			text.cursor+= self.editor.tabsize
			self.editor.updateRowCol(text)
		elif self.editor.lastKey == "enter":
			text.setText(text.text[:text.cursor]+"\n"+text.text[text.cursor:])
			text.cursor+= 1
			self.editor.updateRowCol(text)
		else:
			text.setText(text.text[:text.cursor]+self.editor.lastKey+text.text[text.cursor:])
			text.cursor+=1
			self.editor.updateRowCol(text)

	def findForwards(self, text):
		if text.text[text.cursor] in self.cutchars:
			text.cursor+=1
		while not text.text[text.cursor] in self.cutchars and text.cursor<len(text.text):
			text.cursor+=1
	
	def findBackwards(self, text):
		if text.text[text.cursor] in self.cutchars:
			text.cursor+=1
		while not text.text[text.cursor] in self.cutchars and text.cursor>0:
			text.cursor-=1
	
	def moveRight(self, text):
		length= 1
		if text.cursor in self.tabs:
			length= self.editor.tabsize
		if self.editor.col<self.editor.maxcol and self.editor.col<(len(text.lines[self.editor.row])):
			self.editor.col+= length
			self.editor.updateCursor(text)
	
	def moveLeft(self, text):
		length= 1
		if (text.cursor-self.editor.tabsize) in self.tabs:
			length= self.editor.tabsize
		if self.editor.col>0:
			self.editor.col-= length
			self.editor.updateCursor(text)
	
	def backspace(self, text):
		if text.cursor > 0:
			length= 1
			tab= text.cursor-self.editor.tabsize
			if tab in self.tabs:
				length= self.editor.tabsize
				self.tabs.remove(tab)
			text.setText(text.text[:text.cursor-length]+text.text[text.cursor:])
			text.cursor-= length
			self.editor.updateRowCol(text)

	def register(self):
		self.editor.activation["meta d"]= self
