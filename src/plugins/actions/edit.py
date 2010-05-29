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

		self.cutchars= ['(',' ',')',',']
	
	def run(self,text):
		if self.editor.lastKey == "backspace":
			if text.cursor > 0:
				text.setText(text.text[:text.cursor-1]+text.text[text.cursor:])
				text.cursor-= 1
				self.editor.updateRowCol(text)
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
					self.editor.col= len(text.lines[self.editor.row])-1
				self.editor.updateCursor(text)
		elif self.editor.lastKey == "left":
			if self.editor.col>0:
				self.editor.col-= 1
				self.editor.updateCursor(text)
		elif self.editor.lastKey == "right":
			if self.editor.col<self.editor.maxcol and self.editor.col<(len(text.lines[self.editor.row])):
				self.editor.col+= 1
				self.editor.updateCursor(text)
		elif self.editor.lastKey == "home":
			self.editor.col= 0
			self.editor.updateCursor(text)
			self.editor.lastKey= ""
		elif self.editor.lastKey == "end":
			self.editor.col= len(text.lines[self.editor.getLine(text)])-1
			self.editor.updateCursor(text)
			self.editor.lastKey= ""
		elif self.editor.lastKey == "ctrl left":
			self.findBackwards(text)
			self.editor.updateRowCol(text)
		elif self.editor.lastKey == "ctrl right":
			self.findForwards(text)
			self.editor.updateRowCol(text)
		else:
			if text.lines[self.editor.getLine(text)].marked:
				text.setText(text.text[:text.cursor-1]+self.editor.lastKey+text.text[text.cursor-1:])
			else:
				text.setText(text.text[:text.cursor]+self.editor.lastKey+text.text[text.cursor:])
			text.cursor+=1
			self.editor.updateRowCol(text)

	def findForwards(self, text):
		while not text.text[text.cursor] in self.cutchars and text.cursor<len(text.text):
			text.cursor+=1
	
	def findBackwards(self, text):
		while not text.text[text.cursor] in self.cutchars and text.cursor>0:
			text.cursor-=1

	def register(self):
		# alt+d
		self.editor.activation["meta d"]= self
