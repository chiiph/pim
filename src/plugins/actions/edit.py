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
		self.editor.logger.log("(inner_cursor,cursor)=("+str(text.inner_cursor)+","+str(text.cursor)+")")
		self.editor.logger.log("(row,col)=("+str(self.editor.row)+","+str(self.editor.col)+")")
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
#                text.updateInnerCursor()
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
		elif self.editor.lastKey == "ctrl right":
			self.findForwards(text)
		elif self.editor.lastKey == "tab":
			text.setText(text.text[:text.inner_cursor]+"\t"+text.text[text.inner_cursor:])
			self.moveRight(text)
		elif self.editor.lastKey == "enter":
			text.setText(text.text[:text.inner_cursor]+"\n"+text.text[text.inner_cursor:])
			self.moveRight(text)
		else:
			text.setText(text.text[:text.inner_cursor]+self.editor.lastKey+text.text[text.inner_cursor:])
			self.moveRight(text)

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
		# if the last char we move right of is the newline one
		if text.inner_cursor > 0 and text.text[text.inner_cursor-1] == "\n":
			text.line_pos += 1
			self.editor.logger.log("new line")

		if text.inner_cursor<len(text.text):
			length = 1
			# tab is special since it's displayed as multiple spaces
			if text.text[text.inner_cursor] == "\t":
				# we must check where's the next column where the tab stops
				# to find how many spaces we should jump
				for i in range(0, self.editor.tabsize):
					tmp = (self.getCol(text) + self.editor.tabsize - i)
					# if this offset is the one, continue with the jumping
					if tmp%self.editor.tabsize == 0:
						self.editor.logger.log("TAB###: "+str(self.editor.col)+", i: "+str(i))
						length = self.editor.tabsize - i
						break

			# the inner_cursor is always moved +1
			text.inner_cursor += 1
			# the display cursor is moved 1 or tabsize-some_offset
			text.cursor += length

	
	def getCol(self, text):
		""" Return an UI independant column """
		(line, chars) = self.editor.getLine(text)
		col= text.cursor-chars
		return col
	
	def moveLeft(self, text):
		# if the last char we move left of is the newline one
		if text.inner_cursor + 1 < len(text.text) and text.text[text.inner_cursor+1] == "\n":
			text.line_pos -= 1

		if text.cursor>0:
			text.inner_cursor -= 1
			text.cursor -= 1
			# tab's the special case
			if text.text[text.inner_cursor] == "\t":
				# lets see what's the char behind this tab
				if text.inner_cursor > 0:
					if text.text[text.inner_cursor-1] == "\t":
						# if there's another tab, just move the rest of the tabsize
						text.cursor -= self.editor.tabsize - 1
					elif text.text[text.inner_cursor-1] == " ":
						# for now we handle this like vim does:
						# if there's a space, consider it part of the tab
						i = 0
						while (text.cursor - i) > 0 \
							and text.getAllText()[text.cursor - i] == " "\
							and i < self.editor.tabsize:
							text.cursor -= 1
							i += 1
					else:
						# while we are still in the space defined tab
						# keep going back
						while text.cursor > 0 and \
							text.getAllText()[text.cursor] == " ":
							text.cursor -= 1
						# and we correct the cursor since we want to
						# stand in the tab, no before it
						text.cursor += 1
		
	def backspace(self, text):
		if text.inner_cursor > 0:
			# we move the cursors one char left
			self.moveLeft(text)

			# and then we erease the char we skipped
			text.setText(text.text[:text.inner_cursor]+text.text[text.inner_cursor+1:])

	def register(self):
		self.editor.activation["meta d"]= self
