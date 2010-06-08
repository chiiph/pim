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
			(line,chars) = self.editor.getLine(text)
#            if len(text.lines[line])>self.editor.maxcol:
#                if
			if line>0:
				# TODO
				# Long line case
#                if len(text.lines[line])>self.editor.maxcol and self.editor.maxcol>(len(text.lines[line])-(text.cursor-chars)):
#                    text.cursor -= self.editor.maxcol
				# end of long line case
#                else:
				maxcol = len(text.lines[line-1])
				linepos = text.cursor-chars
				newpos = linepos
				if linepos>maxcol:
					newpos = maxcol
				text.cursor -= linepos # What's left of that line
				if not text.lines[line-1].marked:
					text.cursor -= 1 # minus \n char if it isn't a marked line
				text.cursor -= maxcol-newpos # minus the new column
				text.updateInnerCursor()
		elif self.editor.lastKey == "down":
			(line,chars) = self.editor.getLine(text)
			if line<len(text.lines)-1:
				# TODO
				# Long line case
#                if self.editor.maxcol<(len(text.lines[line])-(text.cursor-chars)):
#                    text.cursor += self.editor.maxcol
				# end of long line case
#                else:
				maxcol = len(text.lines[line+1])
				linepos = text.cursor-chars
				newpos = linepos
				if linepos>maxcol:
					newpos = maxcol
				text.cursor += len(text.lines[line])-linepos # What's left of that line
				if not text.lines[line].marked:
					text.cursor += 1 # plus \n char if it isn't a marked line
				text.cursor += newpos # plus the new column
				text.updateInnerCursor()
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
			self.findBackwards(text)
			self.editor.updateRowCol(text)
		elif self.editor.lastKey == "ctrl right":
			self.findForwards(text)
			self.editor.updateRowCol(text)
		elif self.editor.lastKey == "tab":
			(line, chars) = self.editor.getLine(text)
			col= text.cursor-chars
			pos= self.editor.tabsize-(col%self.editor.tabsize)
			text.properties["tabs"].append(text.cursor)
			text.setText(text.text[:text.inner_cursor]+"\t"+text.text[text.inner_cursor:])
			text.cursor += pos
			text.inner_cursor += 1
			self.editor.updateRowCol(text)
		elif self.editor.lastKey == "enter":
			text.setText(text.text[:text.inner_cursor]+"\n"+text.text[text.inner_cursor:])
			text.cursor+=1
			text.inner_cursor += 1
			self.editor.updateRowCol(text)
		else:
			text.setText(text.text[:text.inner_cursor]+self.editor.lastKey+text.text[text.inner_cursor:])
			text.cursor+=1
			text.inner_cursor += 1
			self.editor.updateRowCol(text)

	def findForwards(self, text):
		if len(text.lines)<self.editor.row:
			return
		if text.text[text.cursor] in self.cutchars:
			text.cursor+=1
		while not text.text[text.cursor] in self.cutchars and text.cursor<len(text.text):
			text.cursor+=1
	
	def findBackwards(self, text):
		if len(text.lines)<self.editor.row:
			return
		if text.text[text.cursor] in self.cutchars:
			text.cursor-=1
		while not text.text[text.cursor] in self.cutchars and text.cursor>0:
			text.cursor-=1
	
	def moveRight(self, text):
		if text.inner_cursor<len(text.text):
			text.inner_cursor += 1
			text.updateCursor()
	
	def moveLeft(self, text):
		if text.cursor>0:
			text.inner_cursor -= 1
			text.updateCursor()
		
	def backspace(self, text):
		if text.inner_cursor > 0:
			text.setText(text.text[:text.inner_cursor-1]+text.text[text.inner_cursor:])
			text.inner_cursor -= 1
			text.updateCursor()
			self.editor.updateRowCol(text)

	def register(self):
		self.editor.activation["meta d"]= self
		# Init every property used by this plugin
		self.editor.baseProperties["tabs"]= []
