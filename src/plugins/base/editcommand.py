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

from core.text import Text
from core.editor import Editor

import curses

class EditCommand(object):
	def __init__(self, edt):
		self.editor= edt
		self.key= 0 # Activation key
		self.name= "EditCommand"
		self.mode= 0
	
	def run(self,text):
		if self.editor.lastKey == "backspace":
			self.backspace(text)
		elif self.editor.lastKey == "delete":
			text.setText(text.text[:text.cursor]+text.text[text.cursor+1:])
		elif self.editor.lastKey == "up":
			return
		elif self.editor.lastKey == "down":
			return
		elif self.editor.lastKey == "left":
			self.moveLeft(text)
		elif self.editor.lastKey == "right":
			self.moveRight(text)
		elif self.editor.lastKey == "home":
			(line, chars)= self.editor.getLine(text)
			text.cursor-=(text.cursor-chars)
			self.editor.lastKey= ""
		elif self.editor.lastKey == "end":
			(line, chars)= self.editor.getLine(text)
			text.cursor+=(len(text.lines[line])-(text.cursor-chars))
			self.editor.lastKey= ""
		elif self.editor.lastKey == "ctrl left":
			return
		elif self.editor.lastKey == "ctrl right":
			return
		elif self.editor.lastKey == "tab":
			return
		elif self.editor.lastKey == "enter":
			return
		else:
			text.setText(text.text[:text.cursor]+self.editor.lastKey+text.text[text.cursor:])
			text.cursor+=1
			self.editor.updateRowCol(text)

	def moveRight(self, text):
		length= 1
		if self.editor.col<self.editor.maxcol and self.editor.col<(len(text.lines[self.editor.row])):
			self.editor.col+= length
			self.editor.updateCursor(text)
	
	def moveLeft(self, text):
		length= 1
		if self.editor.col>0:
			self.editor.col-= length
			self.editor.updateCursor(text)
	
	def backspace(self, text):
		if text.cursor > 0:
			length= 1
			text.setText(text.text[:text.cursor-length]+text.text[text.cursor:])
			text.cursor-= length
#            self.editor.updateRowCol(text)
